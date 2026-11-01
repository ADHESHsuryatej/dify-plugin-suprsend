from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from suprsend_api import add_user_to_list


class AddUserToListTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        result = add_user_to_list(
            self.runtime.credentials["api_key"],
            list_id=tool_parameters["list_id"],
            distinct_id=tool_parameters["distinct_id"],
        )
        yield self.create_json_message(result)
