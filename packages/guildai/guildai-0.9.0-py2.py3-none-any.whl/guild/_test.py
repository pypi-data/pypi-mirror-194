# Copyright 2017-2022 RStudio, PBC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import codecs
import doctest
import fnmatch
import glob
import errno
import filecmp
import json
import os
import platform
import pprint
import queue
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time

import yaml

import guild

from guild import _api as gapi
from guild import ansi_util
from guild import cli
from guild import config as configlib
from guild import file_util
from guild import guildfile
from guild import init
from guild import op_util
from guild import run as runlib
from guild import util
from guild import yaml_util

PLATFORM = platform.system()

TEST_NAME_WIDTH = 27

FIXME = doctest.register_optionflag("FIXME")
FIXME_CI = doctest.register_optionflag("FIXME_CI")
FIXME_WINDOWS = doctest.register_optionflag("FIXME_WINDOWS")
GIT_LS_FILES_TARGET = doctest.register_optionflag("GIT_LS_FILES_TARGET")
KEEP_LF = doctest.register_optionflag("KEEP_LF")
MACOS = doctest.register_optionflag("MACOS")
NORMALIZE_PATHS = doctest.register_optionflag("NORMALIZE_PATHS")
NORMALIZE_PATHSEP = doctest.register_optionflag("NORMALIZE_PATHSEP")
TIMING_CRITICAL = doctest.register_optionflag("TIMING_CRITICAL")
PY3 = doctest.register_optionflag("PY3")
PY310 = doctest.register_optionflag("PY310")
PY311 = doctest.register_optionflag("PY311")
PY37 = doctest.register_optionflag("PY37")
PY38 = doctest.register_optionflag("PY38")
PY39 = doctest.register_optionflag("PY39")
STRICT = doctest.register_optionflag("STRICT")
STRIP_ANSI_FMT = doctest.register_optionflag("STRIP_ANSI_FMT")
STRIP_EXIT_0 = doctest.register_optionflag("STRIP_EXIT_0")
WINDOWS = doctest.register_optionflag("WINDOWS")
WINDOWS_ONLY = doctest.register_optionflag("WINDOWS_ONLY")

DEFAULT_TIMING_MIN_CPUS = 4


def run_all(skip=None, fail_fast=False, force=False, concurrency=None):
    return run(
        all_tests(),
        skip=skip,
        fail_fast=fail_fast,
        concurrency=concurrency,
        force=force,
    )


def all_tests():
    test_pattern = os.path.join(tests_dir(), "*.md")
    return sorted([_test_name_for_path(path) for path in glob.glob(test_pattern)])


def tests_dir():
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), "tests")


def _test_name_for_path(path):
    name, _ext = os.path.splitext(os.path.basename(path))
    return name


def run(tests, skip=None, fail_fast=False, force=False, concurrency=None):
    if concurrency and concurrency > 1:
        return _run_parallel(tests, skip, fail_fast, force, concurrency)
    return _run_(tests, skip, fail_fast, force)


def _run_(tests, skip, fail_fast, force):
    skip = skip or []
    success = True
    for test in tests:
        if test not in skip:
            run_success = _run_test(test, fail_fast, force)
            success &= run_success
        else:
            sys.stdout.write(_test_skipped_output(test))
    return success


def _test_skipped_output(test):
    return f"  {test}:{' ' * (TEST_NAME_WIDTH - len(test))} skipped\n"


def _run_test(name, fail_fast, force):
    sys.stdout.write(f"  {name}: ")
    sys.stdout.flush()
    filename = _filename_for_test(name)
    if not os.path.exists(filename):
        _log_test_not_found(name)
        return False
    if (
        not force
        and os.getenv("FORCE_TEST") != "1"
        and front_matter_skip_test(filename)
    ):
        _log_skipped_test(name)
        return True
    try:
        failures, _tests = run_test_file(filename, fail_fast=fail_fast)
    except IOError:
        _log_test_not_found(name)
        return False
    except RuntimeError as e:
        _log_general_error(name, str(e))
        return False
    else:
        if not failures:
            _log_test_ok(name)
        return failures == 0


def _filename_for_test(name_or_path):
    if os.path.sep in name_or_path or "." in name_or_path:
        return os.path.abspath(name_or_path)
    return _named_test_filename(name_or_path)


def _named_test_filename(name):
    return _resolve_relative_test_filename(os.path.join("tests", name + ".md"))


def _resolve_relative_test_filename(filename):
    if os.path.isabs(filename):
        return filename
    package = doctest._normalize_module(None, 3)
    return doctest._module_relative_path(package, filename)


def front_matter_skip_test(filename):
    filename = _resolve_relative_test_filename(filename)
    fm = yaml_util.yaml_front_matter(filename)
    options = _parse_doctest_options(fm.get("doctest"), filename)
    return options and _skip_for_doctest_options(options) is True


def _parse_doctest_options(encoded_options, filename):
    if not encoded_options:
        return {}
    parser = doctest.DocTestParser()
    parser._OPTION_DIRECTIVE_RE = re.compile(r"([^\n'\"]*)$", re.MULTILINE)
    return parser._find_options(encoded_options, filename, 1)


def _skip_for_doctest_options(options):
    return (
        _skip_fixme(options)
        or _skip_platform(options)
        or _skip_python_version(options)
        or _skip_timing_critical(options)
        or _skip_git_ls_files_target(options)
    )


def _skip_platform(options):
    is_windows = PLATFORM == "Windows"
    is_macos = PLATFORM == "Darwin"
    if options.get(WINDOWS) is False and is_windows:
        return True
    if options.get(WINDOWS_ONLY) is True and not is_windows:
        return True
    if options.get(MACOS) is False and is_macos:
        return True
    return None


def _skip_python_version(options):
    py_major_ver = sys.version_info[0]
    py_minor_ver = sys.version_info[1]
    skip = None
    # All Python 3 targets are enabled by default - check if
    # explicitly disabled
    if options.get(PY3) is False and py_major_ver == 3:
        skip = True
    # Force tests on/off if more specific Python versions specified.
    for opt, maj_ver, min_ver in [
        (options.get(PY37), 3, 7),
        (options.get(PY38), 3, 8),
        (options.get(PY39), 3, 9),
        (options.get(PY310), 3, 10),
        (options.get(PY311), 3, 11),
    ]:
        if opt in (True, False) and py_major_ver == maj_ver and py_minor_ver == min_ver:
            skip = not opt
    return skip


def _skip_fixme(options):
    return (
        options.get(FIXME) is True
        or (options.get(FIXME_CI) is True and _running_under_ci())
        or (options.get(FIXME_WINDOWS) is True and PLATFORM == "Windows")
    )


def _running_under_ci():
    return os.getenv("GUILD_CI") == "1"


def _skip_timing_critical(options):
    """Skips tests that rely on a performant system to test timings.

    Performance threshold is measured by CPU cores, as returned by
    `os.cpu_count()`. The minimum number of cores for a performant
    system can be configured using the environment variable
    `TIMING_MIN_CPUS`.
    """
    opt = options.get(TIMING_CRITICAL)
    if opt is None:
        return False
    return opt != _is_performant_system()


def _is_performant_system():
    min_cpus = util.get_env("TIMING_MIN_CPUS", int, DEFAULT_TIMING_MIN_CPUS)
    return os.cpu_count() >= min_cpus


def _skip_git_ls_files_target(options):
    """Skips test if system Git does not support ls-files target behavior.

    Earlier versions of Git do no support a behavior that Guild relies
    on for source code detection optimization. Tests that exerise this
    behavior can use the option `GIT_LS_FILES_TARGET` to skip tests
    that don't apply to the current version of Git.
    """
    opt = options.get(GIT_LS_FILES_TARGET)
    if opt is None:
        return False
    return opt != _git_ls_files_is_target()


def _git_ls_files_is_target():
    from guild import vcs_util

    return vcs_util.git_version() >= vcs_util.GIT_LS_FILES_TARGET_VER


def _log_skipped_test(name):
    sys.stdout.write(" " * (TEST_NAME_WIDTH - len(name)))
    if os.getenv("NO_SKIPPED_MSG") == "1":
        sys.stdout.write("ok\n")
    else:
        sys.stdout.write("ok (skipped)\n")
    sys.stdout.flush()


def _log_test_not_found(name):
    sys.stdout.write(" " * (TEST_NAME_WIDTH - len(name)))
    sys.stdout.write(cli.style("TEST NOT FOUND\n", fg="red"))
    sys.stdout.flush()


def _log_test_ok(name):
    sys.stdout.write(" " * (TEST_NAME_WIDTH - len(name)))
    sys.stdout.write("ok\n")
    sys.stdout.flush()


def _log_general_error(name, error):
    sys.stdout.write(" " * (TEST_NAME_WIDTH - len(name)))
    sys.stdout.write(cli.style(f"ERROR ({error})\n", fg="red"))
    sys.stdout.flush()


def run_test_file(filename, globs=None, fail_fast=False):
    filename = _resolve_relative_test_filename(filename)
    globs = globs or test_globals()
    return run_test_file_with_config(
        filename,
        globs=globs,
        optionflags=(
            _fail_fast_flag(fail_fast)
            | _report_first_flag()
            | doctest.ELLIPSIS
            | doctest.NORMALIZE_WHITESPACE
            | NORMALIZE_PATHS
            | WINDOWS
            | STRIP_ANSI_FMT
            | STRIP_EXIT_0
        ),
    )


def _fail_fast_flag(fail_fast):
    if fail_fast:
        return doctest.FAIL_FAST
    return 0


def _report_first_flag():
    if os.getenv("REPORT_ONLY_FIRST_FAILURE") == "1":
        return doctest.REPORT_ONLY_FIRST_FAILURE
    return 0


class Checker(doctest.OutputChecker):
    """Guild test checker

    Transforms got and want for tests based:

    - Remove ANSI formatting (disable with `-STRIP_ANSI_FMT`
    - Normalizes paths on Windows (disable with `-NORMALIZE_PATHS`
    - Support 'leading wildcard' of "???" as "..." is treated as block
      continuation

    Optional transforms, enabled with `+<option>`:

    - `+NORMALIZE_PATHSEP` - Replace '::' with with platform specific
      path sep char

    All transforms including ELLIPSIS support are disabled with
    `+STRICT`.

    Default doctest checker options enabled by default:

    - doctest.ELLIPSIS
    - doctest.NORMALIZE_WHITESPACE

    The option `doctest.REPORT_ONLY_FIRST_FAILURE` may be enabled
    globally for tests by setting the `REPORT_ONLY_FIRST_FAILURE`
    environment variable to `1`.

    """

    def check_output(self, want, got, optionflags):
        if optionflags & STRICT:
            optionflags -= optionflags & doctest.ELLIPSIS
        else:
            got = self._got(got, optionflags)
            want = self._want(want, optionflags)
        return doctest.OutputChecker.check_output(self, want, got, optionflags)

    def _got(self, got, optionflags):
        if optionflags & STRICT:
            return got
        if PLATFORM == "Windows" and optionflags & NORMALIZE_PATHS:
            got = _windows_normalize_paths(got)
        if optionflags & STRIP_ANSI_FMT:
            got = ansi_util.strip_ansi_format(got)
        if optionflags & STRIP_EXIT_0:
            got = _strip_exit_0(got)
        return got

    def _want(self, want, optionflags):
        if optionflags & STRICT:
            return want
        if optionflags & NORMALIZE_PATHSEP:
            want = _normalize_pathsep(want)
        want = _leading_wildcard_want(want)
        if optionflags & STRIP_EXIT_0:
            want = _strip_exit_0(want)
        return want


def _strip_exit_0(s):
    """Removes trailing '\n<exit 0>' from s.

    Use to optionally omit `<exit 0>` at the end of run output that is
    expected to succed.
    """
    if s.endswith("\n<exit 0>\n"):
        return s[:-9]
    return s


def _windows_normalize_paths(s):
    return re.sub(r"[c-zC-Z]:\\\\?|\\\\?", "/", s)


def _normalize_pathsep(s):
    return s.replace("::", os.path.pathsep)


def _leading_wildcard_want(want):
    # Treat leading "???" like "..." (work around for "..." as code
    # continuation token in doctest)
    return re.sub(r"^\?\?\?", "...", want)


class TestRunner(doctest.DocTestRunner):
    def __init__(self, checker=None, verbose=None, optionflags=0):
        super().__init__(checker, verbose, optionflags)
        self.skipped = 0

    def run(self, test, compileflags=None, out=None, clear_globs=True):
        self._apply_skip(test)
        super().run(test, compileflags, out, clear_globs)

    @staticmethod
    def _apply_skip(test):
        for example in test.examples:
            skip = _skip_for_doctest_options(example.options)
            if skip is not None:
                example.options[doctest.SKIP] = skip


def run_test_file_with_config(filename, globs, optionflags):
    test_dir = os.path.dirname(filename)
    with _safe_chdir(test_dir):
        return _run_test_file_with_config(filename, globs, optionflags)


def _safe_chdir(dir):
    if not os.path.exists(dir):

        class NoOp:
            def __enter__(self):
                pass

            def __exit__(self, *_args):
                pass

        return NoOp()

    return util.Chdir(dir)


def _run_test_file_with_config(filename, globs, optionflags):
    """Modified from doctest.py to use custom checker."""
    fm = yaml_util.yaml_front_matter(filename)
    doctest_type = fm.get("doctest-type", "python")
    if doctest_type == "python":
        return _run_python_doctest(filename, globs, optionflags)
    if doctest_type == "bash":
        return _run_bash_doctest(filename, globs, optionflags)
    raise RuntimeError(f"unsupported doctest type '{doctest_type}'")


def _run_python_doctest(filename, globs, optionflags):
    return _gen_run_doctest(filename, globs, optionflags)


def _gen_run_doctest(filename, globs, optionflags, parser=None, checker=None):
    parser = parser or doctest.DocTestParser()
    text, filename = _load_testfile(filename)
    name = os.path.basename(filename)
    if globs is None:
        globs = {}
    else:
        globs = globs.copy()
    if "__name__" not in globs:
        globs["__name__"] = "__main__"
    checker = checker or Checker()
    runner = TestRunner(checker=checker, verbose=None, optionflags=optionflags)
    try:
        test = parser.get_doctest(text, globs, name, filename, 0)
    except ValueError as e:
        return _handle_doctest_value_error(e, name, filename)
    else:
        runner.run(test)
        results = runner.summarize()
        if doctest.master is None:
            doctest.master = runner
        else:
            doctest.master.merge(runner)
        return results


def _handle_doctest_value_error(e, name, filename):
    print("*" * 70)
    m = re.match(r"line (\d+) of the doctest for", str(e))
    if m:
        print(f"File \"{filename}\", line {m.group(1)}, in {name}")
    print(e)
    print("*" * 70)
    return 1, []


class BashDocTestParser(doctest.DocTestParser):
    """Hacked DocTestParser to support running bash commands.

    Uses `$` as the prompt and `>` as a continuation char.

    Wraps examples in `run("<example>")` to run them as shell
    commands.
    """

    _EXAMPLE_RE = re.compile(
        r"""
        # Source consists of a PS1 line followed by zero or more PS2 lines.
        (?P<source>
            (?:^(?P<indent> [ ]{4}) \$    .*) # PS1 line
            (?:\n           [ ]{4}  > .*)*)   # PS2 lines
        \n?
        # Want consists of any non-blank lines that do not start with PS1.
        (?P<want> (?:(?![ ]*$)    # Not a blank line
                     (?![ ]*>>>)  # Not a line starting with PS1
                     .+$\n?       # But any other line
                  )*)
        """,
        re.MULTILINE | re.VERBOSE,
    )

    def _parse_example(self, m, name, lineno):
        indent = len(m.group("indent"))

        source_lines = m.group("source").split("\n")
        _check_prompt_blank(source_lines, indent, name, lineno)
        self._check_prefix(source_lines[1:], " " * indent + ">", name, lineno)
        source = "\n".join([sl[indent + 2 :] for sl in source_lines])

        want = m.group("want")
        want_lines = want.split("\n")
        if len(want_lines) > 1 and re.match(r" *$", want_lines[-1]):
            del want_lines[-1]  # forget final newline & spaces after it
        self._check_prefix(want_lines, " " * indent, name, lineno + len(source_lines))
        want = "\n".join([wl[indent:] for wl in want_lines])

        m = self._EXCEPTION_RE.match(want)
        if m:
            exc_msg = m.group("msg")
        else:
            exc_msg = None
        options = self._find_options(source, name, lineno)
        return _wrap_bash(source, options), options, want, exc_msg


def _wrap_bash(source, options):
    if source.startswith("cd "):
        return _cd_from_bash(source)
    if source.startswith("export "):
        return _set_bash_env_from_bash(source)
    if source.startswith("unset "):
        return _unset_bash_env_from_bash(source)
    if not options.get(KEEP_LF):
        source = source.replace("\n", " ")
    return _run_from_bash(source)


def _cd_from_bash(source):
    assert source.startswith("cd ")
    return f"cd(\"{source[3:]}\")"


def _set_bash_env_from_bash(source):
    assert source.startswith("export ")
    parts = source[7:].split("=", 1)
    assert len(parts) == 2, source
    env_name, env_val = parts
    return f"_bash_env[\"{env_name}\"] = \"{env_val}\""


def _unset_bash_env_from_bash(source):
    assert source.startswith("unset ")
    return f"_ = _bash_env.pop(\"{source[6:]}\", None)"


def _run_from_bash(source):
    source = source.replace("\"", "\\\"")
    return f"run(\"\"\"{source}\"\"\", env=_bash_env)"


def _check_prompt_blank(lines, indent, name, lineno, *_):
    for i, line in enumerate(lines):
        if len(line) >= indent + 2 and line[indent + 1] != " ":
            raise ValueError(
                f"line {lineno + i + 1} of the docstring for {name} "
                f"lacks blank after {line[indent : indent + 1]}: {line!r}"
            )


class BashDocTestChecker(doctest.OutputChecker):
    def check_output(self, want, got, optionflags):
        got = self._normalize_exit_0(want, got)
        want = _leading_wildcard_want(want)
        return doctest.OutputChecker.check_output(self, want, got, optionflags)

    @staticmethod
    def _normalize_exit_0(want, got):
        want = want.rstrip()
        got = got.rstrip()
        if got.endswith("\n<exit 0>") and not want.endswith("\n<exit 0>"):
            return got[:-9]
        if got == "<exit 0>" and want == "":
            return ""
        return got


def _run_bash_doctest(filename, globs, optionflags):
    parser = BashDocTestParser()
    checker = BashDocTestChecker()
    return _gen_run_doctest(filename, globs, optionflags, parser, checker)


def _load_testfile(filename):
    # Copied from Python 3.6 doctest._load_testfile to ensure utf-8
    # encoding on Python 2.
    package = doctest._normalize_module(None, 3)
    if getattr(package, "__loader__", None) is not None:
        if hasattr(package.__loader__, "get_data"):
            file_contents = package.__loader__.get_data(filename)
            file_contents = file_contents.decode("utf-8")
            # get_data() opens files as "rb", so one must do the equivalent
            # conversion as universal newlines would do.
            return file_contents.replace(os.linesep, "\n"), filename
    with codecs.open(filename, encoding="utf-8") as f:
        return f.read(), filename


def test_globals():
    return {
        "_dir": _py_dir,
        "_bash_env": {},
        "PLATFORM": PLATFORM,
        "Chdir": util.Chdir,
        "Env": util.Env,
        "Ignore": _Ignore,
        "LogCapture": util.LogCapture,
        "ModelPath": ModelPath,
        "Platform": _Platform,
        "PrintStderr": PrintStderr,
        "Project": Project,
        "Proxy": Proxy,
        "RunError": gapi.RunError,
        "SetCwd": configlib.SetCwd,
        "SetGuildHome": configlib.SetGuildHome,
        "SetUserConfig": configlib.SetUserConfig,
        "StderrCapture": util.StderrCapture,
        "SysPath": SysPath,
        "TempFile": util.TempFile,
        "UserConfig": UserConfig,
        "abspath": os.path.abspath,
        "basename": os.path.basename,
        "cat": cat,
        "cat_json": cat_json,
        "cli": cli,
        "compare_dirs": _compare_dirs,
        "compare_paths": util.compare_paths,
        "copyfile": copyfile,
        "copytree": util.copytree,
        "cd": _chdir,
        "cwd": os.getcwd,
        "diff": _diff,
        "dir": dir,
        "dirname": os.path.dirname,
        "ensure_dir": util.ensure_dir,
        "exists": os.path.exists,
        "example": _example,
        "examples_dir": _examples_dir,
        "find": find,
        "findl": file_util.find,
        "gapi": gapi,
        "guild_home": configlib.guild_home,
        "guild": guild,
        "guildfile": guildfile,
        "isdir": os.path.isdir,
        "isfile": os.path.isfile,
        "islink": os.path.islink,
        "join_path": os.path.join,
        "json": json,
        "make_executable": util.make_executable,
        "mkdir": os.mkdir,
        "mkdtemp": mkdtemp,
        "mktemp_guild_dir": mktemp_guild_dir,
        "normlf": _normlf,
        "not_used": object(),  # an uncooperative value
        "os": os,
        "path": os.path.join,
        "print_runs": _print_runs,
        "printl": _printl,
        "pprint": pprint.pprint,
        "quiet": lambda cmd, **kw: _run(cmd, quiet=True, **kw),
        "re": re,
        "realpath": util.realpath,
        "relpath": os.path.relpath,
        "rm": _rm,
        "rmdir": util.safe_rmtree,
        "run": _run,
        "run_capture": _run_capture,
        "sample": sample,
        "samples_dir": samples_dir,
        "set_guild_home": _set_guild_home,
        "sha256": util.file_sha256,
        "shlex_quote": util.shlex_quote,
        "sleep": time.sleep,
        "symlink": os.symlink,
        "sys": sys,
        "tests_dir": tests_dir,
        "touch": util.touch,
        "use_project": use_project,
        "which": util.which,
        "write": write,
        "yaml": yaml,
    }


def sample(*parts):
    return os.path.join(*(samples_dir(),) + parts)


def samples_dir():
    return os.path.join(tests_dir(), "samples")


def mkdtemp(prefix="guild-test-"):
    return tempfile.mkdtemp(prefix=prefix)


def mktemp_guild_dir():
    guild_dir = mkdtemp()
    init.init_guild_dir(guild_dir)
    return guild_dir


def find(root, followlinks=False, includedirs=False, ignore=None):
    import natsort

    paths = file_util.find(root, followlinks, includedirs)
    if ignore:
        paths = _filter_ignored(paths, ignore)
    paths = _standarize_paths(paths)
    paths.sort(key=natsort.natsort_key)
    if not paths:
        print("<empty>")
    else:
        for path in paths:
            print(path)


def _standarize_paths(paths):
    return [util.stdpath(path) for path in paths]


def _filter_ignored(paths, ignore):
    if isinstance(ignore, str):
        ignore = [ignore]
    return [
        p for p in paths if not any((fnmatch.fnmatch(p, pattern) for pattern in ignore))
    ]


def _diff(path1, path2):
    import difflib

    lines1 = [s.rstrip() for s in open(path1).readlines()]
    lines2 = [s.rstrip() for s in open(path2).readlines()]
    for line in difflib.unified_diff(lines1, lines2, path1, path2, lineterm=""):
        print(line)


def _example(name):
    return os.path.join(_examples_dir(), name)


def _examples_dir():
    try:
        return os.environ["EXAMPLES"]
    except KeyError:
        return os.path.join(guild.__pkgdir__, "examples")


def cat(*parts):
    # pylint: disable=no-value-for-parameter
    with open(os.path.join(*parts), "r") as f:
        s = f.read()
        if not s:
            print("<empty>")
        else:
            print(s)


def cat_json(*parts):
    # pylint: disable=no-value-for-parameter
    with open(os.path.join(*parts), "r") as f:
        data = json.load(f)
        json.dump(data, sys.stdout, sort_keys=True, indent=4, separators=(",", ": "))


_py_dir = dir


def dir(path=".", ignore=None):
    return sorted(
        [
            name
            for name in os.listdir(path)
            if ignore is None or not any((fnmatch.fnmatch(name, p) for p in ignore))
        ]
    )


def copyfile(*args, **kw):
    # No return value here to normalize differenced between python2
    # and python3.
    shutil.copy2(*args, **kw)


def PrintStderr():
    return util.StderrCapture(autoprint=True)


def write(filename, contents, append=False):
    try:
        contents = contents.encode()
    except AttributeError:
        pass
    opts = "ab" if append else "wb"
    with open(filename, opts) as f:
        f.write(contents)


class SysPath:
    _sys_path0 = None

    def __init__(self, path=None, prepend=None, append=None):
        path = path if path is not None else sys.path
        if prepend:
            path = prepend + path
        if append:
            path = path + append
        self.sys_path = path

    def __enter__(self):
        self._sys_path0 = sys.path
        sys.path = self.sys_path

    def __exit__(self, *exc):
        assert self._sys_path0 is not None
        sys.path = self._sys_path0


class ModelPath:
    _model_path0 = None

    def __init__(self, path):
        self.model_path = path

    def __enter__(self):
        from guild import model

        self._model_path0 = model.get_path()
        model.set_path(self.model_path)

    def __exit__(self, *exc):
        from guild import model

        assert self._model_path0 is not None
        model.set_path(self._model_path0)


class Project:
    """Project abstraction used in tests.

    This facility is deprecated and should not be used by tests moving
    forward.  In cases where it makes sense, tests that use this
    facility should be refactored to use the pattern described in
    `guild/tests/test-template.md` using `use_project()`.
    """

    def __init__(self, cwd, guild_home=None, env=None):
        from guild import index as indexlib  # expensive

        self.cwd = self.dir = cwd
        self.guild_home = guild_home or mkdtemp()
        self._env = env
        runs_cache_path = os.path.join(self.guild_home, "cache", "runs")
        self.index = indexlib.RunIndex(runs_cache_path)

    def run_capture(self, *args, **kw):
        """Runs an operation returning a tuple of run and output."""
        run_dir = self._run_dir_apply(kw)
        out = self._run(*args, **kw)
        return runlib.for_dir(run_dir), out

    def _run_dir_apply(self, kw):
        """Returns a run directory for kw, optionally apply it to kw.

        If kw contains an explicit run directory, returns
        it. Otherwise checks if kw is a restart/proto and if so
        returns the run directory associated with the specified
        restart/proto. If it's a normal run, creates a new run ID and
        applies it to kw.

        This scheme is used so that we know the run directory prior to
        running an operation. This lets us return a corresponding run
        object after the operation is finished.
        """
        return util.find_apply(
            [
                lambda: kw.get("run_dir"),
                lambda: self._restart_proto_run_dir(kw),
                lambda: self._init_run_dir_apply(kw),
            ]
        )

    def _restart_proto_run_dir(self, kw):
        """Return the run dir for a restart or proto kw if specified.

        If kw contains either restart or proto spec, performs a lookup
        within the project Guild home for a single matching run and
        returns its directory. Otherwise, returns None.

        This is used to identify the run directory prior to passing
        rerunning/restarting it.
        """
        for name in ("restart", "start", "proto"):
            spec = kw.get(name)
            if not spec:
                continue
            from guild import run_util
            from guild.commands import run_impl

            with configlib.SetGuildHome(self.guild_home):
                run = util.find_apply(
                    [run_util.marked_or_latest_run_for_opspec, run_impl.one_run], spec
                )
                return run.dir
        return None

    def _init_run_dir_apply(self, kw):
        run_id = runlib.mkid()
        run_dir = os.path.join(self.guild_home, "runs", run_id)
        kw["run_dir"] = run_dir
        return run_dir

    def _run(self, *args, **kw):
        ignore_output = kw.pop("ignore_output", False)
        cwd = os.path.join(self.cwd, kw.pop("cwd", "."))
        with self._run_env():
            out = gapi.run_capture_output(
                guild_home=self.guild_home, cwd=cwd, *args, **kw
            )
        if ignore_output:
            out = self._filter_output(out, ignore_output)
        return out.strip()

    def _run_env(self):
        env = {"NO_WARN_RUNDIR": "1"}
        if self._env:
            env.update(self._env)
        return util.Env(env)

    def run(self, *args, **kw):
        try:
            _run, out = self.run_capture(*args, **kw)
        except gapi.RunError as e:
            print(f"{e.output.strip()}\n<exit {e.returncode}>")
        else:
            print(out)

    def run_quiet(self, *args, **kw):
        cwd = os.path.join(self.cwd, kw.pop("cwd", "."))
        with self._run_env():
            gapi.run_quiet(guild_home=self.guild_home, cwd=cwd, *args, **kw)

    @staticmethod
    def _filter_output(out, ignore):
        if isinstance(ignore, str):
            ignore = [ignore]
        return "\n".join(
            [
                line
                for line in out.split("\n")
                if all(s and s not in line for s in ignore)
            ]
        )

    def list_runs(self, **kw):
        return gapi.runs_list(cwd=self.cwd, guild_home=self.guild_home, **kw)

    def print_runs(
        self,
        runs=None,
        ids=False,
        short_ids=False,
        flags=False,
        labels=False,
        tags=False,
        status=False,
        scalars=False,
        cwd=None,
        limit=None,
    ):
        runs = runs if runs is not None else self.list_runs(limit=limit)
        cwd = os.path.join(self.cwd, cwd) if cwd else self.cwd
        with util.Chdir(cwd):  # cwd used to format labels
            _print_runs(
                runs,
                ids=ids,
                short_ids=short_ids,
                flags=flags,
                labels=labels,
                tags=tags,
                status=status,
                scalars=scalars,
                index=self.index,
            )

    def delete_runs(self, runs=None, **kw):
        with PrintStderr():
            gapi.runs_delete(runs, guild_home=self.guild_home, **kw)

    def print_trials(self, *args, **kw):
        print(self._run(print_trials=True, *args, **kw))

    def ls(self, run=None, all=False, sourcecode=False):
        from guild import run_util

        run = run or self._first_run()
        sourcecode_files = set(run_util.sourcecode_files(run)) if sourcecode else {}

        def filter_path(path):
            if all:
                return True
            if sourcecode:
                return path in sourcecode_files
            return not path.startswith(".guild")

        return [path for path in file_util.find(run.dir) if filter_path(path)]

    @staticmethod
    def cat(run, path):
        cat(os.path.join(run.path, path))

    def mark(self, runs, **kw):
        with PrintStderr():
            gapi.mark(runs, cwd=self.cwd, guild_home=self.guild_home, **kw)

    def scalars(self, run):
        self.index.refresh([run], ["scalar"])
        return self.index.run_scalars(run)

    def scalar(self, run, prefix, tag, qual, step):
        self.index.refresh([run], ["scalar"])
        return self.index.run_scalar(run, prefix, tag, qual, step)

    def compare(self, runs=None, **kw):
        return gapi.compare(runs=runs, cwd=self.cwd, guild_home=self.guild_home, **kw)

    def publish(self, runs=None, **kw):
        with PrintStderr():
            gapi.publish(runs=runs, cwd=self.cwd, guild_home=self.guild_home, **kw)

    def package(self, **kw):
        with PrintStderr():
            gapi.package(cwd=self.cwd, guild_home=self.guild_home, **kw)

    def label(self, runs=None, **kw):
        with PrintStderr():
            gapi.runs_label(runs, cwd=self.cwd, guild_home=self.guild_home, **kw)

    def tag(self, runs=None, **kw):
        with PrintStderr():
            gapi.runs_tag(runs, cwd=self.cwd, guild_home=self.guild_home, **kw)

    def select(self, run=None, **kw):
        return gapi.select(run, cwd=self.cwd, guild_home=self.guild_home, **kw)

    def stop_runs(self, runs, **kw):
        gapi.runs_stop(runs, cwd=self.cwd, guild_home=self.guild_home, **kw)

    def _first_run(self):
        runs = self.list_runs()
        if not runs:
            raise RuntimeError("no runs")
        return runs[0]


class _MockConfig:
    def __init__(self, data):
        self.path = configlib.user_config_path()
        self.data = data

    def read(self):
        return self.data


class UserConfig:
    def __init__(self, config):
        self._config = _MockConfig(config)

    def __enter__(self):
        configlib._user_config = self._config

    def __exit__(self, *exc):
        # None forces a lazy re-reread from disk, which is the correct
        # behavior for a reset here.
        configlib._user_config = None


class Proxy:
    """Empty object for use as proxy."""


def _patch_py3_exception_detail():
    import traceback

    format_exception_only = traceback.format_exception_only

    def patch(*args):
        formatted = format_exception_only(*args)
        formatted[-1] = _strip_error_module(formatted[-1])
        return formatted

    traceback.format_exception_only = patch


if sys.version_info[0] > 2:
    _patch_py3_exception_detail()


def _strip_error_module(last_line):
    m = re.match(r"([\w\.]+): (.+)", last_line)
    if not m:
        return _strip_class_module(last_line)
    return f"{_strip_class_module(m.group(1))}: {m.group(2)}"


def _strip_class_module(class_name):
    return class_name[class_name.rfind(".") + 1 :]


def _normlf(s):
    return s.replace("\r", "")


def _printl(l):
    for x in l:
        print(x)


def _rm(path, force=False):
    if force and not os.path.exists(path):
        return
    os.remove(path)


def _run_capture(*args, **kw):
    return _run(*args, _capture=True, **kw)


def _run(
    cmd,
    quiet=False,
    ignore=None,
    timeout=3600,
    cut=None,
    cwd=None,
    env=None,
    _capture=False,
):
    cmd = _run_shell_cmd(cmd)
    proc_env = dict(os.environ)
    _apply_venv_bin_path(proc_env)
    if env:
        proc_env.update(env)
    proc_env["SYNC_RUN_OUTPUT"] = "1"
    p = _popen(cmd, proc_env, cwd)
    with _kill_after(p, timeout):
        out, err = p.communicate()
        assert err is None, err
        exit_code = p.returncode
    if quiet and exit_code == 0:
        return None
    out = out.strip().decode("latin-1")
    if ignore:
        out = _strip_lines(out, ignore)
    if cut:
        out = _cut_cols(out, cut)
    if _capture:
        if exit_code != 0:
            raise gapi.RunError((cmd, cwd, proc_env), exit_code, out)
        return out
    if out:
        print(out)
    print(f"<exit {exit_code}>")
    return None


def _run_shell_cmd(cmd):
    if util.get_platform() == "Windows":
        return _run_shell_win_cmd(cmd)
    return _run_shell_posix_cmd(cmd)


def _run_shell_win_cmd(cmd):
    parts = util.shlex_split(util.stdpath(cmd))
    _apply_guild_cmd_for_win(parts)
    return parts


def _apply_guild_cmd_for_win(parts):
    if parts and parts[0] == "guild":
        parts[0] = _guild_exe_for_win()


def _guild_exe_for_win():
    return util.find_apply(
        [
            _sys_arg_guild_exe_for_win,
            _which_guild_exe_for_win,
            _guild_exe_for_win_error,
        ]
    )


def _sys_arg_guild_exe_for_win():
    arg0 = sys.argv[0]
    arg0_basename = os.path.basename(arg0)
    if arg0_basename in ("guild.cmd", "guild.exe"):
        return arg0
    if arg0_basename == "guild":
        arg0_dir = os.path.dirname(arg0)
        return util.find_apply(
            [
                lambda: _test_exe_path(os.path.join(arg0_dir, "guild.exe")),
                lambda: _test_exe_path(os.path.join(arg0_dir, "guild.cmd")),
            ]
        )
    return None


def _test_exe_path(path):
    if os.path.isfile(path):
        return path
    return None


def _which_guild_exe_for_win():
    return util.find_apply(
        [
            lambda: util.which("guild.cmd"),
            lambda: util.which("guild.exe"),
        ]
    )


def _guild_exe_for_win_error():
    raise RuntimeError("cannot find guild exe for Windows")


def _run_shell_posix_cmd(cmd):
    return f"set -eu && {cmd}"


def _apply_venv_bin_path(env):
    python_bin_dir = os.path.dirname(sys.executable)
    path = env.get("PATH") or ""
    if python_bin_dir not in path:
        env["PATH"] = f"{python_bin_dir}{os.path.pathsep}${path}"


def _popen(cmd, env, cwd):
    if util.get_platform() == "Windows":
        return _popen_win(cmd, env, cwd)
    return _popen_posix(cmd, env, cwd)


def _popen_win(cmd, env, cwd):
    return subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
        env=env,
        cwd=cwd,
    )


def _popen_posix(cmd, env, cwd):
    # pylint: disable=subprocess-popen-preexec-fn
    return subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        preexec_fn=os.setsid,
        env=env,
        cwd=cwd,
    )


class _kill_after:
    def __init__(self, p, timeout):
        self._p = p
        self._timer = threading.Timer(timeout, self._kill)

    def _kill(self):
        if util.get_platform() == "Windows":
            self._kill_win()
        else:
            self._kill_posix()

    def _kill_win(self):
        try:
            self._p.send_signal(signal.CTRL_BREAK_EVENT)
            self._p.kill()
        except OSError as e:
            if e.errno != errno.ESRCH:  # no such process
                raise

    def _kill_posix(self):
        try:
            os.killpg(os.getpgid(self._p.pid), signal.SIGKILL)
        except OSError as e:
            if e.errno != errno.ESRCH:  # no such process
                raise

    def __enter__(self):
        self._timer.start()

    def __exit__(self, _type, _val, _tb):
        self._timer.cancel()


def _strip_lines(out, patterns):
    if isinstance(patterns, str):
        patterns = [patterns]
    stripped_lines = [
        line
        for line in out.split("\n")
        if not any((re.search(p, line) for p in patterns))
    ]
    return "\n".join(stripped_lines)


def _cut_cols(out, to_cut):
    assert isinstance(to_cut, list) and to_cut, to_cut
    cut_lines = [_cut_line(line, to_cut) for line in out.split("\n")]
    return "\n".join([" ".join(cut_line) for cut_line in cut_lines])


def _cut_line(line, to_cut):
    cut_line = []
    cols = line.split()
    for i in to_cut:
        cut_line.extend(cols[i : i + 1])
    return cut_line


def _chdir(s):
    os.chdir(os.path.expandvars(s))


def _set_guild_home(path):
    if os.getenv("DEBUG") == "1":
        sys.stderr.write(f"Setting Guild home: {path}\n")
    configlib.set_guild_home(path)


def _compare_dirs(d1, d2):
    if not isinstance(d1, tuple) and len(d1) != 2:
        raise ValueError("d1 must be a tuple of (dir, label)")
    if not isinstance(d2, tuple) and len(d2) != 2:
        raise ValueError("d2 must be a tuple of (dir, label)")
    d1_path, d1_label = d1
    d2_path, d2_label = d2
    cmp_dir = mkdtemp()
    d1_link = os.path.join(cmp_dir, d1_label)
    os.symlink(os.path.realpath(d1_path), d1_link)
    d2_link = os.path.join(cmp_dir, d2_label)
    os.symlink(os.path.realpath(d2_path), d2_link)
    with util.StdoutCapture() as out:
        filecmp.dircmp(d1_link, d2_link).report_full_closure()
    print(out.get_value().replace(cmp_dir, ""), end="")


def _print_runs(
    runs,
    ids=False,
    short_ids=False,
    flags=False,
    labels=False,
    tags=False,
    status=False,
    scalars=False,
    index=None,
):
    index = index or _index_for_print_runs(scalars)
    if scalars:
        assert index
        index.refresh(runs, ["scalar"])

    cols = _cols_for_print_runs(ids, short_ids, flags, labels, tags, status, scalars)
    rows = []

    for run in runs:
        rows.append(
            _row_for_print_run(
                run,
                ids,
                short_ids,
                flags,
                labels,
                tags,
                status,
                scalars,
                index,
            )
        )
    cli.table(rows, cols)


def _index_for_print_runs(scalars):
    if not scalars:
        return None

    from guild import index as indexlib

    return indexlib.RunIndex()


def _cols_for_print_runs(ids, short_ids, flags, labels, tags, status, scalars):
    cols = ["opspec"]
    if ids:
        cols.append("id")
    if short_ids:
        cols.append("short_id")
    if flags:
        cols.append("flags")
    if labels:
        cols.append("label")
    if tags:
        cols.append("tags")
    if status:
        cols.append("status")
    if scalars:
        cols.append("scalars")
    return cols


def _row_for_print_run(
    run,
    ids,
    short_ids,
    flags,
    labels,
    tags,
    status,
    scalars,
    index,
):
    from guild.commands import runs_impl

    fmt_run = runs_impl.format_run(run)
    row = {"opspec": fmt_run["op_desc"]}
    if ids:
        row["id"] = run.id
    if short_ids:
        row["short_id"] = run.short_id
    if flags:
        row["flags"] = _print_run_flags(run)
    if labels:
        row["label"] = run.get("label")
    if tags:
        row["tags"] = " ".join(sorted(run.get("tags") or []))
    if status:
        row["status"] = run.status
    if scalars:
        row["scalars"] = _print_run_scalars(run, index)
    return row


def _print_run_flags(run):
    flag_vals = run.get("flags") or {}
    return op_util.flags_desc(flag_vals, delim=" ")


def _print_run_scalars(run, index):
    assert index
    scalars = index.run_scalars(run)
    return " ".join(f"{s['tag']}={s['last_val']:.5f}" for s in scalars)


class _Platform:
    _platform_save = None

    def __init__(self, platform):
        self._platform = platform

    def __enter__(self):
        self._platform_save = PLATFORM
        globals()["PLATFORM"] = self._platform

    def __exit__(self, *_args):
        globals()["PLATFORM"] = self._platform_save


class _Ignore(util.StdoutCapture):
    def __init__(self, ignore_patterns):
        self.ignore_patterns = _compile_ignore_patterns(ignore_patterns)

    def __exit__(self, *args):
        super().__exit__(*args)
        sys.stdout.write(_strip_ignored_lines(self._captured, self.ignore_patterns))


def _compile_ignore_patterns(patterns):
    if not isinstance(patterns, list):
        patterns = [patterns]
    return [re.compile(p) for p in patterns]


def _strip_ignored_lines(captured, ignore_patterns):
    lines = "".join(captured).split("\n")
    filtered = [line for line in lines if not _capture_ignored(line, ignore_patterns)]
    return "\n".join(filtered)


def _capture_ignored(s, ignore_patterns):
    return any(p.search(s) for p in ignore_patterns)


def use_project(project_name, guild_home=None):
    guild_home = guild_home or mkdtemp()
    _chdir(sample("projects", project_name))
    _set_guild_home(guild_home)


def _run_parallel(tests, skip, fail_fast, force, concurrency):
    skip = skip or []
    tests = _init_concurrent_tests(tests, skip)
    test_queue = _init_test_queue([test for test in tests if not test.skip])
    test_runners = _init_test_runners(test_queue, fail_fast, force, concurrency)
    try:
        success = True
        for test in tests:
            if test.skip:
                sys.stdout.write(_test_skipped_output(test.name))
                continue
            test.wait_done()
            assert test.output is not None
            assert test.success is not None
            sys.stdout.write(test.output)
            success &= test.success
        assert test_queue.empty()
        for runner in test_runners:
            runner.join()
        assert all(not r.is_alive() for r in test_runners)
        return success
    except (KeyboardInterrupt, Exception):
        for runner in test_runners:
            runner.stop()
        raise


def _init_concurrent_tests(tests, skip):
    return [_ConcurrentTest(name, name in skip) for name in tests]


class _ConcurrentTest:
    def __init__(self, name, skip):
        self.name = name
        self.skip = skip
        self.success = None
        self.output = None
        self._done_event = threading.Event()

    def wait_done(self):
        self._done_event.wait()

    def set_done(self, success, output):
        assert success is not None
        assert output is not None
        self.success = success
        self.output = output
        self._done_event.set()


def _init_test_queue(tests):
    q = queue.Queue()
    for test in tests:
        q.put(test)
    return q


def _init_test_runners(test_queue, fail_fast, force, concurrency):
    assert not test_queue.empty()
    return [
        _ConcurrentTestRunner(test_queue, fail_fast, force) for _ in range(concurrency)
    ]


class _ConcurrentTestRunner(threading.Thread):
    def __init__(self, test_queue, fail_fast, force):
        super().__init__()
        self.test_queue = test_queue
        self.fail_fast = fail_fast
        self.force = force
        self._p_lock = threading.Lock()
        self._p = None
        self._running_lock = threading.Lock()
        self._running = True
        self.start()

    @property
    def running(self):
        with self._running_lock:
            return self._running

    def stop(self, timeout=5):
        with self._running_lock:
            self._running = False
        with self._p_lock:
            if not self._p:
                return
            self._p.terminate()
            self._p.wait(timeout)
            if self._p.returncode is None:
                self._p.kill()
            self._p = None

    def run(self):
        while self.running:
            try:
                test = self.test_queue.get(block=False)
            except queue.Empty:
                break
            else:
                try:
                    with self._p_lock:
                        assert not self._p
                        self._p = _start_external_test_proc(
                            test.name,
                            self.fail_fast,
                            self.force,
                        )
                    out, _err = self._p.communicate()
                    assert self._p.returncode is not None
                    assert out is not None
                    success = self._p.returncode == 0
                    out = out.decode()
                    with self._p_lock:
                        self._p = None
                except AssertionError:
                    test.set_done(False, "")
                    raise
                except Exception as e:
                    test.set_done(False, str(e))
                else:
                    test.set_done(success, out)


def _start_external_test_proc(test_name, fail_fast, force):
    env = dict(os.environ)
    env["PYTHONPATH"] = guild.__pkgdir__
    cmd = [
        sys.executable,
        "-m",
        "guild.main_bootstrap",
        "check",
        "--no-chrome",  # just print test results
        "-nt",
        test_name,
    ]
    if fail_fast:
        cmd.append("--fast")
    if force:
        cmd.append("--force-test")
    return subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
    )
