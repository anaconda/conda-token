
from __future__ import print_function

import sys
from argparse import ArgumentParser
from packaging import version

from .. import __version__, repo_config
from .utils import condarc_path_args


def main(args):
    if repo_config.CONDA_VERSION < version.parse('4.10.1'):
        print('You must first upgrade to at least Conda version 4.10.1.')
        return 1

    if args.enable and args.disable:
        raise ValueError('Enable and disable cannot both be true')

    if args.enable:
        tokens = repo_config.token_list()
        if repo_config.REPO_URL not in tokens:
            print("You must first activate your subscription with 'conda token set <TOKEN>'")
            return 1
        else:
            repo_config.enable_extra_safety_checks(args.system, args.env, args.file)
            repo_config.clean_index()
            print('Conda package signature verification enabled.')
            return 0

    if args.disable:
        repo_config.disable_extra_safety_checks(args.system, args.env, args.file)
        repo_config.clean_index()
        return 0


def cli(argv=None):
    parser = ArgumentParser('conda-signature-verification', usage='conda signature-verification',
                            description='Configure Conda package signature verification.')

    parser.add_argument(
        '-V', '--version',
        action='version',
        help='Show the conda-signature-verification version number and exit.',
        version="conda-signature-verification %s" % __version__,
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--enable', action='store_true', help='Enable Conda package signature verification.')
    group.add_argument('--disable', action='store_true', help='Disable Conda package signature verification.')

    condarc_path_args(parser)

    parser.set_defaults(func=main)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == '__main__':
    cli(sys.argv[1:])
