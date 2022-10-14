# A Sample Python Software Project

A trivial pure-Python boilerplate project aiming to pull together some sensible practices to
develop, test, document, build and deploy a modern (as of 2022) Python project.

This is a work in progress and should be seen as a starting point of a discussion.


The project contains a module with a dependency, a command-line script, and a unit test. To install
and play around with

```bash
git clone git@gitlab.pb.local:tvendelin/python-project-template.git && cd python-project-template

# This will create a Python virtual environment. Your local system setups should not be affected.
make bootstrap

. v/bin/activate
```

[[_TOC_]]

## Separation of Concerns

The aim of a Python project is to produce a _wheel_ and publish it to a PyPI
package registry, internal or global.

Further OS-specific packaging should be handled asynchronously. This allows the developers to
continue their work even in the presence of some issues downstream. Example: new dependencies have
been introduced to the project, but no all of them exist in a form of a Debian package. Creation of
the said packages is deferred, the development continues. Later on it turns out that some of the new
dependencies are not necessary after all, their packaging is now skipped, saving a few man-hours. 

Building and publishing either Python-native or OS packages should be triggered based on annotated
git tags. 

A git repository for each project must be a separate, independent entity. Dependencies should be
handled only through `pyproject.toml` and PyPI as far as Python project as such is concerned. A test
question should be: "If I release it to Open Source and push it to global PyPI, will it still work?"

## Uniform Project Structure

Uniformity helps both to read and to automate.

The project is governed by a single `pyproject.toml` file. This covers metadata, dependencies,
"optional" dependencies (testing, development), CLI utilities, etc. Most development tools that we
use accept configuration from PyPI.  `flake8` is the only notable exception, but it is also
redundant if `black` and `pylint` are used. FYI: `setup.cfg` seems to be on its way to
[deprecation](https://github.com/pypa/setuptools/issues/3214). 

Open the [example pyproject.toml](pyproject.toml)
in a separate tab/window to follow the rest of this section.

### Separate Folders for Software Proper ("Sources"), Unit Tests, etc. 
Source code of the actual application should reside in a separate substructure, `src` being the
common choice.

Unit tests should reside in a separate sub directory, `tests` being the common choice.

Integration tests should be set apart from unit tests (suggestions as to where and how?)

Dependencies that are not part of the actual software, should handled as "optional" identified as
`dev`. This includes linters, code formatters, testing frameworks and such. 

### Expose CLI Utilities 

Should a project provide command-line utilities, expose the respective functions from
the `[project.scripts]` section of `pyproject.toml`. This will create the wrapper scripts in the
`$PATH` regardless of whether `pip` or `apt-get` is used. This approach takes path to Python
interpreter out of the equation completely. Neither is there any need for creating a separate module
for each script.

Add a CLI utility that lists the CLI utilities provided by your package - with short descriptions. 
The most natural way would probably be to call `mypackage -h` for the purpose. 

### A Commented `.gitignore`

Non-trivial entries (at least) must be commented.  Example: In all likelihood, a developer would use
a virtual environment.  For development's sake, the project root is the most natural place for it,
but then it should be git-ignored. Instead of five developers adding their `venv` directory name
each to `.gitignore`, one commented entry should do the trick (see [.gitignore
example](.gitignore)).

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
facilitates simpler CI/CD pipelines. The suggested targets are (see [Makefile](Makefile))

```bash
# Create a virtual environment and install for development
make bootstrap
# Create documentation in HTML
make html
# Run code formatters and linters
make tidy

make clean
make test
make coverage
make dist
make upload
```

Do not add `install` target as it will interfere with Debian tools.

This gives teams/developers more flexibility over which tools to use, reducing disputes like
`unittest` over `pytest` or `setuptools` over `poetry`.

### Code Formatters

By contrast with the above, these should be the same across the team(s), and be set up in build
pipeline directly. Care should be taken to exclude the tools with overlapping functionality, i.e.,
if the code formatted with `black` is always PEP8-compliant, do we need `flake8`?

## Version and Releases

The last annotated git tag that complies to version format is the single source of truth regarding
the software being released. The Python wheel version as well as OS-specific package version should
be generated based on that. `pyproject.toml` allows for dynamic versioning, and many existing
project management tools (`setuptools >= 61`, `poetry`, to name a few), support that functionality
as well either directly, or with a plugin. In this project, `setuptools-git-versioning` is used, but
even with `setuptools` alone, this is not the only option.

### `debian/changelog`

The project includes [`changelog.sh`](build_scripts/changelog.sh) script that generates the contents
of `debian/changelog` file based on annotated git tags. The only limitation is that metadata field
is set statically to `urgency=medium`. This _can_ be implemented, but so far we haven't used it for
any practical purpose.  According to
[deb-changelog(5)](https://manpages.debian.org/testing/dpkg-dev/deb-changelog.5.en.html),

>metadata lists zero or more comma-separated keyword=value items

meaning the field is optional anyway.

## 100% Test Coverage

There are plenty of valid reasons for some code not being covered by unit tests. However, instead of
agreeing on a certain lower test coverage percentage (based on what?), one should instead configure
exclusions based on rational, case-by-case justifications. As far as `coverage.py` is concerned, the
exclusions can be configured both as regexps in `pyproject.toml` and as pragmas in the code
directly.

## Publishing a Python Package

Create a separate project in Gitlab that will be used as a PyPI package registry only. This should
be accessible for all teams and groups probably. More than one such projects (essentially PyPI
package registries) could be created to distinct between releases and snapshot builds.

Obtain a personal access token (User > Preferences > Access Tokens) with a descriptive name.

Create a `$HOME/.pypirc` and `$HOME/.config/pip/pip.conf` files. This project contains a PyPI index
for the sake of example. The configuration files should be similar to

```
# $HOME/.pypirc

[distutils]
index-servers =
    gitlab

[gitlab]
repository = https://gitlab.pb.local/api/v4/projects/2354/packages/pypi
username = your_token_name
password = y0Ur-t0ken
```

and 

```
# $HOME/.config/pip/pip.conf
[global]
index-url = https://your_token_name:y0Ur-t0ken@gitlab.pb.local/api/v4/projects/2354/packages/pypi/simple
```

If a package is not found in our internal index, Gitlab will forward the request to the global PyPI. Since `pip` does not prioritize repositories, using `extra-index-url` is a security risk (code injection).
