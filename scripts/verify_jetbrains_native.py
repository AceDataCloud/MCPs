"""Exercise real compiled native clients against a local fake MCP, never production."""

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import subprocess
import tempfile
import threading

ROOT = Path(__file__).resolve().parents[1]
SERVICES = json.loads((ROOT / "scripts/jetbrains_services.json").read_text())[
    "services"
]

JAVA = r"""import java.net.URI;
public class NativeClientProbe {
 public static void main(String[] args) throws Exception {
  Class<?> c=Class.forName(args[0]);
  Object client=c.getConstructor(URI.class,String.class).newInstance(URI.create(args[1]),"LOCAL_TEST_KEY");
  Class<?> parser=Class.forName("com.google.gson.JsonParser");
  Object parsed=parser.getMethod("parseString",String.class).invoke(null,args[3]);
  Object arguments=parsed.getClass().getMethod("getAsJsonObject").invoke(parsed);
  try { System.out.println(c.getMethod("callTool",String.class,Class.forName("com.google.gson.JsonObject")).invoke(client,args[2],arguments)); }
  catch(java.lang.reflect.InvocationTargetException e) {System.err.println(e.getCause().getMessage()); System.exit(2);}
 }
}"""

PANEL_JAVA = r"""import java.awt.Component;
import java.awt.Container;
import java.lang.reflect.Field;
import javax.swing.*;
public class NativePanelProbe {
 static Object field(Object panel, String name) throws Exception {
  Field f=panel.getClass().getDeclaredField(name); f.setAccessible(true); return f.get(panel);
 }
 static JButton generationButton(Container parent) {
  for (Component child:parent.getComponents()) {
   if (child instanceof JButton b && b.getText().startsWith("Generate ")) return b;
   if (child instanceof Container c) { JButton b=generationButton(c); if (b!=null) return b; }
  }
  return null;
 }
 public static void main(String[] args) throws Exception {
  SwingUtilities.invokeAndWait(() -> {
   try {
    Object panel=Class.forName(args[0]).getConstructor().newInstance();
    JTextField model=(JTextField)field(panel,"model");
    JTextArea prompt=(JTextArea)field(panel,"prompt");
    JLabel status=(JLabel)field(panel,"status");
    JButton generate=generationButton((Container)panel);
    if (generate==null) throw new AssertionError("Generation button missing");
    prompt.setText("Headless validation only; key stays empty");
    for (int i=1;i<args.length;i++) {
     model.setText(args[i]); generate.doClick();
     if (!status.getText().equals("Paste only your raw application API key."))
      throw new AssertionError(args[i]+": "+status.getText());
    }
    model.setText(""); generate.doClick();
    if (!status.getText().contains("enter a model explicitly")) throw new AssertionError("Empty model accepted");
    model.setText(args[1]); prompt.setText(""); generate.doClick();
    if (!status.getText().equals("Enter a prompt.")) throw new AssertionError("Empty prompt accepted");
    panel.getClass().getMethod("dispose").invoke(panel);
    System.out.println((args.length-1)+" model IDs reached the empty-key guard; no request or paid confirmation opened");
   } catch (Exception e) {throw new RuntimeException(e);}
  });
 }
}"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--java", required=True)
    parser.add_argument("--ide-home", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--service",
        action="append",
        choices=[service["alias"] for service in SERVICES],
        help="Verify only these service aliases",
    )
    args = parser.parse_args()
    received = []
    mode = {"status": 200, "sse": False, "tool_error": False, "catalog_text": None}
    image_models = json.loads(
        (ROOT / "scripts/fixtures/published_image_models.json").read_text()
    )["model_ids"]

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def do_POST(self):
            data = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            received.append(
                {
                    "payload": data,
                    "auth": self.headers.get("Authorization"),
                    "session": self.headers.get("Mcp-Session-Id"),
                }
            )
            if data["method"] == "notifications/initialized":
                self.send_response(202)
                self.end_headers()
                return
            if data["method"] == "tools/call" and mode["status"] != 200:
                self.send_response(mode["status"])
                self.end_headers()
                return
            if data["method"] == "initialize":
                result = {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {},
                    "serverInfo": {"name": "local-only", "version": "1"},
                }
            elif data["method"] == "tools/list":
                result = {
                    "tools": [
                        {
                            "name": "nanobanana_generate_image",
                            "inputSchema": {
                                "properties": {"model": {"enum": ["LOCAL_TEST_MODEL"]}}
                            },
                        }
                    ]
                }
            else:
                result = {
                    "content": [
                        {
                            "type": "text",
                            "text": mode["catalog_text"]
                            or '{"task_id":"LOCAL_EXISTING_TASK","status":"pending","model":"gpt-image-LOCAL_TEST"}',
                        }
                    ],
                    "isError": mode["tool_error"],
                }
            reply = json.dumps({"jsonrpc": "2.0", "id": data["id"], "result": result})
            body = ("event: message\ndata: " + reply + "\n\n") if mode["sse"] else reply
            self.send_response(200)
            self.send_header(
                "Content-Type",
                "text/event-stream" if mode["sse"] else "application/json",
            )
            self.send_header("Mcp-Session-Id", "LOCAL_SESSION")
            self.send_header("Content-Length", str(len(body.encode())))
            self.end_headers()
            self.wfile.write(body.encode())

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    endpoint = f"http://127.0.0.1:{server.server_port}/mcp"
    with tempfile.TemporaryDirectory(
        prefix="jetbrains-native-local-test-"
    ) as temporary:
        probe = Path(temporary) / "NativeClientProbe.java"
        probe.write_text(JAVA)
        panel_probe = Path(temporary) / "NativePanelProbe.java"
        panel_probe.write_text(PANEL_JAVA)
        results = []
        for service in SERVICES:
            if args.service and service["alias"] not in args.service:
                continue
            directory = ROOT / service["directory"]
            jar = next((directory / "build/libs").glob("mcp-*-0.1.0.jar"))
            classpath = ":".join(map(str, [jar, *args.ide_home.glob("lib/*.jar")]))
            for sse in [False, True]:
                mode.update(status=200, sse=sse)
                start = len(received)
                p = subprocess.run(
                    [
                        args.java,
                        "-cp",
                        classpath,
                        str(probe),
                        service["package"] + ".AceServiceClient",
                        endpoint,
                        service["model_tool"],
                        "{}",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                requests = received[start:]
                assert p.returncode == 0, p.stderr
                assert len(requests) == 3
                assert all(r["auth"] == "Bearer LOCAL_TEST_KEY" for r in requests)
                assert requests[-1]["session"] == "LOCAL_SESSION"
                assert requests[-1]["payload"]["method"] == (
                    "tools/list"
                    if service["model_tool"].startswith("@schema:")
                    else "tools/call"
                )
                results.append(
                    {
                        "service": service["alias"],
                        "sse": sse,
                        "pass": True,
                        "requests": len(requests),
                    }
                )
            if service["alias"] == "gpt-image":
                catalog_text = (
                    "Available image models:\n\n"
                    + "\n".join(f"- {model}" for model in image_models)
                    + "\n\nChoose an exact ID and check current pricing."
                )
                for sse in [False, True]:
                    mode.update(status=200, sse=sse, catalog_text=catalog_text)
                    start = len(received)
                    p = subprocess.run(
                        [
                            args.java,
                            "-cp",
                            classpath,
                            str(probe),
                            service["package"] + ".AceServiceClient",
                            endpoint,
                            service["model_tool"],
                            "{}",
                        ],
                        capture_output=True,
                        text=True,
                        timeout=30,
                    )
                    assert p.returncode == 0, p.stderr
                    assert p.stdout.strip() == catalog_text, p.stdout
                    assert len(received[start:]) == 3
                    results.append(
                        {
                            "service": service["alias"],
                            "scenario": "complete-image-catalog",
                            "sse": sse,
                            "models": len(image_models),
                            "pass": True,
                        }
                    )
                mode["catalog_text"] = None
                start = len(received)
                p = subprocess.run(
                    [
                        args.java,
                        "-Djava.awt.headless=true",
                        "-cp",
                        classpath,
                        str(panel_probe),
                        service["package"] + ".AceServicePanel",
                        *image_models,
                    ],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                assert p.returncode == 0, p.stderr
                assert len(received) == start
                results.append(
                    {
                        "service": service["alias"],
                        "scenario": "all-models-pass-panel-validation",
                        "models": len(image_models),
                        "requests": 0,
                        "pass": True,
                    }
                )
            mode.update(status=429, sse=False)
            start = len(received)
            # A fake generation reaches only localhost; proves one call and no retry.
            p = subprocess.run(
                [
                    args.java,
                    "-cp",
                    classpath,
                    str(probe),
                    service["package"] + ".AceServiceClient",
                    endpoint,
                    service["generate_tool"],
                    '{"model":"LOCAL_TEST_MODEL","prompt":"local-only test"}',
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )
            assert p.returncode == 2 and "429" in p.stderr
            assert (
                sum(r["payload"]["method"] == "tools/call" for r in received[start:])
                == 1
            )
            results.append(
                {
                    "service": service["alias"],
                    "scenario": "rate-limit-no-retry",
                    "pass": True,
                }
            )
            for status in [401, 403]:
                mode.update(status=status, tool_error=False)
                start = len(received)
                p = subprocess.run(
                    [
                        args.java,
                        "-cp",
                        classpath,
                        str(probe),
                        service["package"] + ".AceServiceClient",
                        endpoint,
                        service["task_tool"],
                        json.dumps({service["task_arg"]: "LOCAL_EXISTING_TASK"}),
                    ],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                assert p.returncode == 2 and str(status) in p.stderr
                assert len(received[start:]) == 3
                results.append(
                    {
                        "service": service["alias"],
                        "scenario": f"http-{status}",
                        "pass": True,
                    }
                )
            mode.update(status=200, sse=True, tool_error=False)
            start = len(received)
            p = subprocess.run(
                [
                    args.java,
                    "-cp",
                    classpath,
                    str(probe),
                    service["package"] + ".AceServiceClient",
                    endpoint,
                    service["task_tool"],
                    json.dumps({service["task_arg"]: "LOCAL_EXISTING_TASK"}),
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )
            assert p.returncode == 0 and "LOCAL_EXISTING_TASK" in p.stdout
            assert received[start:][-1]["payload"]["params"]["arguments"] == {
                service["task_arg"]: "LOCAL_EXISTING_TASK"
            }
            results.append(
                {
                    "service": service["alias"],
                    "scenario": "same-task-query",
                    "pass": True,
                }
            )
            mode.update(status=200, sse=False, tool_error=True)
            p = subprocess.run(
                [
                    args.java,
                    "-cp",
                    classpath,
                    str(probe),
                    service["package"] + ".AceServiceClient",
                    endpoint,
                    service["task_tool"],
                    json.dumps({service["task_arg"]: "LOCAL_EXISTING_TASK"}),
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )
            assert p.returncode == 2
            results.append(
                {
                    "service": service["alias"],
                    "scenario": "tool-error-not-success",
                    "pass": True,
                }
            )
            mode["tool_error"] = False
        args.output.write_text(
            json.dumps(
                {
                    "scope": "compiled native clients against localhost only; no production or billable request",
                    "results": results,
                },
                indent=2,
            )
            + "\n"
        )
        print(f"{len(results)} native MCP transport scenarios passed; localhost only")
    server.shutdown()


if __name__ == "__main__":
    main()
