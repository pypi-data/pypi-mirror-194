# gpt-commit

Generate commit messages using GPT-3. To use `gpt-commit`, simply invoke it whenever you'd use `git commit`. Git will prompt you to edit the generated commit message.

```bash
git add .
gpt-commit
```

Based on Markus' [gpt-commit](https://github.com/markuswt/gpt-commit).

- [gpt-commit](#gpt-commit)
  - [Installation](#installation)
    - [pipx](#pipx)
    - [pip](#pip)
  - [Getting Started](#getting-started)
  - [Develop](#develop)


## Installation

Minimum Python version required: 3.10.

### pipx

This is the recommended installation method.

```
$ pipx install gpt-commit-cli
```

### [pip](https://pypi.org/project/gpt-commit-cli/)

```
$ pip install gpt-commit-cli
```


## Getting Started

Set the environment variable `OPENAI_API_KEY` to your [OpenAI API key](https://platform.openai.com/account/api-keys), e.g. by adding the following line to your `.bashrc`.

```bash
export OPENAI_API_KEY=<YOUR API KEY>
export OPENAI_ORG_ID=<YOUR ORG ID> # optional
```

<!-- ### Modify `git commit` (optional)

If you want `git commit` to automatically invoke `gpt-commit`, copy `gpt-commit.py` and `prepare-commit-msg` to the `.git/hooks` directory in any project where you want to modify `git commit`.
 -->

## Develop

```
$ git clone https://github.com/tddschn/gpt-commit-cli.git
$ cd gpt-commit-cli
$ poetry install
```