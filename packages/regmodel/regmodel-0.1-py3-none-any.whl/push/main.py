import logging
import argparse

log = logging.getLogger(__name__)


def main(args=None):

    parser = argparse.ArgumentParser(prog='modelreg', description='Command line interface for the modelreg package')
    
    subparsers = parser.add_subparsers(help='Sub-commands')

    from .cmd import add_subcommand_push
    add_subcommand_push(subparsers)

    # from .bye import add_subcommand_bye
    # add_subcommand_bye(subparsers)

    # Parse all command line arguments
    args = parser.parse_args(args)

    # This is not a good way to handle the cases
    # where help should be printed.
    # TODO: there must be a better way?
    if hasattr(args, 'func'):
        # Call the desired subcommand function
        args.func(args)
        return 0
    else:
        parser.print_help()
        return 0

    # log.debug('some debug')
    # log.info('some info')
    # log.warning('some warning')

