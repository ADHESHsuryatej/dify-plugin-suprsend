from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from suprsend_api import update_preference


class UpdatePreferenceTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        result = update_preference(
            self.runtime.credentials["api_key"],
            distinct_id=tool_parameters["distinct_id"],
            category=tool_parameters["category"],
            preference=tool_parameters.get("preference") or "opt_in",
            tenant_id=tool_parameters.get("tenant_id"),
        )
        yield self.create_json_message(result)
