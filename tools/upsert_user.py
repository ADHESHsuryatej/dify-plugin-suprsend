from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from suprsend_api import upsert_user


class UpsertUserTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        result = upsert_user(
            self.runtime.credentials["api_key"],
            distinct_id=tool_parameters["distinct_id"],
            name=tool_parameters.get("name"),
            emails=tool_parameters.get("emails"),
            phones=tool_parameters.get("phones"),
            timezone=tool_parameters.get("timezone"),
            properties=tool_parameters.get("properties"),
        )
        yield self.create_json_message(result)
