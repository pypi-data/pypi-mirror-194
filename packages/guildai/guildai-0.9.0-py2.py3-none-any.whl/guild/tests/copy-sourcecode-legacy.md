# Copying source code

These tests confirm that Guild continues to support alternative source
code destinations. We will support this behavior for backward
compatibility until it's obvious that changing it is safe for all
users.

These tests exercise each of the operations defined in the
`copy-sourcecode-legacy` sample project.

    >>> project_dir_src = sample("projects/copy-sourcecode-legacy")

We configure the default source code dest as the legacy value
`.guild/sourcecode` for the default model, which is shown below when
we print operation source code configuration.

To control the files that are under the project, we copy the project
source to a new location, taking care to copy only the following
files:

    >>> project_files = [
    ...   ".dotdir",
    ...   ".dotdir/a.txt",
    ...   ".gitattributes",
    ...   "__pycache__/hello.pyc",
    ...   "a.txt",
    ...   "empty",
    ...   "env",
    ...   "env/bin",
    ...   "env/bin/activate",
    ...   "env/some-env-file",
    ...   "guild.yml",
    ...   "hello.py",
    ...   "hello.pyc",
    ...   "nocopy_dir",
    ...   "nocopy_dir/.guild-nocopy",
    ...   "nocopy_dir/a.txt",
    ...   "subdir",
    ...   "subdir/b.txt",
    ...   "subdir/logo.png",
    ... ]

Copy the project files to a new project directory:

    >>> project_dir = mkdtemp()

    >>> for root, _dirs, names in os.walk(project_dir_src):
    ...     for name in names:
    ...         src = path(root, name)
    ...         relpath = os.path.relpath(src, project_dir_src)
    ...         normpath = relpath.replace(os.path.sep, "/")
    ...         if not normpath in project_files:
    ...             continue
    ...         dest = path(project_dir, relpath)
    ...         ensure_dir(dirname(dest))
    ...         copyfile(src, dest)

    >>> find(project_dir)  # doctest: +REPORT_UDIFF
    .dotdir/a.txt
    .gitattributes
    __pycache__/hello.pyc
    a.txt
    empty
    env/bin/activate
    env/some-env-file
    guild.yml
    hello.py
    hello.pyc
    nocopy_dir/.guild-nocopy
    nocopy_dir/a.txt
    subdir/b.txt
    subdir/logo.png

    >>> project = Project(project_dir)

Helper function for printing operation sourcecode config:

    >>> import yaml
    >>> from guild import yaml_util

    >>> data = yaml.safe_load(open(join_path(project_dir, "guild.yml"), "r"))

    >>> def print_config(op):
    ...     parts = op.split(":", 1)
    ...     if len(parts) == 1:
    ...         model = ""
    ...     else:
    ...         model, op = parts
    ...     for model_data in data:
    ...         if model_data["model"] == model:
    ...             break
    ...     else:
    ...         assert False, (model, op)
    ...     config = {}
    ...     if "sourcecode" in model_data:
    ...         config["model-sourcecode"] = model_data["sourcecode"]
    ...     op_data = model_data["operations"][op]
    ...     if "sourcecode" in op_data:
    ...         config["op-sourcecode"] = op_data["sourcecode"]
    ...     if config:
    ...         print(yaml_util.encode_yaml(config).strip())
    ...     else:
    ...         print("<none>")

Helper function that runs the specified operation outside of Guild
home (i.e. to a new, temp run directory) and prints the list of copied
files for the generated run:

    >>> def run(op, sourcecode_root=".guild/sourcecode"):
    ...     run_dir = mkdtemp()
    ...     project.run_quiet(op, run_dir=run_dir)
    ...     find(join_path(run_dir, sourcecode_root))

And a helper for previewing source code copies:

    >>> def preview(op):
    ...     project.run(op, test_sourcecode=True)

## Default files

Guild copies text files by default.

    >>> print_config("default")
    model-sourcecode:
      dest: .guild/sourcecode

Here's a preview of the copy, which shows the rules that are applied:

    >>> preview("default")  # doctest: +REPORT_UDIFF
    Copying from the current directory
    Rules:
      exclude dir .*
      exclude dir * containing .guild-nocopy
      include text * size < 1048577, max match 100
      exclude dir __pycache__
      exclude dir * containing bin/activate
      exclude dir * containing Scripts/activate
      exclude dir build
      exclude dir dist
      exclude dir *.egg-info
    Selected for copy:
      .gitattributes
      a.txt
      empty
      guild.yml
      hello.py
      subdir/b.txt
    Skipped:
      .dotdir/
      __pycache__/
      env/
      nocopy_dir/
      hello.pyc
      subdir/logo.png

Note that Guild doesn't consider files under ignored directories for
selected/ignored preview. This is an optimization to avoid evaluating
potentially large numbers of files in ignored directories.

And the copied files:

    >>> run("default")
    .gitattributes
    a.txt
    empty
    guild.yml
    hello.py
    subdir/b.txt

## Alternate root

Specify `root` to change the directory that files are copied from.

    >>> print_config("alt-root")
    model-sourcecode:
      dest: .guild/sourcecode
    op-sourcecode:
      root: subdir

    >>> preview("alt-root")
    Copying from 'subdir'
    Rules:
      exclude dir .*
      exclude dir * containing .guild-nocopy
      include text * size < 1048577, max match 100
      exclude dir __pycache__
      exclude dir * containing bin/activate
      exclude dir * containing Scripts/activate
      exclude dir build
      exclude dir dist
      exclude dir *.egg-info
    Selected for copy:
      subdir/b.txt
    Skipped:
      subdir/logo.png

    >>> run("alt-root")
    b.txt

## Include additional files

To include additional files that are not otherwise selected (i.e. are
not text files), use explicit includes.

    >>> print_config("include-png")
    model-sourcecode:
      dest: .guild/sourcecode
    op-sourcecode:
    - include: '*.png'

This rule is applied after the default rules:

    >>> preview("include-png")  # doctest: +REPORT_UDIFF
    Copying from the current directory
    Rules:
      exclude dir .*
      exclude dir * containing .guild-nocopy
      include text * size < 1048577, max match 100
      exclude dir __pycache__
      exclude dir * containing bin/activate
      exclude dir * containing Scripts/activate
      exclude dir build
      exclude dir dist
      exclude dir *.egg-info
      include *.png
    Selected for copy:
      .gitattributes
      a.txt
      empty
      guild.yml
      hello.py
      subdir/b.txt
      subdir/logo.png
    Skipped:
      .dotdir/
      __pycache__/
      env/
      nocopy_dir/
      hello.pyc

The `png` file is copied along containing the default files:

    >>> run("include-png")
    <BLANKLINE>
    .gitattributes
    a.txt
    empty
    guild.yml
    hello.py
    subdir/b.txt
    subdir/logo.png

## Override defaults

Defaults can be overridden containing explicit string patterns.

Only png files:

    >>> print_config("only-png")
    model-sourcecode:
      dest: .guild/sourcecode
    op-sourcecode: '*.png'

When only string patterns are specified for an include, Guild
implicitly inserts an exclude * before adding the patterns. This
ensures that only those files matching the specified patterns are
selected.

    >>> preview("only-png")  # doctest: +REPORT_UDIFF
    Copying from the current directory
    Rules:
      exclude dir .*
      exclude dir * containing .guild-nocopy
      include text * size < 1048577, max match 100
      exclude dir __pycache__
      exclude dir * containing bin/activate
      exclude dir * containing Scripts/activate
      exclude dir build
      exclude dir dist
      exclude dir *.egg-info
      exclude *
      include *.png
    Selected for copy:
      subdir/logo.png
    Skipped:
      .dotdir/
      __pycache__/
      env/
      nocopy_dir/
      .gitattributes
      a.txt
      empty
      guild.yml
      hello.py
      hello.pyc
      subdir/b.txt

    >>> run("only-png")
    subdir/logo.png

Only py files:

    >>> print_config("only-py")
    model-sourcecode:
      dest: .guild/sourcecode
    op-sourcecode:
    - '*.py'

    >>> run("only-py")
    hello.py

Only png and py files:

    >>> print_config("png-and-py")
    model-sourcecode:
      dest: .guild/sourcecode
    op-sourcecode:
    - '*.png'
    - '*.py'

    >>> run("png-and-py")
    hello.py
    subdir/logo.png

This logic can be alternatively specified by first excluding all
matches and then including those to select.

    >>> print_config("only-py2")
    model-sourcecode:
      dest: .guild/sourcecode
    op-sourcecode:
    - exclude: '*'
    - include: '*.py'

    >>> run("only-py2")
    hello.py

## Excluding some default files

Some of the default files can be excluded by specifying one or more
exclude specs.

    >>> print_config("exclude-py")
    model-sourcecode:
      dest: .guild/sourcecode
    op-sourcecode:
    - exclude: '*.py'

    >>> preview("exclude-py")  # doctest: +REPORT_UDIFF
    Copying from the current directory
    Rules:
      exclude dir .*
      exclude dir * containing .guild-nocopy
      include text * size < 1048577, max match 100
      exclude dir __pycache__
      exclude dir * containing bin/activate
      exclude dir * containing Scripts/activate
      exclude dir build
      exclude dir dist
      exclude dir *.egg-info
      exclude *.py
    Selected for copy:
      .gitattributes
      a.txt
      empty
      guild.yml
      subdir/b.txt
    Skipped:
      .dotdir/
      __pycache__/
      env/
      nocopy_dir/
      hello.py
      hello.pyc
      subdir/logo.png

    >>> run("exclude-py")
    .gitattributes
    a.txt
    empty
    guild.yml
    subdir/b.txt

## Excluding directories

Guild does not evaluate files under excluded directories. Such files
are neither selected nor ignored - they are not even seen.

    >>> print_config("no-subdir")
    model-sourcecode:
      dest: .guild/sourcecode
    op-sourcecode:
    - exclude:
        dir: subdir

In the preview, 'subdir' is not mentioned:

    >>> preview("no-subdir")  # doctest: +REPORT_UDIFF
    Copying from the current directory
    Rules:
      exclude dir .*
      exclude dir * containing .guild-nocopy
      include text * size < 1048577, max match 100
      exclude dir __pycache__
      exclude dir * containing bin/activate
      exclude dir * containing Scripts/activate
      exclude dir build
      exclude dir dist
      exclude dir *.egg-info
      exclude dir subdir
    Selected for copy:
      .gitattributes
      a.txt
      empty
      guild.yml
      hello.py
    Skipped:
      .dotdir/
      __pycache__/
      env/
      nocopy_dir/
      subdir/
      hello.pyc

And the copied files:

    >>> run("no-subdir")
    .gitattributes
    a.txt
    empty
    guild.yml
    hello.py

## Including only directories

Source code can be limited to only subdirectories by specifying the
globbed subdirectory as a string.

    >>> print_config("only-subdir")
    model-sourcecode:
      dest: .guild/sourcecode
    op-sourcecode: subdir/*

The preview:

    >>> preview("only-subdir")  # doctest: +REPORT_UDIFF
    Copying from the current directory
    Rules:
      exclude dir .*
      exclude dir * containing .guild-nocopy
      include text * size < 1048577, max match 100
      exclude dir __pycache__
      exclude dir * containing bin/activate
      exclude dir * containing Scripts/activate
      exclude dir build
      exclude dir dist
      exclude dir *.egg-info
      exclude *
      include subdir/*
    Selected for copy:
      subdir/b.txt
      subdir/logo.png
    Skipped:
      .dotdir/
      __pycache__/
      env/
      nocopy_dir/
      .gitattributes
      a.txt
      empty
      guild.yml
      hello.py
      hello.pyc

And the copied files:

    >>> run("only-subdir")
    subdir/b.txt
    subdir/logo.png

Alternatively, the subdirectory glob may be omitted. Guild will assume
the glob pattern when the pattern matches an existing directory.

This is illustrated by the `only-subdir2` operation.

    >>> print_config("only-subdir2")
    model-sourcecode:
      dest: .guild/sourcecode
    op-sourcecode: subdir

The preview shows that Guild modified the pattern containing the glob:

    >>> preview("only-subdir2")  # doctest: +REPORT_UDIFF
    Copying from the current directory
    Rules:
      exclude dir .*
      exclude dir * containing .guild-nocopy
      include text * size < 1048577, max match 100
      exclude dir __pycache__
      exclude dir * containing bin/activate
      exclude dir * containing Scripts/activate
      exclude dir build
      exclude dir dist
      exclude dir *.egg-info
      exclude *
      include subdir/*
    Selected for copy:
      subdir/b.txt
      subdir/logo.png
    Skipped:
      .dotdir/
      __pycache__/
      env/
      nocopy_dir/
      .gitattributes
      a.txt
      empty
      guild.yml
      hello.py
      hello.pyc

And the copied files:

    >>> run("only-subdir2")
    subdir/b.txt
    subdir/logo.png

## Including default ignored directories

By default, Guild ignores various directories (see list of excluded
dirs in the previews above). Such directorie can be explicitly
included.

    >>> print_config("include-dotdir")
    model-sourcecode:
      dest: .guild/sourcecode
    op-sourcecode:
    - include:
        dir: .dotdir

    >>> preview("include-dotdir")  # doctest: +REPORT_UDIFF
    Copying from the current directory
    Rules:
      exclude dir .*
      exclude dir * containing .guild-nocopy
      include text * size < 1048577, max match 100
      exclude dir __pycache__
      exclude dir * containing bin/activate
      exclude dir * containing Scripts/activate
      exclude dir build
      exclude dir dist
      exclude dir *.egg-info
      include dir .dotdir
    Selected for copy:
      .gitattributes
      a.txt
      empty
      guild.yml
      hello.py
      .dotdir/a.txt
      subdir/b.txt
    Skipped:
      __pycache__/
      env/
      nocopy_dir/
      hello.pyc
      subdir/logo.png

    >>> run("include-dotdir")
    .dotdir/a.txt
    .gitattributes
    a.txt
    empty
    guild.yml
    hello.py
    subdir/b.txt

## Disabling source code copies

There are multiple ways to disable source code copies altogether.

Using no (False):

    >>> print_config("disabled")
    model-sourcecode:
      dest: .guild/sourcecode
    op-sourcecode: false

    >>> preview("disabled")
    Copying from the current directory
    Rules:
      exclude *
    Source code copy disabled

    >>> run("disabled")
    <empty>

Specifying an emty list of specs:

    >>> print_config("disabled2")
    model-sourcecode:
      dest: .guild/sourcecode
    op-sourcecode: []

    >>> preview("disabled2")
    Copying from the current directory
    Rules:
      exclude *
    Source code copy disabled

    >>> run("disabled2")
    <empty>

Using an exclude spec:

    >>> print_config("disabled3")
    model-sourcecode:
      dest: .guild/sourcecode
    op-sourcecode:
    - exclude: '*'

    >>> preview("disabled3")
    Copying from the current directory
    Rules:
      exclude dir .*
      exclude dir * containing .guild-nocopy
      include text * size < 1048577, max match 100
      exclude dir __pycache__
      exclude dir * containing bin/activate
      exclude dir * containing Scripts/activate
      exclude dir build
      exclude dir dist
      exclude dir *.egg-info
      exclude *
    Source code copy disabled

    >>> run("disabled3")
    <empty>

## Model and op config interactions

Source code config can be specified at the model level as well as the
operaiton level. Model level specs are applied first, followed by op
level specs. This lets operations append rules to the model level
rules, which are evaluated subsequently and therefore can change model
level select behavior.

Model adds png and operation excludes `*.py` and `a.*` files:

    >>> print_config("m1:op")
    model-sourcecode:
      dest: .guild/sourcecode
      select:
      - include: subdir/logo.png
    op-sourcecode:
    - exclude:
      - '*.py'
      - a.*

    >>> preview("m1:op")  # doctest: +REPORT_UDIFF
    Copying from the current directory
    Rules:
      exclude dir .*
      exclude dir * containing .guild-nocopy
      include text * size < 1048577, max match 100
      exclude dir __pycache__
      exclude dir * containing bin/activate
      exclude dir * containing Scripts/activate
      exclude dir build
      exclude dir dist
      exclude dir *.egg-info
      include subdir/logo.png
      exclude *.py, a.*
    Selected for copy:
      .gitattributes
      empty
      guild.yml
      subdir/b.txt
      subdir/logo.png
    Skipped:
      .dotdir/
      __pycache__/
      env/
      nocopy_dir/
      a.txt
      hello.py
      hello.pyc

    >>> run("m1:op")
    .gitattributes
    empty
    guild.yml
    subdir/b.txt
    subdir/logo.png

Model disables source code copy:

    >>> print_config("m2:op1")
    model-sourcecode:
      dest: .guild/sourcecode
      select: false

    >>> preview("m2:op1")
    Copying from the current directory
    Rules:
      exclude *
    Source code copy disabled

    >>> run("m2:op1")
    <empty>

Model disables source code copy but operation re-enables it to copy
only py and yml files.

    >>> print_config("m2:op2")
    model-sourcecode:
      dest: .guild/sourcecode
      select: false
    op-sourcecode:
    - '*.py'
    - '*.yml'

    >>> preview("m2:op2")  # doctest: +REPORT_UDIFF
    Copying from the current directory
    Rules:
      exclude dir .*
      exclude dir * containing .guild-nocopy
      include text * size < 1048577, max match 100
      exclude dir __pycache__
      exclude dir * containing bin/activate
      exclude dir * containing Scripts/activate
      exclude dir build
      exclude dir dist
      exclude dir *.egg-info
      exclude *
      include *.py
      include *.yml
    Selected for copy:
      guild.yml
      hello.py
    Skipped:
      .dotdir/
      __pycache__/
      env/
      nocopy_dir/
      .gitattributes
      a.txt
      empty
      hello.pyc
      subdir/b.txt
      subdir/logo.png

    >>> run("m2:op2")
    guild.yml
    hello.py

Model enables all files to copy:

    >>> print_config("m3:op1")
    model-sourcecode:
      dest: .guild/sourcecode
      select: '*'

    >>> preview("m3:op1")  # doctest: +REPORT_UDIFF
    Copying from the current directory
    Rules:
      exclude dir .*
      exclude dir * containing .guild-nocopy
      include text * size < 1048577, max match 100
      exclude dir __pycache__
      exclude dir * containing bin/activate
      exclude dir * containing Scripts/activate
      exclude dir build
      exclude dir dist
      exclude dir *.egg-info
      exclude *
      include *
    Selected for copy:
      .gitattributes
      a.txt
      empty
      guild.yml
      hello.py
      hello.pyc
      subdir/b.txt
      subdir/logo.png
    Skipped:
      .dotdir/
      __pycache__/
      env/
      nocopy_dir/

    >>> run("m3:op1")  # doctest: +REPORT_UDIFF
    <BLANKLINE>
    .gitattributes
    a.txt
    empty
    guild.yml
    hello.py
    hello.pyc
    subdir/b.txt
    subdir/logo.png

Model enables all files to copy, operation disables source code copy:

    >>> print_config("m3:op2")
    model-sourcecode:
      dest: .guild/sourcecode
      select: '*'
    op-sourcecode: false

    >>> preview("m3:op2")
    Copying from the current directory
    Rules:
      exclude *
    Source code copy disabled

    >>> run("m3:op2")
    <empty>

## Source code for Python scripts

NOTE: This behavior deviates from legacy support because we're not explicit
configuring an alternative source code dest.

When running a Python script, Guild generates a model proxy that is used to run
the script. The proxy uses the default rules for copying source code. As of
Guild 0.9, the default destination directory for source code is '.' (the run
root).

For our sample project, there is no sourcecode configuration for
`hello.py`:

    >>> print_config("hello.py")
    Traceback (most recent call last):
    KeyError: 'hello.py'

Here's the preview:

    >>> preview("hello.py")  # doctest: +REPORT_UDIFF
    Copying from the current directory
    Rules:
      exclude dir .*
      exclude dir * containing .guild-nocopy
      include text * size < 1048577, max match 100
      exclude dir __pycache__
      exclude dir * containing bin/activate
      exclude dir * containing Scripts/activate
      exclude dir build
      exclude dir dist
      exclude dir *.egg-info
    Selected for copy:
      .gitattributes
      a.txt
      empty
      guild.yml
      hello.py
      subdir/b.txt
    Skipped:
      .dotdir/
      __pycache__/
      env/
      nocopy_dir/
      hello.pyc
      subdir/logo.png

Files copied to the legacy location (`.guild/sourcecode` - configured above):

    >>> run("hello.py")
    <empty>

Files in the run root:

    >>> run("hello.py", sourcecode_root=".")
    .gitattributes
    .guild/...
    a.txt
    empty
    guild.yml
    hello.py
    subdir/b.txt

## Alt Sourcecode Destination

The `hello-alt-dest` operation defines an alternative destination for
source code.

Here's the list of source code saved to the default location
(`./guild/sourcecode`):

    >>> run("hello-alt-dest")
    <empty>

Here's the list saved to the configured source code dest for the
operation (`src`):

    >>> run("hello-alt-dest", sourcecode_root="src")
    .gitattributes
    a.txt
    empty
    guild.yml
    hello.py
    subdir/b.txt
