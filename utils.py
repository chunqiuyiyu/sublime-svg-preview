"""
Utility functions for current plugin
"""

import os
import tempfile

import sublime

TMP_DIR = os.path.join(tempfile.gettempdir(), 'sublime-svg-preview')
PLUGIN_NAME = 'Sublime SVG Preview'


def keep_tmp_pool():
    """
    Delete oldest file in tmp directory when files have exceed
    """
    if bool(len(os.listdir(TMP_DIR)) > 20):
        # We only keep 10 SVG files in tmp directory, So max size is 20
        # (10 original SVG files and 10 automatically generated PNG files)

        all_files = os.listdir(TMP_DIR)

        file_mtimes = [
            os.stat(os.path.join(TMP_DIR, name)).st_mtime for name in all_files
        ]
        index = file_mtimes.index(min(file_mtimes))
        oldest_file = all_files[index]
        print(oldest_file)

        os.remove(os.path.join(TMP_DIR, oldest_file))


def active_console(err_msg, cmd):
    """
    Active console panel when some errors occurs.
    """
    msg = '{}: {}\nRun `{}` in your bash for information.'.format(
        PLUGIN_NAME, err_msg, cmd)

    sublime.active_window().run_command("show_panel", {"panel": "console"})
    raise Exception(msg)


def run_cmd(cmd, msg):
    """
    Run custom command and deal with std errors
    """
    stdout = os.popen(cmd)

    result = stdout.buffer.read().decode(encoding='utf8')
    stderr = stdout.close()
    return result if not stderr else active_console(msg, cmd)


def get_origin_name(path):
    """
    Getting the name of the file without the extension
    """
    return os.path.splitext(path)[0]
