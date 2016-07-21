import sublime
import sublime_plugin
import os.path
import platform


def compare_file_names(x, y):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        return x.lower() == y.lower()
    else:
        return x == y


class MySwitchFileCommand(sublime_plugin.WindowCommand):
    def run(self, extensions=[]):
        if not self.window.active_view():
            return

        fname = self.window.active_view().file_name()
        if not fname:
            return

        pData = sublime.active_window().project_data()
        if pData is not None:
            file = ProjectSearch(pData, fname, extensions)
        else:
            file = DefaultSearch(fname, extensions)

        if file is not None:
            OpenFile(file)


def SearchFolder(searchFolder, fname, extensions):
    ext = ExtractSearchExtensions(extensions, fname)
    base, _ = os.path.splitext(fname)
    filename = os.path.basename(base)

    for root, dirs, files in os.walk(searchFolder):
        for e in ext:
            newFile = root + "\\" + filename + "." + e
            if os.path.exists(newFile):
                return newFile

    return None


def ExtractSearchExtensions(extensions, fname):
    base, ext = os.path.splitext(fname)
    ext = ext[1:]
    return [e for e in extensions if e != ext]


def ProjectSearch(projectData, fname, extensions):
    paths = [f["path"] for f in projectData["folders"]]
    for p in paths:
        match = SearchFolder(p, fname, extensions)
        if match is not None:
            return match

    return None


def DefaultSearch(fname, extensions):
    base = os.path.dirname(fname)
    return SearchFolder(base, fname, extensions)


def OpenFile(fname):
    windows = sublime.windows()
    for w in windows:
        view = w.find_open_file(fname)
        if view is not None:
            w.focus_view(view)
            if w != sublime.active_window():
                # Hack to get focus on other window
                # https://github.com/SublimeTextIssues/Core/issues/444
                w.run_command("focus_neighboring_group")
                w.focus_view(view)

    sublime.active_window().open_file(fname)
