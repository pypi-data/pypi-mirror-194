# Copyright 2017-2023 Posit Software, PBC
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
import collections
import csv
import datetime
import os
import re
import shutil
import stat

import jinja2
import yaml

from guild import run_util
from guild import util
from guild import yaml_util

DEFAULT_DEST_HOME = "published-runs"
DEFAULT_TEMPLATE = "default"

NO_COPY_FILES = 0
COPY_DEFAULT_FILES = 1
COPY_ALL_FILES = 2


class PublishError(Exception):
    pass


class TemplateError(PublishError):
    def __init__(self, e):
        super().__init__(e)
        self._e = e

    def __str__(self):
        if hasattr(self._e, "filename"):
            return self._default_str()
        return super().__str__()

    def _default_str(self):
        e = self._e
        msg = e.filename
        if hasattr(e, "lineno"):
            msg += ":" + str(e.lineno)
        if e.message:
            msg += ": " + e.message
        return msg


class GenerateError(PublishError):
    def __init__(self, e, template):
        super().__init__(e)
        self._e = e
        self._template = template

    def __str__(self):
        return f"{_format_template_files(self._template)}: {self._e.message}"


def _format_template_files(t):
    if len(t.files) == 1:
        basename = t.files[0]
    else:
        basename = f"{{{','.join(sorted(t.files))}}}"
    return os.path.join(t.path, basename)


class RunFilters:
    IMG_PATTERN = re.compile(r"\.(png|gif|jpe?g|tiff?|bmp|webp)", re.IGNORECASE)

    def __init__(self, run_dest):
        self.run_dest = run_dest

    def install(self, env):
        env.filters.update(
            {
                "csv_dict_rows": self.csv_dict_rows,
                "empty": self.empty,
                "file_size": self.file_size,
                "flag_val": self.flag_val,
                "nbhyph": self.nbhyph,
                "nbsp": self.nbsp,
                "runfile_link": self.runfile_link,
                "scalar_key": self.scalar_key,
                "short_id": self.short_id,
                "utc_date": self.utc_date,
            }
        )

    @staticmethod
    def empty(val):
        if val in (None, "") or isinstance(val, jinja2.Undefined):
            return ""
        return val

    @staticmethod
    def flag_val(val):
        if isinstance(val, jinja2.Undefined):
            return ""
        return run_util.format_attr(val)

    def runfile_link(self, path):
        if self.run_dest is None:
            raise TemplateError(
                "runfile_link cannot be used in this context (not publishing a run"
            )
        if not isinstance(path, str):
            return ""
        maybe_runfile = os.path.join(self.run_dest, "runfiles", path)
        if os.path.isfile(maybe_runfile):
            return "runfiles/" + path
        return None

    @staticmethod
    def utc_date(val, unit="s"):
        if not isinstance(val, (int, float, str)):
            return ""
        try:
            val = int(val)
        except (ValueError, TypeError):
            return ""
        else:
            if unit == "s":
                ts = val * 1000000
            elif unit == "ms":
                ts = val * 1000
            elif unit == "us":
                ts = val
            else:
                raise ValueError(f"unsupported unit {unit!r} (expected s, ms, or us)")
            return util.utcformat_timestamp(ts)

    @staticmethod
    def file_size(val):
        if not isinstance(val, (int, float, str)):
            return ""
        try:
            bytes = int(val)
        except (ValueError, TypeError):
            return ""
        else:
            return util.format_bytes(bytes)

    @staticmethod
    def scalar_key(s):
        return run_util.run_scalar_key(s)

    @staticmethod
    def csv_dict_rows(csv_rows):
        keys = csv_rows[0]
        return [dict(zip(keys, row)) for row in csv_rows[1:]]

    @staticmethod
    def nbsp(x):
        if not x:
            return "&nbsp;"
        return x

    @staticmethod
    def short_id(id):
        if not isinstance(id, str):
            return ""
        return id[:8]

    @staticmethod
    def nbhyph(s):
        if not s:
            return s
        return s.replace("-", "&#8209;")


class Template:
    def __init__(self, path, run_dest=None, filters=None):
        if not os.path.exists(path):
            raise RuntimeError(f"invalid template source: {path}")
        self.path = path
        self._file_templates = sorted(_init_file_templates(path, run_dest, filters))

    @property
    def files(self):
        return [t[0] for t in self._file_templates]

    def generate(self, dest, vars):
        util.ensure_dir(dest)
        for relpath, src, template in self._file_templates:
            file_dest = os.path.join(dest, relpath)
            util.ensure_dir(os.path.dirname(file_dest))
            if template is None:
                shutil.copyfile(src, file_dest)
            else:
                _render_template(template, vars, file_dest)


def _init_file_templates(path, run_dest=None, filters=None):
    ts = []
    for root, _dirs, files in os.walk(path):
        for name in files:
            if name[:1] == "_":
                continue
            abspath = os.path.join(root, name)
            relpath = os.path.relpath(abspath, path)
            template = _init_file_template(abspath, run_dest, filters)
            ts.append((relpath, abspath, template))
    return ts


def _init_file_template(path, run_dest=None, filters=None):
    """Returns template for path or None if path is not a text file.

    Raises TemplateError if path does not exist or cannot be parsed as
    a template.
    """
    if not os.path.exists(path):
        raise TemplateError(f"{path} does not exist")
    if not util.is_text_file(path):
        return None
    dirname, basename = os.path.split(path)
    templates_home = _local_path("templates")
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader([dirname, templates_home]),
        autoescape=jinja2.select_autoescape(['html', 'xml']),
    )
    RunFilters(run_dest).install(env)
    if filters:
        env.filters.update(filters)
    try:
        return env.get_template(basename)
    except jinja2.TemplateError as e:
        raise TemplateError(e) from e


def _render_template(template, vars, dest):
    with open(dest, "w") as f:
        for part in template.generate(vars):
            f.write(part)
        f.write(os.linesep)


PublishRunState = collections.namedtuple(
    "PublishRunState",
    [
        "run",
        "opdef",
        "copy_files",
        "include_links",
        "formatted_run",
        "dest_home",
        "template",
        "run_dest",
        "md5s",
    ],
)


def publish_run(
    run,
    dest=None,
    template=None,
    copy_files=None,
    include_links=False,
    md5s=True,
    formatted_run=None,
):
    state = _init_publish_run_state(
        run, dest, template, copy_files, include_links, md5s, formatted_run
    )
    _init_published_run(state)
    _publish_run_guild_files(state)
    _copy_sourcecode(state)
    _maybe_copy_runfiles(state)
    _generate_template(state)


def _init_publish_run_state(
    run, dest, template, copy_files, include_links, md5s, formatted_run
):
    dest_home = dest or DEFAULT_DEST_HOME
    opdef = run_util.run_opdef(run)
    run_dest = _published_run_dest(dest_home, run)
    template = _init_template(template, opdef, run_dest)
    if not formatted_run:
        formatted_run = _format_run_for_publish(run)
    return PublishRunState(
        run,
        opdef,
        copy_files,
        include_links,
        formatted_run,
        dest_home,
        template,
        run_dest,
        md5s,
    )


def _init_template(template, opdef, run_dest):
    template_spec = util.find_apply([lambda: template, lambda: _opdef_template(opdef)])
    template_path = _find_template(template_spec, opdef)
    return Template(template_path, run_dest)


def _opdef_template(opdef):
    return util.find_apply(
        [lambda: _opdef_publish_template(opdef), lambda: DEFAULT_TEMPLATE]
    )


def _opdef_publish_template(opdef):
    if not opdef or not opdef.publish:
        return None
    return opdef.publish.template


def _find_template(name, opdef):
    return util.find_apply(
        [
            lambda: _abs_template(name),
            lambda: _default_template(name),
            lambda: _project_template(name, opdef),
            lambda: _cannot_find_template_error(name),
        ]
    )


def _abs_template(name):
    if name[:1] == "." and os.path.exists(name):
        return name
    return None


def _default_template(name):
    if name == "default":
        return _local_path("templates/publish-default")
    return None


def _local_path(path):
    return os.path.join(os.path.dirname(__file__), path)


def _project_template(name, opdef):
    path = os.path.join(opdef.guildfile.dir, name)
    if os.path.exists(path):
        return path
    return None


def _cannot_find_template_error(name):
    raise PublishError(f"cannot find template {name}")


def _published_run_dest(dest_home, run):
    return os.path.join(dest_home, run.id)


def _format_run_for_publish(run):
    frun = run_util.format_run(run)
    if not frun["stopped"]:
        frun["duration"] = ""
    return frun


def _init_published_run(state):
    """Ensure empty target directory for published run.

    As a side effect, lazily creates `state.dest_home` and creates
    `.guild-nocopy` to ensure that the published runs home is not
    considered by Guild for source snapshots.
    """
    util.ensure_dir(state.dest_home)
    util.touch(os.path.join(state.dest_home, ".guild-nocopy"))
    if os.path.exists(state.run_dest):
        util.safe_rmtree(state.run_dest)
    os.mkdir(state.run_dest)


def _publish_run_guild_files(state):
    _publish_run_info(state)
    _publish_flags(state)
    _publish_scalars(state)
    _publish_output(state)
    _publish_sourcecode_list(state)
    _publish_runfiles_list(state)


def _publish_run_info(state):
    """Write run.yml to run publish dest.

    This function should be kept in sync with output generated by
    `guild runs info` - minus system-specific values (e.g. run_dir and
    pid) and flags (which are written to a separate file).
    """
    run = state.run
    frun = state.formatted_run
    path = os.path.join(state.run_dest, "run.yml")
    encode = lambda x: yaml_util.encode_yaml(x).rstrip()
    fmt_ts = util.utcformat_timestamp
    started = run.get("started")
    stopped = run.get("stopped")
    with codecs.open(path, "w", "utf-8") as f:
        f.write(f"id: {run.id}\n")
        f.write(f"operation: {encode(frun['operation'])}\n")
        f.write(f"status: {encode(frun['status'])}\n")
        f.write(f"started: {fmt_ts(started)}\n")
        f.write(f"stopped: {fmt_ts(stopped)}\n")
        f.write(f"time: {_format_time(started, stopped)}\n")
        f.write(f"marked: {encode(frun['marked'])}\n")
        f.write(f"label: {encode(run.get('label'))}\n")
        f.write(f"command: {encode(frun['command'])}\n")
        f.write(f"exit_status: {encode(frun['exit_status'])}\n")


def _format_time(started, stopped):
    if started and stopped:
        return util.format_duration(started, stopped)
    return ""


def _publish_flags(state):
    flags = state.run.get("flags") or {}
    dest = os.path.join(state.run_dest, "flags.yml")
    _save_yaml(flags, dest)


def _save_yaml(val, path):
    with open(path, "w") as f:
        yaml.safe_dump(
            val,
            f,
            default_flow_style=False,
            indent=2,
            encoding="utf-8",
            allow_unicode=True,
        )


def _publish_scalars(state):
    cols = [
        "prefix",
        "tag",
        "count",
        "total",
        "avg_val",
        "first_val",
        "first_step",
        "last_val",
        "last_step",
        "min_val",
        "min_step",
        "max_val",
        "max_step",
    ]
    dest = os.path.join(state.run_dest, "scalars.csv")
    scalars = _run_scalars(state)
    with open(dest, "w") as f:
        out = csv.writer(f, lineterminator="\n")
        out.writerow(cols)
        for s in scalars:
            out.writerow([s[col] for col in cols])


def _run_scalars(state):
    from guild import index as indexlib  # expensive

    index = indexlib.RunIndex()
    index.refresh([state.run], ["scalar"])
    return list(index.run_scalars(state.run))


def _publish_output(state):
    src = state.run.guild_path("output")
    if os.path.isfile(src):
        dest = os.path.join(state.run_dest, "output.txt")
        shutil.copyfile(src, dest)


def _publish_sourcecode_list(state):
    dest = os.path.join(state.run_dest, "sourcecode.csv")
    with open(dest, "w") as out:
        _write_sourcecode_csv(state.run, state.md5s, out)


def _write_sourcecode_csv(run, md5s, out):
    paths = util.natsorted(run_util.sourcecode_files(run))
    csv_out = csv.writer(out, lineterminator="\n")
    csv_out.writerow(["path", "type", "size", "mtime", "md5"])
    for path in paths:
        src = os.path.join(run.dir, path)
        csv_out.writerow(_file_csv_row(path, src, md5s))


def _path_type(st, lst):
    parts = []
    if st:
        if stat.S_ISREG(st.st_mode):
            parts.append("file")
        elif stat.S_ISDIR(st.st_mode):
            parts.append("dir")
        else:
            parts.append("other")
    if lst:
        if stat.S_ISLNK(lst.st_mode):
            parts.append("link")
    return " ".join(parts)


def _path_mtime(st):
    if not st:
        return ""
    return int((st.st_mtime + _utc_offset()) * 1000000)


def _utc_offset():
    try:
        return globals()["__utc_offset"]
    except KeyError:
        globals()["__utc_offset"] = offset = int(
            round(
                (datetime.datetime.now() - datetime.datetime.utcnow()).total_seconds()
            )
        )
        return offset


def _path_md5(path, st):
    if not st or not stat.S_ISREG(st.st_mode):
        return ""
    return util.file_md5(path)


def _publish_runfiles_list(state):
    dest = os.path.join(state.run_dest, "runfiles.csv")
    with open(dest, "w") as out:
        _write_runfile_csv(state.run, state.md5s, out)


def _write_runfile_csv(run, md5s, out):
    paths = util.natsorted(_runfiles(run))
    csv_out = csv.writer(out, lineterminator="\n")
    csv_out.writerow(["path", "type", "size", "mtime", "md5"])
    for path in paths:
        src = os.path.join(run.dir, path)
        csv_out.writerow(_file_csv_row(path, src, md5s))


def _runfiles(run):
    sourcecode = set(run_util.sourcecode_files(run))
    paths = []
    for root, dirs, files in os.walk(run.dir, followlinks=True):
        util.safe_list_remove(".guild", dirs)
        for name in files:
            relpath = os.path.relpath(os.path.join(root, name), run.dir)
            if relpath in sourcecode:
                continue
            paths.append(relpath)
    return paths


def _file_csv_row(path, src, md5):
    st = _maybe_stat(src)
    lst = _maybe_lstat(src)
    return [
        path,
        _path_type(st, lst),
        st.st_size if st else "",
        _path_mtime(st),
        _path_md5(src, st) if md5 else "",
    ]


def _maybe_stat(src):
    try:
        return os.stat(src)
    except OSError:
        return None


def _maybe_lstat(src):
    try:
        return os.lstat(src)
    except OSError:
        return None


def _copy_sourcecode(state):
    util.select_copytree(
        run_util.sourcecode_dest(state.run),
        _sourcecode_dest(state),
        [],
        _SourcecodeFilter(state),
    )


class _SourcecodeFilter(util.CopyFilter):
    def __init__(self, state):
        self.run_dir = state.run.dir
        self.files = set(run_util.sourcecode_files(state.run))

    def default_select_path(self, path):
        return _is_sourcecode_file(path, self.run_dir, self.files)


def _is_sourcecode_file(path, run_dir, manifest_set):
    relpath = util.stdpath(os.path.relpath(path, run_dir))
    return relpath in manifest_set


def _sourcecode_dest(state):
    return os.path.join(state.run_dest, "sourcecode")


class PublishRunVars:
    def __init__(self, state):
        self._state = state
        self._cache = {}
        self._keys = [
            "flags",
            "output",
            "run",
            "runfiles",
            "scalars",
            "sourcecode",
        ]

    def keys(self):
        return self._keys

    def __getitem__(self, name):
        try:
            return self._cache[name]
        except KeyError:
            self._cache[name] = val = self._load(name)
            return val

    def _load(self, name):
        return util.find_apply([self._load_yaml, self._load_csv, self._load_txt], name)

    def _load_yaml(self, name):
        path = os.path.join(self._state.run_dest, name + ".yml")
        if not os.path.exists(path):
            return None
        return yaml.safe_load(open(path, "r"))

    def _load_csv(self, name):
        path = os.path.join(self._state.run_dest, name + ".csv")
        if not os.path.exists(path):
            return None
        with open(path, "r") as f:
            return list(csv.reader(f))

    def _load_txt(self, name):
        path = os.path.join(self._state.run_dest, name + ".txt")
        if not os.path.exists(path):
            return None
        return open(path, "r").read()


def _delete_guild_dir(dirs):
    try:
        dirs.remove(".guild")
    except ValueError:
        pass


def _delete_dir_links(parent, dirs):
    """Deletes any symlinked dirs from `dirs`.

    `dirs` is a list of dir names under the directory `parent`.
    """
    for name in list(dirs):
        if os.path.islink(os.path.join(parent, name)):
            dirs.remove(name)


def _maybe_copy_runfiles(state):
    if not state.copy_files:
        return
    util.select_copytree(
        state.run.dir,
        _runfiles_dest(state),
        _copy_runfiles_config(state),
        _CopyRunFilesFilter(state),
    )


def _runfiles_dest(state):
    return os.path.join(state.run_dest, "runfiles")


def _copy_runfiles_config(state):
    if state.copy_files in (NO_COPY_FILES, COPY_ALL_FILES):
        # If we're not copying files or we're copying all files,
        # ignore user-defined criteria - the determining result is
        # defined by the copy filter used with `select_copytree()`
        return []
    if not state.opdef:
        # If we don't have an opdef for a run there's no selection
        # criteria to provide
        return []
    return [state.opdef.publish.files]


class _CopyRunFilesFilter(util.CopyFilter):
    """Filter used to copy run files.

    This is part of the `util.select_copytree()` interface. It
    performs two tasks: remove dirs from the list of traversals and
    provide a default select result for a candidate path.

    `.guild` are always removed from dirs lists for travesal as there
    are no files under `.guild` that are considered for selection.

    Linked directories are also removed unless `state.include_links`
    is true.

    The default select result is used by the copy operation only when
    a configured selection rule has not been applied. In this case,
    the default determines if the file is selected for copy.

    Source code files are never selected for copy by this filter as
    they aren't considered run files by definition.

    Links are not selected unless `state.include_links` is true.

    If a candidate path is a source code file, the default select
    result is always `False`. Source code files are not considered run
    files and are copied as a separate publishing step.

    If `state.copy_files` is not `COPY_ALL_FILES` the default select
    value `False`. This puts places responsibility for a path select
    on the configured rules.

    If `state.copy_files` is `COPY_ALL_FILES`, the default select
    value is `True` if the candidate is not a link or
    `state.include_links` is true.
    """

    def __init__(self, state):
        self.state = state
        self.sourcecode_files = set(run_util.sourcecode_files(state.run))

    def delete_excluded_dirs(self, parent, dirs):
        _delete_guild_dir(dirs)
        if not self.state.include_links:
            _delete_dir_links(parent, dirs)

    def default_select_path(self, path):
        if self.state.copy_files not in (COPY_DEFAULT_FILES, COPY_ALL_FILES):
            return False
        if _is_sourcecode_file(path, self.state.run.dir, self.sourcecode_files):
            return False
        return self.state.include_links or not os.path.islink(path)


def _generate_template(state):
    template = state.template
    render_vars = PublishRunVars(state)
    try:
        template.generate(state.run_dest, render_vars)
    except jinja2.TemplateRuntimeError as e:
        raise GenerateError(e, template) from e
    except jinja2.exceptions.TemplateNotFound as e:
        e.message = f"template not found: {e.message}"
        raise GenerateError(e, template) from e


def _template_config(opdef):
    if not opdef or not opdef.publish:
        return {}
    config = opdef.publish.get("config") or {}
    return {name.replace("-", "_"): val for name, val in config.items()}


def refresh_index(dest, index_template_path=None):
    dest_home = dest or DEFAULT_DEST_HOME
    if not index_template_path:
        index_template_path = _local_path("templates/runs-index/README.md")
    template = _init_file_template(index_template_path)
    index_path = os.path.join(dest_home, "README.md")
    runs = _published_runs(dest_home)
    _render_template(template, {"runs": runs}, index_path)


def _published_runs(dest_home):
    runs = []
    for name in os.listdir(dest_home):
        run_yml = os.path.join(dest_home, name, "run.yml")
        if not os.path.exists(run_yml):
            continue
        info = yaml.safe_load(open(run_yml, "r"))
        runs.append(info)
    return sorted(runs, key=lambda run: run.get("started"), reverse=True)
