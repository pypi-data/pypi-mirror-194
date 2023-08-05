from pathlib import Path
import json
from .exceptions import CredentialFileDoesNotExist, InvalidFormatForCredentialFile
from dataclasses import dataclass


@dataclass
class Credentials:
    username: str
    repository_name: str
    token: str

    def get_token(self) -> str:
        return "Bearer " + self.token


class CredentialManager:
    REQUIRED_CREDENTIAL_FILE_KEYS = {"username", "repository", "token"}

    def __init__(self) -> None:
        self._pr_json_path = Path("pr.json")

    def pr_json_file_exists(self) -> bool:
        return self._pr_json_path.is_file()

    def has_all_required_keys(self, credential_file: dict) -> bool:
        credential_file_keys = set(credential_file.keys())
        return all(
            key in credential_file_keys for key in self.REQUIRED_CREDENTIAL_FILE_KEYS
        )

    def read_credential_file(self) -> Credentials:
        if not self.pr_json_file_exists():
            raise CredentialFileDoesNotExist()

        with open(self._pr_json_path) as file:
            pr_json_file = json.loads(file.read())

            if not self.has_all_required_keys(pr_json_file):
                raise InvalidFormatForCredentialFile()

            return Credentials(
                pr_json_file["username"],
                pr_json_file["repository"],
                pr_json_file["token"],
            )
