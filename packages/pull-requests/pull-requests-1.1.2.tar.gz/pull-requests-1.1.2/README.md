# pull-requests
⬆️ A command line tool for creating pull requests.

## Requirements

- Python 3.10 or above

## Installation

```
pip install pull-requests
```

## Usage
First of all, you need to have a file in your project root directory called `pr.json`. That file needs
to have the following fields in order to make the program works. See below an example of that file structure:

```json
{
    "username": "YOUR_GITHUB_USERNAME",
    "repository": "YOUR_REPOSITORY_NAME",
    "token": "YOUR_GITHUB_ACCESS_TOKEN"
}
```

That's is everything we need to use the program. Now, on your project root directory, you can the
following command:

```bash
pull-requests --from "HEAD_BRANCH" --to "BASE_BRANCH" --title "Some title" --body "Some optional body text"
```

## License
This project is licensed under the MIT license. See [LICENSE](LICENSE).
