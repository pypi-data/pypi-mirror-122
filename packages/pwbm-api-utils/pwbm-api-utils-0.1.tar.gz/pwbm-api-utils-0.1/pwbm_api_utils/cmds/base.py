import abc
import argparse
from typing import Union


class CommandBase(abc.ABC):
    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Name of the command in the CLI."""

    @property
    @abc.abstractmethod
    def description(self) -> str:
        """Description of the command, displayed in the command help."""

    @property
    @abc.abstractmethod
    def help(self) -> str:
        """Short description of the command, displayed in the command list help."""

    @classmethod
    def register_subparser(cls, subparsers: argparse._SubParsersAction):
        cmd_subparser = subparsers.add_parser(
            name=cls.name,
            description=cls.description,
            help=cls.help,
        )
        cmd_subparser.set_defaults(cmd_callable=cls.run)
        cls.configure_cli(cmd_subparser)

    @classmethod
    def configure_cli(cls, parser: argparse.ArgumentParser):
        """Configure CLI arguments of the command"""
        pass

    @classmethod
    @abc.abstractmethod
    def run(cls, args: argparse.Namespace) -> Union[int, str]:
        """Command logic."""
