#!/usr/bin/env python3
"""
Author : Xinyuan Chen <45612704+tddschn@users.noreply.github.com>
Date   : 2023-02-26
Purpose: Generate commit messages using GPT-3.
"""

import argparse
import sys
from .utils import get_diff, generate_commit_message, commit


def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Generate commit messages using GPT-3.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        '-p',
        '--print',
        '--print-message',
        help='Print the generated commit message to stdout instead of committing',
        action='store_true',
    )

    return parser.parse_args()


def main():
    """Make a jazz noise here"""

    args = get_args()
    try:
        diff = get_diff()
        commit_message = generate_commit_message(diff)
    except UnicodeDecodeError:
        print("gpt-commit does not support binary files", file=sys.stderr)
        commit_message = "# gpt-commit does not support binary files. Please enter a commit message manually or unstage any binary files."

    if args.print:
        print(commit_message)
    else:
        exit(commit(commit_message))


if __name__ == '__main__':
    main()
