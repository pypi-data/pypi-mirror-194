import os
import subprocess
from pathlib import Path

from colorama import Fore, Style

from core.toolkit import Colored


class Mkdk:

    _DEFAULT_PS_FORMAT = 'table {{.ID}}\t{{.Names}}\t{{.Ports}}\t{{.Image}}'
    _PS_FORMAT = os.environ.get('MKIE_PS_FORMAT', _DEFAULT_PS_FORMAT)

    @classmethod
    def ps(cls, format, pattern):
        format = format or cls._PS_FORMAT
        _cmd = ['docker', 'ps', '--format', format]

        if pattern:
            _cmd.extend(['--filter', f'name={pattern}'])

        subprocess.run(_cmd)

    @classmethod
    def build(cls):
        subprocess.run(['docker-compose', 'build'])

    @classmethod
    def up(cls, project):
        _cmd = ['docker-compose',  'up', '-d']
        if project:
            _cmd.extend(['--project-name', project])

        project_name = project or Path.cwd().name
        color_prefix = Style.RESET_ALL + Fore.BLACK
        prefix = Colored.get_color_prefix(color='LIGHTYELLOW_EX',
                                          color_prefix=color_prefix,
                                          prefix_msg='🐳 Docker ⬆ ',
                                          bottom=True,
                                          bottom_color='LIGHTBLUE_EX',
                                          bottom_prefix=Fore.BLACK,
                                          bottom_msg=project_name)

        print(prefix)
        subprocess.run(_cmd)

    @classmethod
    def down(cls, project):
        _cmd = ['docker-compose',  'down']
        if project:
            _cmd.extend(['--project-name', project])

        project_name = project or Path.cwd().name
        color_prefix = Style.RESET_ALL + Fore.BLACK
        prefix = Colored.get_color_prefix(color='LIGHTGREEN_EX',
                                          color_prefix=color_prefix,
                                          prefix_msg='🐳 Docker ⬇ ',
                                          bottom=True,
                                          bottom_color='LIGHTBLUE_EX',
                                          bottom_prefix=Fore.BLACK,
                                          bottom_msg=project_name)

        print(prefix)
        subprocess.run(_cmd)
