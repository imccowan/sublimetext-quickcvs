import os
import sublime
import sublime_plugin
import threading
import subprocess
import functools
import os.path
import re


class RunBuildCvsCommand(sublime_plugin.WindowCommand):
    # helper
    #  * for setting the build_system
    #  * running build
    #  * and then resetting the build_system to automatic
    def run(self, build_system, build_variant):
        self.window.run_command("set_build_system", {"file": build_system})
        self.window.run_command("build", {"variant": build_variant})
        # Set build_system to *automatic*
        self.window.run_command("set_build_system", {"file": ""})


class QuickCvsCommitBuildTargetCommand(sublime_plugin.WindowCommand):
    def run(self, cmd=None, file_regex="", line_regex="", working_dir="",
            encoding="utf-8", env=None, path="", shell=False):
        if cmd is None:
            cmd = []
        if env is None:
            env = {}
        self.execDict = {
            "path": path,
            "shell": shell,
            "cmd": cmd,
            "file_regex": file_regex,
            "line_regex": line_regex,
            "working_dir": working_dir,
            "encoding": encoding,
            "env": env
        }
        self.window.show_input_panel("Commit message", "", self.on_done, None, None)

    def on_done(self, message):
        self.execDict["cmd"][3] = message
        self.window.run_command('exec', self.execDict)


# generic threading stuff, shamelessly stolen from git plugin

def main_thread(callback, *args, **kwargs):
    # sublime.set_timeout gets used to send things onto the main thread
    # most sublime.[something] calls need to be on the main thread
    sublime.set_timeout(functools.partial(callback, *args, **kwargs), 0)


class QuickCvsCommandThread(threading.Thread):
    def __init__(self, command, on_done, working_dir="", fallback_encoding="", **kwargs):
        threading.Thread.__init__(self)
        self.command = command
        self.on_done = on_done
        self.working_dir = working_dir
        if "stdin" in kwargs:
            self.stdin = kwargs["stdin"]
        else:
            self.stdin = None
        self.kwargs = kwargs

    def run(self):
        try:
            # Ignore directories that no longer exist
            if os.path.isdir(self.working_dir):
                # Per http://bugs.python.org/issue8557 shell=True is required
                # to get $PATH on Windows. Yay portable code.
                shell = os.name == 'nt'
                if self.working_dir != "":
                    os.chdir(self.working_dir)

                output = subprocess.check_output(
                    self.command,
                    stderr=subprocess.STDOUT,
                    stdin=subprocess.PIPE,
                    shell=shell,
                    universal_newlines=True
                )
                main_thread(self.on_done, output, **self.kwargs)

        except subprocess.CalledProcessError as e:
            main_thread(self.on_done, e.returncode)


# A base for all commands
class QuickCvsCommand(object):
    may_change_files = False

    def run_command(self, command, callback=None, show_status=True,
                    filter_empty_args=True, no_save=False, **kwargs):
        if filter_empty_args:
            command = [arg for arg in command if arg]
        if 'working_dir' not in kwargs:
            kwargs['working_dir'] = self.get_working_dir()

        s = sublime.load_settings("QuickCVS.sublime-settings")
        if s.get('cvs_save_first') and self.active_view() and self.active_view().is_dirty() and not no_save:
            self.active_view().run_command('save')

        thread = QuickCvsCommandThread(command, callback, **kwargs)
        thread.start()


def cvs_root(directory):
    retval = False

    if os.path.exists(os.path.join(directory, 'CVS')):
        retval = directory

    return retval


class QuickCvsTextCommand(QuickCvsCommand, sublime_plugin.TextCommand):
    def active_view(self):
        return self.view

    def is_enabled(self):
        # First, is this actually a file on the file system?
        if self.view.file_name() and len(self.view.file_name()) > 0:
            return True
        else:
            return False

    def get_file_name(self):
        return os.path.basename(self.view.file_name())

    def get_relative_file_name(self):
        working_dir = self.get_working_dir()
        file_path = working_dir.replace(cvs_root(working_dir), '')[1:]
        file_name = os.path.join(file_path, self.get_file_name())
        return file_name.replace('\\', '/')  # windows issues

    def get_working_dir(self):
        return os.path.realpath(os.path.dirname(self.view.file_name()))

    def get_window(self):
        # Fun discovery: if you switch tabs while a command is working,
        # self.view.window() is None. (Admittedly this is a consequence
        # of my deciding to do async command processing... but, hey,
        # got to live with that now.)
        # I did try tracking the window used at the start of the command
        # and using it instead of view.window() later, but that results
        # panels on a non-visible window, which is especially useless in
        # the case of the quick panel.
        # So, this is not necessarily ideal, but it does work.
        return self.view.window() or sublime.active_window()


class QuickCvsBranchStatusListener(sublime_plugin.EventListener):
    def on_activated(self, view):
        view.run_command("quick_cvs_branch_status")

    def on_post_save(self, view):
        view.run_command("quick_cvs_branch_status")

    def on_load(self, view):
        view.run_command("quick_cvs_branch_status")


class QuickCvsBranchStatusCommand(QuickCvsTextCommand):
    def run(self, edit):
        s = sublime.load_settings("QuickCVS.sublime-settings")
        if s.get("cvs_statusbar"):
            self.run_command(
                ['cvs', 'status', self.get_file_name()],
                self.branchstatus_done, show_status=False, no_save=True
            )
        else:
            self.view.set_status("cvs-branch", "")
            self.view.set_status("cvs-status", "")

    def branchstatus_done(self, result):
        try:
            lines = result.splitlines()
        except AttributeError:
            self.view.set_status("cvs-branch", "")
            self.view.set_status("cvs-status", "Not in CVS")
            return

        branch = ""
        status = ""

        m = re.compile(r".*?Status:\s+([a-zA-Z -]*)").match(lines[1])
        if m:
            status = m.group(1).strip()
        else:
            # something's wrong
            self.view.set_status("cvs-branch", "")
            self.view.set_status("cvs-status", "")
            return

        m = re.compile(r".*?Sticky Tag:\s+(\S*)").match(lines[7])
        if m:
            branch = m.group(1).strip()

        if branch == "" or branch == "(none)":
            branch = "HEAD"

        self.view.set_status("cvs-branch", "CVS branch: " + branch)
        self.view.set_status("cvs-status", "status: " + status)
