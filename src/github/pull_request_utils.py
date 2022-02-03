#!/usr/bin/env python3

# noinspection PyPep8, PyPep8Naming
r"""
|  ___   _  _   _     _       ___   ___    __    _  _   ___    __   _____     _  _   _____   _   _      __
| | _,\ | || | | |   | |     | _ \ | __|  /__\  | || | | __| /' _/ |_   _|   | || | |_   _| | | | |   /' _/
| | v_/ | \/ | | |_  | |_    | v / | _|  | \/ | | \/ | | _|  `._`.   | |     | \/ |   | |   | | | |_  `._`.
| |_|    \__/  |___| |___|   |_|_\ |___|  \_V_\  \__/  |___| |___/   |_|      \__/    |_|   |_| |___| |___/
|

Utilities for the GitHub Pull Request workflow.

Usage:

    python3 pull_request_utils.py <commit_title>
"""

import io
import logging
import os
import platform
import subprocess
import sys


def main(commit_title=None):
    logging.getLogger().setLevel(level=logging.DEBUG)

    logging.debug(f"You are using platform system: {platform.system()}")

    if platform.system() == "linux" or platform == "linux2":
        print("Linux not supported at this time.")
        exit(-1)
        return
    elif platform.system() == "win32":
        print("Windows not supported at this time.")
        exit(-1)
        return

    current_working_dir = os.getcwd()
    logging.debug(f"Current working directory: {current_working_dir}")

    if not Utils.navigate_to_git_root():
        exit(-1)
        return

    if not commit_title:
        commit_title = GitCommand.get_commit_title()

    file_name: str = '.github/pull_request_template.md'

    try:
        template_file = FileUtils.open_template_file(file_name)

        if template_file is not None:
            # Create a temporary file to write the contents of our commit message template.
            tmp_file_name: str = 'tmp_file.txt'
            FileUtils.write_contents_to_tmp_file(template_file, commit_title, tmp_file_name)
            template_file.close()

            GitCommand.amend_commit_with_file(tmp_file_name)

            # Remove the unnecessary temp file.
            os.remove(tmp_file_name)

            # Open the editor (ex: VI), which will pause this program.
            GitCommand.open_editor_to_amend_commit()
    except FileNotFoundError:
        print(f"Template file '{file_name}' does not exist!")


class GitCommand:

    def __init__(self):
        pass

    @staticmethod
    def get_commit_title() -> str:
        """
        Gets the commit message from the current Git HEAD.
        Command Ref: git log -n 1 --pretty=format:%s
        """
        git_commit_message = ["git", "log", "-n", "1", "--pretty=format:%s"]
        process = subprocess.run(git_commit_message, stdout=subprocess.PIPE)
        message = process.stdout.decode('utf-8')
        logging.debug(f"Git commit title = {message}")
        return message

    @staticmethod
    def amend_commit_with_file(tmp_file_name):
        """
        Amends the current commit with the contents of the temp file.
        """
        command = f"git commit --amend --allow-empty -F {tmp_file_name}"
        logging.debug(f"Executing command: {command}")
        p = subprocess.Popen(command, shell=True)
        p.communicate()

    @staticmethod
    def open_editor_to_amend_commit():
        """
        Executes the amend commit command, which opens the terminal editor.
        """
        command = f"git commit --amend"
        logging.debug(f"Executing command: {command}")
        p = subprocess.Popen(command, shell=True)
        p.communicate()


class FileUtils:

    def __init__(self):
        pass

    @staticmethod
    def open_template_file(file_name: str) -> io.TextIOBase:
        # noinspection PyTypeChecker
        text_file: io.TextIOBase = open(file_name, mode='r')
        logging.debug(f"Template text_file = {text_file}")
        return text_file

    @staticmethod
    def write_contents_to_tmp_file(template_file, commit_title, tmp_file_name):
        # Create a temporary 'Commit Message' file.
        commit_msg_file = open(tmp_file_name, mode='w')
        # Write the 'Commit Title' as the first line of the commit message.
        commit_msg_file.write(commit_title)
        commit_msg_file.write('\n\n')

        # Read the contents of the 'Template File'.
        file_lines = list(template_file.read().splitlines(keepends=True))

        for file_line in file_lines[:]:
            # logging.debug(f"Writing content: {file_line}")
            commit_msg_file.write(file_line)

        # Close the file.
        commit_msg_file.close()


class Utils:

    def __init__(self):
        pass

    @staticmethod
    def navigate_to_git_root() -> bool:
        """
        Checks whether the current directory contains a .git directory. If not,
        we climb up a couple levels looking for one.
        :return: True if the current working directory is a Git repository.
        False if a .git directory could not be found.
        """
        dir_climb_count = 0
        continue_dir_traverse = True
        while continue_dir_traverse:
            if not Utils.contains_dir('.git'):
                print(f"Current dir {os.getcwd()} is not a Git repository.")
                # Change directory up one level.
                os.chdir("../")
                dir_climb_count += 1
            else:
                print(f"Current dir {os.getcwd()} is a recognized Git repository.")
                return True

            if dir_climb_count > 3:
                continue_dir_traverse = False

        if not Utils.contains_dir('.git'):
            logging.error('Unable to locate Git repository.')

        return False

    @staticmethod
    def contains_dir(target_dir: str) -> bool:
        """
        Walks the directory and file list in the current working directory, and
        looks for the target dir.
        :param target_dir: The target dir to search for.
        :return: True if the target dir exists in the current working directory.
        """
        for dir_path, dir_names, files in os.walk(os.getcwd()):
            for name in dir_names:
                if name == target_dir:
                    return True

        return False


if __name__ == '__main__':
    # Assume this file is being executed from CLI or Python interpreter
    # The 0th arg is the module filename.
    if sys.argv is not None and len(sys.argv) > 1:
        main(commit_title=str(sys.argv[1]))
    else:
        main()
