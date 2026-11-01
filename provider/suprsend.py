from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from suprsend_api import SuprSendError, validate_key


class SuprSendProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        api_key = credentials.get("api_key")
        if not api_key:
            raise ToolProviderCredentialValidationError("API key is required.")
        try:
            validate_key(api_key)
        except SuprSendError as e:
            raise ToolProviderCredentialValidationError(str(e)) from e
