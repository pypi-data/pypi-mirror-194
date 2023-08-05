"""
Iris Exception Types
"""
# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #

from typing import Optional


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                Iris Exception Types                                                  #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


class IrisException(Exception):
    """Error raised when occurs an unidentified internal error in the iris package"""

    message = "Iris Command Error"

    def __init__(self, message: Optional[str] = None, details: Optional[str] = None):
        """
        Args:
            message (str): Error message. This will replace the defined class message.
            details (str): Details about the error.
        """
        self.message = self._compose_message(message=message, details=details)
        super().__init__(self.message)

    def __str__(self):
        return self.message

    def _compose_message(
        self, message: Optional[str] = None, details: Optional[str] = None
    ) -> str:
        """Composition of the error message

        Args:
            message (str): Error message. This will replace the defined class message.
            details (str): Details about the error.

        Returns:
            message (str): A message  error with the following format:
                self.message: message - details
        """
        return " - ".join([msg for msg in [message or self.message, details] if msg])


# ────────────────────────────────────────────── BAD REQUEST Exceptions ────────────────────────────────────────────── #


class InvalidLoginError(IrisException):
    """Error raised when the login is invalid"""

    message = "Invalid login credentials. Are you logged in?"


class EndpointNotFoundError(IrisException):
    """Error raised when the endpoint is not found"""

    message = "Endpoint not found: "


class BadRequestError(IrisException):
    """Error raised when there are input data errors"""

    message = "Bad request error. Please check your input data"


class UnprocessableEntityError(IrisException):
    """Error raised when there are input data errors"""

    message = "Unprocessable entity error. Please check your input data"


class DownloadLinkNotFoundError(IrisException):
    """Error raised when the download link is not found"""

    message = "Download link not found"


class NotLoggedInError(IrisException):
    """Error raised when the keyfile is not found, which means that the user is not logged in"""

    message = "Keyfile doesn't exist. User should login"


class InvalidCommandError(IrisException):
    """Error raised when the command is invalid"""

    message = "Invalid command. Please check your command again!"


class DownloadLinkExpiredError(IrisException):
    """Error raised when the download link is expired"""

    message = "This download link is already expired. This expire time is: "


class ArtefactNotFoundError(IrisException):
    """Error raised when attempting to upload a nonexistent artefact"""

    message = "File not found"


class ArtefactTypeInvalidError(IrisException):
    """Error raised when attempting to upload an artefact which is not a folder"""

    message = "Only folders are supported"


class UnsafeTensorsError(IrisException):
    """Error raised when attempting to upload a model (artefact) which does not contain a .safetensors file"""

    message = "Only models safely saved using safetensors are compatible. See https://huggingface.co/docs/safetensors/index"
