# A Sample Python Software Project

This README is draft; a starting point for a discussion with the teams involved.
The project contains a module, a command-line script, and a unit test. To install and play around
with

```
git clone
python -m venv v
. v/bin/activate
pip install -e ".[dev]"
```

## Separation of Concerns

A Python project is a separate entity and should work regardless of later packaging for a particular
OS environment. The successful iteration of a development cycle ends with pushing a _wheel_ into
PyPI repository. Further automatic pipelines  may be triggered by this event.

To distinct a change that constites a release, git tags containing a version should be used. A change
in a pipeline file, for example, should not result in releasing a new package. This is not to say such a
change should not be scrutinized in code review. It naturally follows that the OS-specific packaging
should also be triggered based on presence of a specific git tag.

A git repository for each project must be a separate, independent entity. Dependencies should be
handled only through `pyproject.toml` and PiPY as far as Python project as such is concerned. A
test question should be: if I release it to Open Source and push it to global PyPI, will it still work?

## Uniform Project Structure

Uniformty helps both to read and to automate.

`pyproject.toml` should govern the project: metadata, adependencies, "optional" dependencies (testing,
development), CLI utilities, etc. FYI: `setup.cfg` seems to be on its way to
[deprecation](https://github.com/pypa/setuptools/issues/3214). Open the [example pyproject.toml](pyproject.toml)
in a separate tab/window to follow the rest of this section.

Source code of the actual application should reside in a separate subdirectory, `src` being the
common choice.

Unit tests should reside in a separate subdirectory, `tests` being the common choice.

Integration tests should be set apart from unit tests (suggestions as to where and how?)

Dependencies that are not part of the actual software, should handled as "optional" identified as
`dev`. This includes linters, code formatters, testing frameworks and such. 

If a project contains command-line utilities, these should be exposed as such using `pyproject.toml`.
This will resolve issues with hardcoded path to a python interpreter, not to mention clear
documentation of what is available to the end user.

A `Makefile` covering the main tasks: test, build, generate HTML documentation, etc. with uniform
target names. So instead of figuring out, whether `pytest` or `unitttest` or whatever else should be
used, one can just `make test` to run unit tests or `make doc` to generate documentation.

A `.gitignore` file covering generated files and folders.  Non-trivial entries (at least) must be
commented.  Example: In all likelihood, a developer would use a virtual environment.  For
development's sake, the project root is the most natural place for it, but then it should be
git-ignored. Instead of five developers adding their `venv` directory name each to `.gitignore`, one
commented entry should do the trick (see [.gitignore example](.gitignore)).

