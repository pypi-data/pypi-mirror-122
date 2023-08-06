
[![Build](https://github.com/KnowKit/convmoji/actions/workflows/build.yaml/badge.svg)](https://github.com/KnowKit/convmoji/actions/workflows/build.yaml)
[![codecov](https://codecov.io/gh/KnowKit/convmoji/branch/main/graph/badge.svg?token=84LAM4S1RD)](https://codecov.io/gh/KnowKit/convmoji)
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


# convmoji

A simple cli tool to commit Conventional Commits.

### Install

```bash
pip install convmoji
convmoji --help
```

## Examples

A conventianal commit
````bash
convmoji "epic feature added" feat
````

One with a scope
````bash
convmoji "epic feature added" feat --scope somescope
# ✨: epic feature added
````

With some options
````bash
convmoji "epic feature added" feat --scope somescope --amend --no-verify
# ✨(somescope): epic feature added --amend --no-verify
````

With more textual information
````bash
convmoji "epic feature added" feat --scope somescope \
  --body "more body information" --foot "more footer information"
# ✨(somescope): epic feature added
# 
# more body information
# 
# more footer information
````

Inform people about breaking changes
````bash
convmoji "epic feature added" feat --scope somescope \
  --body "more body information" --footer "more footer information" \
  --breaking-changes "breaks somthing"
# ✨‼️(somescope): epic feature added
# 
# more body information
# 
# BREAKING CHANGE: breaks somthing
# more footer information
````

> If you want to see what to does without performing the action, run it with `--debug`

## Commit types

For details on commit types see [conventional commits specification](https://www.conventionalcommits.org/en/v1.0.0/#specification).

* `feat`: ✨
* `fix`: 🐛
* `docs`: 📚
* `style`: 💎
* `refactor`: 🔨
* `perf`: 🚀
* `test`: 🚨
* `build`: 📦
* `ci`: 👷
* `chore`: 🔧

## convmoji --help

**Usage**:

```console
$ [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `commit`
* `info`

## `commit`

**Usage**:

```console
$ commit [OPTIONS] DESCRIPTION COMMIT_TYPE [SCOPE] [BODY] [FOOTER]
```

**Arguments**:

* `DESCRIPTION`: Commit message, as in 'git commit -m "..."'  [required]
* `COMMIT_TYPE`: Either of [feat, fix, docs, style, refactor, perf, test, build, ci, chore]  [required]
* `[SCOPE]`: Scope for commit (any string)  [default: ]
* `[BODY]`: Body message for commit  [default: ]
* `[FOOTER]`: Footer message (formatted two blank lines below body)  [default: ]

**Options**:

* `--breaking-changes TEXT`: Specially formatted message to show changes might break previous versions  [default: ]
* `-a, --amend`: Execute commit with --amend  [default: False]
* `--no-verify, --nv`: Execute commit with --no-verify  [default: False]
* `--co-authored_by, --co TEXT`: A string of authors formatted like: --co-authored-by '<User user@no-reply> ' --co-authored-by '<User2 user2@no-reply>'
* `--debug / --no-debug`: [default: False]
* `--help`: Show this message and exit.

## `info`

**Usage**:

```console
$ info [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

