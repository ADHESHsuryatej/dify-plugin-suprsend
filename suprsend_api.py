"""SuprSend REST calls. Standard library only; request shapes match the SuprSend Zapier, Make and n8n apps."""

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

BASE_URL = "https://hub.suprsend.com"
TIMEOUT_SECONDS = 30
# Cloudflare in front of hub.suprsend.com rejects urllib's default User-Agent
USER_AGENT = "suprsend-dify-plugin/0.0.1"


class SuprSendError(Exception):
    pass


def call(api_key: str, method: str, path: str, body: Any = None, query: dict[str, str] | None = None) -> Any:
    url = BASE_URL + path
    if query:
        url += "?" + urllib.parse.urlencode(query)
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            raw = response.read()
    except urllib.error.HTTPError as e:
        # Surface SuprSend's message, never the request headers (they hold the key)
        detail = e.read().decode(errors="replace")[:500]
        raise SuprSendError(f"SuprSend API error {e.code}: {detail}") from e
    except urllib.error.URLError as e:
        raise SuprSendError(f"Could not reach SuprSend: {e.reason}") from e
    return json.loads(raw) if raw else {}


def split_list(value: str | None) -> list[str] | None:
    if not value:
        return None
    items = [s.strip() for s in value.split(",") if s.strip()]
    return items or None


def parse_json_object(value: str | None, field: str) -> dict[str, Any]:
    if not value:
        return {}
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as e:
        raise SuprSendError(f"{field} must be valid JSON: {e.msg}") from e
    if not isinstance(parsed, dict):
        raise SuprSendError(f"{field} must be a JSON object, like {{\"key\": \"value\"}}")
    return parsed


def validate_key(api_key: str) -> None:
    call(api_key, "GET", "/v1/subscriber_list/", query={"limit": "1"})


def trigger_workflow(api_key: str, workflow: str, distinct_id: str, data: str | None = None,
                     emails: str | None = None, phones: str | None = None, tenant_id: str | None = None) -> Any:
    recipient: dict[str, Any] = {"distinct_id": distinct_id}
    if email_list := split_list(emails):
        recipient["$email"] = email_list
    if phone_list := split_list(phones):
        recipient["$sms"] = phone_list
    body: dict[str, Any] = {"workflow": workflow, "recipients": [recipient]}
    if payload := parse_json_object(data, "Data"):
        body["data"] = payload
    if tenant_id:
        body["tenant_id"] = tenant_id
    return call(api_key, "POST", "/trigger/", body)


def upsert_user(api_key: str, distinct_id: str, name: str | None = None, emails: str | None = None,
                phones: str | None = None, timezone: str | None = None, properties: str | None = None) -> Any:
    # Custom properties first so the explicit fields always win
    body = parse_json_object(properties, "Custom properties")
    if name:
        body["name"] = name
    if email_list := split_list(emails):
        body["$email"] = email_list
    if phone_list := split_list(phones):
        body["$sms"] = phone_list
    if timezone:
        body["$timezone"] = timezone
    return call(api_key, "POST", f"/v1/user/{urllib.parse.quote(distinct_id, safe='')}/", body)


def update_preference(api_key: str, distinct_id: str, category: str, preference: str,
                      tenant_id: str | None = None) -> Any:
    if preference not in ("opt_in", "opt_out"):
        raise SuprSendError("Preference must be opt_in or opt_out")
    path = (f"/v1/user/{urllib.parse.quote(distinct_id, safe='')}/preference/category/"
            f"{urllib.parse.quote(category, safe='')}/")
    return call(api_key, "PATCH", path, {"preference": preference},
                query={"tenant_id": tenant_id} if tenant_id else None)


def add_user_to_list(api_key: str, list_id: str, distinct_id: str) -> Any:
    path = f"/v1/subscriber_list/{urllib.parse.quote(list_id, safe='')}/subscriber/add/"
    return call(api_key, "POST", path, {"distinct_ids": [distinct_id]})
