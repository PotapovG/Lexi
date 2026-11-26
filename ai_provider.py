"""Optional OpenAI transport. No calls at import, no SDK/runtime dependency.

Official contracts checked 2026-11-26. No automatic paid retries, arbitrary
base URLs, provider tools, persisted Responses, or audio reference prompting.
"""
from __future__ import annotations
import json
import math
import re
import secrets
import socket
import urllib.error
import urllib.request

TEXT_MODEL = "gpt-6.1-terra"
AUDIO_MODEL = "gpt-transcribe"
MAX_RESPONSE_BYTES = 1024 * 1024
MAX_OUTPUT_TOKENS = 900


class ProviderError(Exception):
    def __init__(self, code, *, usage=None, uncertain=False):
        super().__init__(code)
        self.code, self.usage, self.uncertain = code, usage, uncertain


def _response_usage(response):
    usage = response.get("usage")
    model = response.get("model")
    if isinstance(model,str) and re.fullmatch(r"[A-Za-z0-9_.:-]{1,160}",model):
        usage = dict(usage) if isinstance(usage,dict) else {}
        usage["providerModel"] = model
    return usage


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ProviderError("provider_redirect", uncertain=True)


class OpenAIProvider:
    def __init__(self, key, text_model=TEXT_MODEL, audio_model=AUDIO_MODEL,
                 timeout=30, opener=None):
        self.key = key
        self.text_model, self.audio_model = text_model, audio_model
        self.timeout = max(1, min(60, float(timeout)))
        self.opener = opener or urllib.request.build_opener(_NoRedirect())

    def _post(self, endpoint, data, content_type):
        if not self.key:
            raise ProviderError("ai_unavailable")
        request = urllib.request.Request(
            "https://api.openai.com/v1/" + endpoint, data=data,
            headers={"Authorization": "Bearer " + self.key,
                     "Content-Type": content_type}, method="POST")
        try:
            with self.opener.open(request, timeout=self.timeout) as response:
                raw = response.read(MAX_RESPONSE_BYTES + 1)
                if len(raw) > MAX_RESPONSE_BYTES:
                    raise ProviderError("provider_response_too_large", uncertain=True)
                value = json.loads(raw)
                if not isinstance(value, dict):
                    raise ProviderError("provider_invalid_response", uncertain=True)
                return value
        except urllib.error.HTTPError as error:
            # Do not expose provider response bodies (may echo learner text).
            code = {401: "provider_auth", 403: "provider_access",
                    429: "provider_limit"}.get(error.code, "provider_error")
            raise ProviderError(code, uncertain=error.code >= 500) from None
        except (urllib.error.URLError, TimeoutError, socket.timeout):
            raise ProviderError("provider_timeout", uncertain=True) from None
        except (json.JSONDecodeError, UnicodeError):
            raise ProviderError("provider_invalid_response", uncertain=True) from None

    def text(self, instructions, context, schema):
        payload = {
            "model": self.text_model, "store": False,
            "reasoning": {"effort": "none"},
            "max_output_tokens": MAX_OUTPUT_TOKENS,
            "input": [
                {"role": "developer", "content": instructions},
                {"role": "user", "content": json.dumps(context, ensure_ascii=False)},
            ],
            "text": {"format": {"type": "json_schema", "name": "lexi_feedback",
                                "strict": True, "schema": schema}},
        }
        response = self._post("responses",
                              json.dumps(payload).encode(), "application/json")
        usage = _response_usage(response)
        if response.get("status") != "completed":
            raise ProviderError("provider_incomplete", usage=usage,
                                uncertain=text_cost(usage) is None)
        chunks = []
        for item in response.get("output", []):
            for part in item.get("content", []):
                if part.get("type") == "refusal":
                    raise ProviderError("provider_refusal", usage=usage,
                                        uncertain=text_cost(usage) is None)
                if part.get("type") == "output_text":
                    chunks.append(part.get("text", ""))
        try:
            result = json.loads("".join(chunks))
            if not isinstance(result, dict):
                raise ValueError()
        except (ValueError, TypeError):
            raise ProviderError("provider_invalid_schema", usage=usage,
                                uncertain=text_cost(usage) is None) from None
        return result, usage

    def transcribe(self, audio, mime, extension):
        boundary = "lexi" + secrets.token_hex(16)
        parts = []
        for name, value in (("model", self.audio_model), ("response_format", "json"),
                            ("languages[]", "el")):
            parts.append(("--" + boundary + "\r\nContent-Disposition: form-data; name=\"" +
                          name + "\"\r\n\r\n" + value + "\r\n").encode())
        # No prompt/keywords/reference text: reading recognition is independent.
        parts.append(("--" + boundary +
                      "\r\nContent-Disposition: form-data; name=\"file\"; filename=\"speech." +
                      extension + "\"\r\nContent-Type: " + mime + "\r\n\r\n").encode())
        parts.extend((audio, ("\r\n--" + boundary + "--\r\n").encode()))
        response = self._post("audio/transcriptions", b"".join(parts),
                              "multipart/form-data; boundary=" + boundary)
        text = response.get("text")
        languages = response.get("languages")
        usage = _response_usage(response)
        if not isinstance(text, str) or len(text) > 5000:
            raise ProviderError("recognition_uncertain", usage=usage)
        # Model language metadata is optional; absence is not invented confidence.
        if languages is not None:
            codes = [x.get("code") for x in languages if isinstance(x, dict)]
            if not codes or "el" not in codes:
                raise ProviderError("recognition_uncertain", usage=usage)
        if not text.strip():
            raise ProviderError("recognition_uncertain", usage=usage)
        return {"transcript": text.strip(), "languages": languages,
                "origin": "asr", "edited": False}, usage


def _nonnegative_integer(value):
    return value if type(value) is int and 0 <= value <= 2**53 - 1 else None


def text_cost(usage):
    """Return USD millionths, or None when paid usage cannot be established.

    This parser is deliberately total: an unexpected provider usage shape
    preserves the reservation instead of turning a paid request into zero cost.
    """
    if not isinstance(usage, dict):
        return None
    if set(usage) - {"input_tokens","output_tokens","total_tokens","input_tokens_details",
                     "output_tokens_details","providerModel","type"}:
        return None
    actual_model = usage.get("providerModel")
    if actual_model is not None and (not isinstance(actual_model,str) or not (
            actual_model == TEXT_MODEL or actual_model.startswith(TEXT_MODEL + "-"))):
        return None
    incoming = _nonnegative_integer(usage.get("input_tokens"))
    outgoing = _nonnegative_integer(usage.get("output_tokens"))
    if incoming is None or outgoing is None:
        return None
    details = usage.get("input_tokens_details")
    if details is None:
        details = {}
    if not isinstance(details, dict) or set(details) - {"cached_tokens","cache_write_tokens"}:
        return None
    output_details = usage.get("output_tokens_details")
    if output_details is not None and (
            not isinstance(output_details,dict) or set(output_details) - {"reasoning_tokens"}):
        return None
    cached = _nonnegative_integer(details.get("cached_tokens", 0))
    writes = _nonnegative_integer(details.get("cache_write_tokens", 0))
    if cached is None or writes is None or cached + writes > incoming:
        return None
    # Cache-write duration is not inferred from a missing provider field. Use
    # the highest documented tier (2.5) until billing is reconciled. This is a
    # conservative tariff estimate, not an assertion about the provider invoice.
    # Exact integer arithmetic also avoids malformed-count overflow.
    numerator = 20 * (incoming - cached - writes) + cached + 50 * writes + 100 * outgoing
    return (numerator + 10) // 20


def reserve_text_cost(context_bytes):
    # One UTF-8 byte per token is a conservative cap, not a tokenizer estimate.
    # Covers the highest documented cache-write tier until duration is known.
    return int(context_bytes * 2.5 + MAX_OUTPUT_TOKENS * 5 + 1500)


def audio_cost(seconds):
    """Known duration cost, or None for malformed/non-finite provider usage."""
    if type(seconds) not in (int, float):
        return None
    try:
        if not math.isfinite(seconds) or seconds < 0:
            return None
        amount = seconds * 4500 / 60
        return int(round(amount)) if math.isfinite(amount) else None
    except (TypeError, ValueError, OverflowError):
        return None


def audio_usage_cost(usage):
    if (not isinstance(usage, dict) or usage.get("type") != "duration"
            or set(usage) - {"type","seconds","providerModel"}):
        return None
    actual_model = usage.get("providerModel")
    if actual_model is not None and (not isinstance(actual_model,str) or not (
            actual_model == AUDIO_MODEL or actual_model.startswith(AUDIO_MODEL + "-"))):
        return None
    seconds = usage.get("seconds")
    if type(seconds) not in (int,float) or not 0 <= seconds <= 3600:
        return None
    return audio_cost(seconds)
