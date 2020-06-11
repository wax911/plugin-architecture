import argparse

from engine import PluginEngine
from util import FileSystem


def __description() -> str:
    return "Create your own anime meta data"


def __usage() -> str:
    return "vrv-meta.py --service vrv"


def __init_cli() -> argparse:
    parser = argparse.ArgumentParser(description=__description(), usage=__usage())
    parser.add_argument(
        '-l', '--log', default='DEBUG', help="""
        Specify log level which should use. Default will always be DEBUG, choose between the following options
        CRITICAL, ERROR, WARNING, INFO, DEBUG
        """
    )
    parser.add_argument(
        '-d', '--directory', default=f'{FileSystem.get_plugins_directory()}', help="""
        (Optional) Supply a directory where plugins should be loaded from. The default is ./plugins
        """
    )
    return parser


def __print_program_end() -> None:
    print("-----------------------------------")
    print("End of execution")
    print("-----------------------------------")


def __init_app(parameters: dict) -> None:
    PluginEngine(options=parameters).start()


if __name__ == '__main__':
    __cli_args = __init_cli().parse_args()
    __init_app({
        'log_level': __cli_args.log,
        'directory': __cli_args.directory
    })
