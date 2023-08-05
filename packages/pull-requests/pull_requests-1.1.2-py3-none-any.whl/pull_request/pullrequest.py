from dataclasses import dataclass
import requests
from .credential_manager import Credentials


@dataclass
class PullRequestData:
    title: str | None
    body: str | None
    head_branch: str
    base_branch: str


class PullRequest:
    def __init__(self, credentials: Credentials, pr_content: PullRequestData) -> None:
        self.credentials = credentials
        self.pr_content = pr_content

    def get_headers(self) -> dict:
        token = self.credentials.get_token()
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": token,
            "Content-Type": "application/json",
        }
        return headers

    def get_body(self) -> dict:
        body = {
            "title": self.pr_content.title
            if self.pr_content.title is not None
            else self.pr_content.head_branch,
            "base": self.pr_content.base_branch,
            "head": f"{self.credentials.username}:{self.pr_content.head_branch}",
            "body": self.pr_content.body if self.pr_content.body is not None else "",
        }
        return body

    def get_endpoint_url(self) -> str:
        return f"https://api.github.com/repos/{self.credentials.username}/{self.credentials.repository_name}/pulls"

    def handle_http_response(self, response: requests.Response) -> None:
        match response.status_code:
            case 201:
                print(
                    f"Pull request from '{self.pr_content.head_branch}' to '{self.pr_content.base_branch}' was successfully made"
                )
            case (403 | 422):
                print(
                    "Error: This command is probably being spammed. There is probably a pull request for this branch"
                )
            case _:
                print("Unexpected behavior")
                print(
                    f"STATUS CODE: {response.status_code}\nRESPONSE BODY: {response.json()}"
                )

    async def make_pull_request(self):
        headers = self.get_headers()
        body = self.get_body()
        url = self.get_endpoint_url()
        response = requests.post(url, headers=headers, json=body)
        self.handle_http_response(response)
