"""
    | ┏┓       ┏┓
    ┏━┛┻━━━━━━━┛┻━┓
    ┃      ☃      ┃
    ┃  ┳┛     ┗┳  ┃
    ┃      ┻      ┃
    ┗━┓         ┏━┛
    | ┗┳        ┗━┓
    |  ┃          ┣┓
    |  ┃          ┏┛
    |  ┗┓┓┏━━━━┳┓┏┛
    |   ┃┫┫    ┃┫┫
    |   ┗┻┛    ┗┻┛
    God Bless,Never Bug.
"""
import click
from click_help_colors import HelpColorsCommand, HelpColorsGroup
from importlib_metadata import version

import mkie
from mkie.core.mkdk import Mkdk
from mkie.core.mkgit import MkGit


class Mkie(click.MultiCommand):

    @click.group(
        cls=HelpColorsGroup,
        help_headers_color='yellow',
        help_options_color='green',
        context_settings=dict(help_option_names=['-h', '--help']),
    )
    @click.version_option(version=version('mkie'), prog_name='mkie')
    def cli():
        """
        \b
                      __   _
           ____ ___  / /__(_)__
          / __ `__ \/ //_/ / _ \\
         / / / / / / ,< / /  __/
        /_/ /_/ /_/_/|_/_/\___/

        A useful tool for control clis in terminal.
        """
        pass

    @cli.command()
    @click.option('-i', '--ignore', help='ignore files', multiple=True)
    def gitadd(ignore):
        """ Auto add all files to git and ignore submodules. """
        MkGit.add(ignore=ignore)

    @cli.command()
    def gitfetch():
        """ sort out current branchs. """
        MkGit.fetch()

    @cli.command()
    @click.option('-i',
                  '--ignore',
                  help='ignore submodules',
                  is_flag=False,
                  flag_value='general',
                  multiple=True)
    @click.argument('branch_name', required=True)
    def s(ignore, branch_name):
        """ Swap current branch to target branch. """
        MkGit.swap(ignore=ignore, branch_name=branch_name)

    @cli.command()
    def gitpull():
        """ pull latest update from repo """
        MkGit.pull()

    @cli.command()
    @click.option('-f',
                  '--format',
                  help='pretty print container cols,'
                  'default:".ID.Names.Ports.Image"')
    @click.option('--pattern', help='rg pattern word container name')
    def dps(format, pattern):
        """ list docker containers """
        Mkdk.ps(format=format, pattern=pattern)

    @cli.command()
    def dbu():
        """ build docker container """
        Mkdk.build()

    @cli.command()
    @click.argument('project', required=False)
    def dup(project):
        """ start docker container """
        Mkdk.up(project=project)

    @cli.command()
    @click.argument('project', required=False)
    def dd(project):
        """ start docker container """
        Mkdk.down(project=project)


if __name__ == '__main__':
    Mkie.cli()
