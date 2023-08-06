# -*- coding: utf-8 -*-

"""Pashword command-line interface.

This module allows the user to launch the main features of the package
from a command-line interface.
"""

from argparse import ArgumentParser, SUPPRESS
from sys import exit, stderr

from pashword import config
from pashword._version import version
from pashword.main import read, sort

def main():
    """Run the command-line interpreter."""
    parser = ArgumentParser(
        prog=__package__,
        description=__doc__,
    )
    parser.add_argument('-v', '--version',
        action='version',
        version=f'%(prog)s {version}',
    )
    parser.add_argument('-c', '--config',
        help='custom configuration file path',
        metavar='path',
    )
    subparsers = parser.add_subparsers(
        required=True,
        help="name of the command to run",
    )
    for module in (read, sort):
        subparser = subparsers.add_parser(
            name=module.__name__.split('.')[-1],
            help=f'run {module.__name__} module',
            argument_default=SUPPRESS,
        )
        module.setup(subparser)
    args = parser.parse_args()
    try:
        if args.config:
            with open(args.config) as file:
                config.read_file(file)
        args.func(**vars(args))
    except Exception as exception:
        print(exception, file=stderr)
        exit(1)
    except SystemExit as exception:
        print("program exited")
        exit(0)

if __name__ == '__main__':
    main()
