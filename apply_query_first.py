#!/usr/bin/env python3
"""Apply query-first pattern to all API Credential OAuth implementations."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent
PLATFORM_TOKEN_EXEMPTION = "acedatacloud"

OLD_CODE = '''                if not application_id:
                    return None

                cred_resp = await client.post(
                    f"{settings.platform_base_url}/api/v1/credentials/",
                    headers={**headers, "Content-Type": "application/json"},
                    json={
                        "application_id": application_id,
                        "name": "OAuth MCP",
                    },
                )
                if cred_resp.status_code not in (200, 201):
                    logger.error(
                        "Failed to get managed MCP Credential: "
                        f"{cred_resp.status_code} {cred_resp.text[:500]}"
                    )
                    return None
                data = cred_resp.json()
                token = data.get("token") if isinstance(data, dict) else None
                if isinstance(token, str) and token:
                    logger.info(f"Using shared OAuth MCP Credential (id={data.get('id')})")
                    return token
                logger.error("Managed MCP Credential response did not contain a token")'''

NEW_CODE = '''                if not application_id:
                    return None

                # Query for existing shared "OAuth MCP" credential first
                cred_list_resp = await client.get(
                    f"{settings.platform_base_url}/api/v1/credentials/",
                    params={"application_id": application_id, "name": "OAuth MCP"},
                    headers=headers,
                )
                existing_creds = []
                if cred_list_resp.status_code == 200:
                    cred_data = cred_list_resp.json()
                    existing_creds = cred_data.get("items", cred_data.get("results", []))

                # Reuse existing credential if found
                if existing_creds and isinstance(existing_creds, list):
                    data = existing_creds[0]
                    token = data.get("token") if isinstance(data, dict) else None
                    if isinstance(token, str) and token:
                        logger.info(
                            f"Reusing existing OAuth MCP Credential (id={data.get('id')})"
                        )
                        return token

                # Create new credential only if not found
                cred_resp = await client.post(
                    f"{settings.platform_base_url}/api/v1/credentials/",
                    headers={**headers, "Content-Type": "application/json"},
                    json={
                        "application_id": application_id,
                        "name": "OAuth MCP",
                    },
                )
                if cred_resp.status_code not in (200, 201):
                    logger.error(
                        "Failed to create OAuth MCP Credential: "
                        f"{cred_resp.status_code} {cred_resp.text[:500]}"
                    )
                    return None
                data = cred_resp.json()
                token = data.get("token") if isinstance(data, dict) else None
                if isinstance(token, str) and token:
                    logger.info(f"Created new OAuth MCP Credential (id={data.get('id')})")
                    return token
                logger.error("OAuth MCP Credential response did not contain a token")'''


def main():
    updated = []
    for path in sorted(ROOT.glob("*/core/oauth.py")):
        name = path.parts[-3]
        if name == PLATFORM_TOKEN_EXEMPTION:
            continue

        source = path.read_text()
        if "_get_user_credential" not in source:
            continue

        # Skip if already has query-first pattern
        if 'params={"application_id": application_id, "name": "OAuth MCP"}' in source:
            print(f"✓ {name}: already has query-first pattern")
            continue

        if OLD_CODE not in source:
            print(f"✗ {name}: old pattern not found")
            continue

        # Apply transformation
        new_source = source.replace(OLD_CODE, NEW_CODE)
        path.write_text(new_source)
        updated.append(name)
        print(f"✓ {name}: applied query-first pattern")

    print(f"\nUpdated {len(updated)} MCPs: {', '.join(updated)}")


if __name__ == "__main__":
    main()
