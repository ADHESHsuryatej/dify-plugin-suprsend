from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from suprsend_api import trigger_workflow


class TriggerWorkflowTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        result = trigger_workflow(
            self.runtime.credentials["api_key"],
            workflow=tool_parameters["workflow"],
            distinct_id=tool_parameters["distinct_id"],
            data=tool_parameters.get("data"),
            emails=tool_parameters.get("emails"),
            phones=tool_parameters.get("phones"),
            tenant_id=tool_parameters.get("tenant_id"),
        )
        yield self.create_json_message(result)
