# A Sample Python Software Project

This README is draft; a starting point for a discussion with the teams involved.
The project contains a module, a command-line script, and a unit test. To install and play around
with

```
git clone git@gitlab.pb.local:tvendelin/python-project-template.git && cd python-project-template
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

A `.gitignore` file covering generated files and folders.  Non-trivial entries (at least) must be
commented.  Example: In all likelihood, a developer would use a virtual environment.  For
development's sake, the project root is the most natural place for it, but then it should be
git-ignored. Instead of five developers adding their `venv` directory name each to `.gitignore`, one
commented entry should do the trick (see [.gitignore example](.gitignore)).

## Goals and Means, or Which Tools to Use?

The goals are important, the means less so.

Valid goals for a software could be:
- it should work according to the requirements
- it should comply with coding standards 
- it should have a reasonable test coverage
- the API documentation can be extracted from source code and generated as HTML
- the automatic build pipelines should work without unnecessary tweaking

On the other hand, it doesn't matter much, which framework is used to run the unit tests, or whether
the HTML documentation is generated with `Sphynx` or `pydoc`. 

### Indirection Using Makefile

A project should contain a `Makefile` with standard, mandatory, intuitive target names. This
facilitates simpler CI/CD pipelines. The following commands hardly need any explanations:

```
make test
make coverage
make doc
make build
```

On the other hand, amounts of time saved by avoiding `unittest` over `pytest` or `setuptools` over
`poetry` arguments would be substantial.

### Code Formatters

By contrast with the above, these should be the same across the team(s), and be set up in build
pipeline directly. Care should be taken to exclude the tools with overlapping functionality, i.e.,
if the code formatted with `black` is always PEP8-compliant, do we need `flake8`?

## Version and Releases

The last annotated git tag that complies to version format is the single source of truth regarding
the software being released. The Python wheel version as well as OS-specific package version should
be generated based on that.

### `pyproject.toml`

Allows dynamic version specification, and there are several tools/plugins supporting this
functionality. In this project, `setuptools-git-versioning` is used, but even with `setuptools`,
this is not the only option.

### `debian/changelog`

The project includes [`changelog.sh`](build_scripts/changelog.sh) script that generates the contents
of `debian/changelog` file based on annotated git tags. The only limitation is that metadata field
is set statically to `urgency=medium`. This _can_ be implemented, but so far we haven't used it for
any practical purpose.  According to
[deb-changelog(5)](https://manpages.debian.org/testing/dpkg-dev/deb-changelog.5.en.html),

>metadata lists zero or more comma-separated keyword=value items

meaning the field is optional anyway.

### What if...

Q: Someone changes/deletes a version tag? 

A: While it is technically possible, it must be a deliberate two-step action: 
- delete the tag locally
- push the change to upstream

In that sense, it hardly differs from manual modification of static text file.

Apart from that, Gitlab at least offers a "protected tag" feature. While changing a tag pushed to
upstream remains possible, it requires maintainer access rights and involves some fiddling.
