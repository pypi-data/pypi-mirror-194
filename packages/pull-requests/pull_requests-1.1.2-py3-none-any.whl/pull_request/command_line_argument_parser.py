from argparse import ArgumentParser


class CommandLineArgumentParser:
    def __init__(self) -> None:
        self._parser = ArgumentParser(
            description="Pull requests on command line - Author: Icarus"
        )
        self.add_commands()

    @property
    def parser(self) -> ArgumentParser:
        return self._parser

    def add_commands(self) -> None:
        self.parser.add_argument(
            "-f", "--from", help="Changes are coming from this branch", required=True
        )
        self.parser.add_argument(
            "-t", "--to", help="Changes are going to that branch", required=True
        )
        self.parser.add_argument(
            "-T", "--title", help="Title of pull request",
        )
        self.parser.add_argument("-b", "--body", help="Body of the pull request")

    def parse_args(self) -> dict:
        args = self.parser.parse_args()
        return vars(args)
