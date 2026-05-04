"""HTTP client for GLM API."""

import contextvars
import json
from typing import Any

import httpx
from loguru import logger

from core.config import settings
from core.exceptions import GlmAPIError, GlmAuthError, GlmError, GlmTimeoutError

# Context variable for per-request API token (used in HTTP/remote mode)
_request_api_token: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "_request_api_token", default=None
)


def set_request_api_token(token: str | None) -> None:
    """Set the API token for the current request context (HTTP mode)."""
    _request_api_token.set(token)


def get_request_api_token() -> str | None:
    """Get the API token from the current request context."""
    return _request_api_token.get()


class GlmClient:
    """Async HTTP client for AceDataCloud GLM API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        """Initialize the GLM API client.

        Args:
            api_token: API token for authentication. If not provided, uses settings.
            base_url: Base URL for the API. If not provided, uses settings.
        """
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

        logger.info(f"GlmClient initialized with base_url: {self.base_url}")
        logger.debug(f"API token configured: {'Yes' if self.api_token else 'No'}")
        logger.debug(f"Request timeout: {self.timeout}s")

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        token = get_request_api_token() or self.api_token
        if not token:
            logger.error("API token not configured!")
            raise GlmAuthError("API token not configured")

        return {
            "accept": "application/json",
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
        }

    def _handle_error_response(self, response: httpx.Response) -> None:
        """Parse API error response and raise the appropriate exception.

        The AceDataCloud API returns errors in the format:
            {"error": {"code": "...", "message": "..."}}
        """
        status = response.status_code
        try:
            body = response.json()
        except Exception:
            body = {}

        error_obj = body.get("error", {})
        code = error_obj.get("code", f"http_{status}")
        message = (
            error_obj.get("message") or body.get("detail") or response.text or f"HTTP {status}"
        )

        logger.error(f"API error {status} [{code}]: {message}")

        if status in (401, 403):
            raise GlmAuthError(message)
        raise GlmAPIError(message=message, code=code, status_code=status)

    async def chat_completions(
        self,
        messages: list[dict[str, Any]],
        model: str,
        n: int | None = None,
        stream: bool | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        response_format: dict[str, Any] | None = None,
        top_p: float | None = None,
        frequency_penalty: float | None = None,
        presence_penalty: float | None = None,
        seed: int | None = None,
        stop: str | list[str] | None = None,
        max_completion_tokens: int | None = None,
        logprobs: bool | None = None,
        top_logprobs: int | None = None,
        stream_options: dict[str, Any] | None = None,
        parallel_tool_calls: bool | None = None,
        user: str | None = None,
        reasoning_effort: str | None = None,
        service_tier: str | None = None,
        store: bool | None = None,
        metadata: dict[str, Any] | None = None,
        logit_bias: dict[str, Any] | None = None,
        modalities: list[str] | None = None,
        audio: dict[str, Any] | None = None,
        prediction: dict[str, Any] | None = None,
        web_search_options: dict[str, Any] | None = None,
        tools: list[dict[str, Any]] | None = None,
        tool_choice: str | dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a GLM chat completion.

        Args:
            messages: Conversation messages (required).
            model: The model to use (required).
            n: How many completions to generate.
            stream: Stream response.
            max_tokens: Max tokens.
            temperature: Sampling temperature (0-2).
            response_format: Response format.
            top_p: Nucleus sampling.
            frequency_penalty: Frequency penalty (-2 to 2).
            presence_penalty: Presence penalty (-2 to 2).
            seed: Random seed.
            stop: Stop sequences.
            max_completion_tokens: Upper bound for completion tokens.
            logprobs: Return log probabilities.
            top_logprobs: Number of most likely tokens to return.
            stream_options: Options for streaming.
            parallel_tool_calls: Enable parallel function calling.
            user: End-user identifier.
            reasoning_effort: Reasoning effort level.
            service_tier: Service tier.
            store: Store output.
            metadata: Key-value pairs.
            logit_bias: Token likelihood modification.
            modalities: Output types.
            audio: Audio output parameters.
            prediction: Static predicted output.
            web_search_options: Web search options.
            tools: Tools the model may call.
            tool_choice: Tool choice.

        Returns:
            API response dictionary.
        """
        payload: dict[str, Any] = {
            "messages": messages,
            "model": model,
        }

        optional_fields = {
            "n": n,
            "stream": stream,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "response_format": response_format,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "seed": seed,
            "stop": stop,
            "max_completion_tokens": max_completion_tokens,
            "logprobs": logprobs,
            "top_logprobs": top_logprobs,
            "stream_options": stream_options,
            "parallel_tool_calls": parallel_tool_calls,
            "user": user,
            "reasoning_effort": reasoning_effort,
            "service_tier": service_tier,
            "store": store,
            "metadata": metadata,
            "logit_bias": logit_bias,
            "modalities": modalities,
            "audio": audio,
            "prediction": prediction,
            "web_search_options": web_search_options,
            "tools": tools,
            "tool_choice": tool_choice,
        }

        for key, value in optional_fields.items():
            if value is not None:
                payload[key] = value

        logger.info(f"Creating GLM chat completion with model: {model}")
        logger.debug(f"Messages count: {len(messages)}")

        url = f"{self.base_url}/glm/chat/completions"

        logger.info(f"POST {url}")
        logger.debug(f"Request payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")

        async with httpx.AsyncClient() as http_client:
            try:
                response = await http_client.post(
                    url,
                    json=payload,
                    headers=self._get_headers(),
                    timeout=self.timeout,
                )

                logger.info(f"Response status: {response.status_code}")

                if response.status_code >= 400:
                    self._handle_error_response(response)

                result = response.json()
                logger.success("Chat completion created successfully!")

                return result  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                logger.error(f"Request timeout after {self.timeout}s: {e}")
                raise GlmTimeoutError(
                    f"Request to /glm/chat/completions timed out after {self.timeout}s"
                ) from e

            except GlmError:
                raise

            except Exception as e:
                logger.error(f"Request error: {e}")
                raise GlmAPIError(message=str(e)) from e


# Global client instance
client = GlmClient()
