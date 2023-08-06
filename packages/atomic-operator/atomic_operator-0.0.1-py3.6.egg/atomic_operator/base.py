import os
import re
import sys
import zipfile
from io import BytesIO
import platform
import subprocess
import requests
from .config import Config
from .utils.logger import LoggingBase


class Base(metaclass=LoggingBase):

    CONFIG = None
    ATOMIC_RED_TEAM_REPO = 'https://github.com/redcanaryco/atomic-red-team/zipball/master/'
    command_map = {
        'command_prompt': {
            'windows': 'C:\\Windows\\System32\\cmd.exe',
            'linux': '/bin/sh',
            'macos': '/bin/sh',
            'default': '/bin/sh'
        },
        'powershell': {
            'windows': 'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe'
        },
        'sh': {
            'linux': '/bin/sh',
            'macos': '/bin/sh'
        },
        'bash': {
            'linux': '/bin/bash',
            'macos': '/bin/bash'
        }
    }

    def clean_output(self, data):
        # Remove Windows CLI garbage
        data = re.sub(r"Microsoft\ Windows\ \[version .+\]\r?\nCopyright.*(\r?\n)+[A-Z]\:.+?\>", "", data.decode("utf-8", "ignore"))
        # formats strings with newline and return characters
        return re.sub(r"(\r?\n)*[A-Z]\:.+?\>", "", data)

    def download_atomic_red_team_repo(self, save_path, **kwargs):
        response = requests.get(Base.ATOMIC_RED_TEAM_REPO, stream=True, **kwargs)
        z = zipfile.ZipFile(BytesIO(response.content))
        z.extractall(save_path)
        return z.namelist()[0]

    def format_config_data(self, config_file):
        return_dict = {}
        if config_file:
            if not os.path.exists(config_file):
                raise Exception('Please provide a config_file path that exists')
            from .atomic.loader import Loader
            config_file = Loader().load_technique(config_file)
            
            if not config_file.get('atomic_tests') and not isinstance(config_file, list):
                raise Exception('Please provide one or more atomic_tests within your config_file')
            for item in config_file['atomic_tests']:
                if item.get('guid') not in return_dict:
                    return_dict[item['guid']] = {}
                if item.get('input_arguments'):
                    for key,val in item['input_arguments'].items():
                        return_dict[item['guid']].update({
                            key: val.get('value')
                        })
        return return_dict

    def get_local_system_platform(self):
        os_name = platform.system().lower()
        if os_name == "darwin":
            return "macos"
        return os_name

    def get_abs_path(self, value):
        return os.path.abspath(os.path.expanduser(os.path.expandvars(value)))

    def show_details(self, value):
        if Base.CONFIG.show_details:
            self.__logger.info(value)

    def prompt_user_for_input(self, title, input_object):
        print(f"""
Inputs for {title}:
    Input Name: {input_object.name}
    Default:     {input_object.default}
    Description: {input_object.description}
""")
        print(f"Please provide a value for {input_object.name} (If blank, default is used):",)
        value = sys.stdin.readline()
        if bool(value):
            return value
        return input_object.default

    def print_process_output(self, command, return_code, output, errors):
        # Output the appropriate outputs if they exist.
        if output or errors:
            if output:
                self.__logger.info("\n\nOutput: {}".format(self.clean_output(output)))
            else:
                self.__logger.warning(f"\n\nCommand: {command} returned exit code {return_code}: \n{self.clean_output(errors)}")
        else:
            self.__logger.info("(No output)")

    def execute_subprocess(self, executor, command, cwd):
        p = subprocess.Popen(
            executor, 
            shell=False, 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, 
            env=os.environ, 
            cwd=cwd
        )
        try:
            outs, errs = p.communicate(
                bytes(command, "utf-8") + b"\n", 
                timeout=Base.CONFIG.command_timeout
            )
            self.print_process_output(command, p.returncode, outs, errs)
            return outs, errs
        except subprocess.TimeoutExpired as e:
            # Display output if it exists.
            if e.output:
                self.__logger.warning(e.output)
            if e.stdout:
                self.__logger.warning(e.stdout)
            if e.stderr:
                self.__logger.warning(e.stderr)
            self.__logger.warning("Command timed out!")

            # Kill the process.
            p.kill()
            return "", ""
