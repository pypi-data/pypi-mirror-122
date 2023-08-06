import os
import re
from typing import Any, Dict, List

from commitizen import defaults, git
from commitizen.config import BaseConfig
from commitizen.cz.base import BaseCommitizen
from commitizen.cz.exceptions import CzException
from commitizen.cz.utils import multiple_line_breaker, required_validator

__all__ = ["GitJiraConventionalCz"]


class GitJiraConventionalCz(BaseCommitizen):
    bump_pattern = defaults.bump_pattern
    bump_map = defaults.bump_map
    commit_parser = defaults.commit_parser
    changelog_pattern = defaults.bump_pattern

    def __init__(self, config: BaseConfig):
        super().__init__(config)
        if "jira_base_url" not in self.config.settings:
            print(
                "Please add the key jira_base_url to your .cz.yaml|json|toml config file."
            )
            quit()
        if "git_repo" not in self.config.settings:
            print("Please add the key git_repo to your .cz.yaml|json|toml config file.")
            quit()
        self.jira_base_url = self.config.settings["jira_base_url"]
        self.git_repo = self.config.settings["git_repo"]
        self.change_type_map = {
            "feat": "New",
            "fix": "Fix",
            "refactor": "Refactor",
            "perf": "Performance",
        }

    def questions(self) -> List[Dict[str, Any]]:
        questions: List[Dict[str, Any]] = [
            {
                "type": "list",
                "name": "prefix",
                "message": "Select the type of change you are committing",
                "choices": [
                    {
                        "value": "fix",
                        "name": "fix: A bug fix. Correlates with PATCH in SemVer",
                    },
                    {
                        "value": "feat",
                        "name": "feat: A new feature. Correlates with MINOR in SemVer",
                    },
                    {"value": "docs", "name": "docs: Documentation only changes"},
                    {
                        "value": "style",
                        "name": (
                            "style: Changes that do not affect the "
                            "meaning of the code (white-space, formatting,"
                            " missing semi-colons, etc)"
                        ),
                    },
                    {
                        "value": "refactor",
                        "name": (
                            "refactor: A code change that neither fixes "
                            "a bug nor adds a feature"
                        ),
                    },
                    {
                        "value": "perf",
                        "name": "perf: A code change that improves performance",
                    },
                    {
                        "value": "test",
                        "name": (
                            "test: Adding missing or correcting " "existing tests"
                        ),
                    },
                    {
                        "value": "build",
                        "name": (
                            "build: Changes that affect the build system or "
                            "external dependencies (example scopes: pip, docker, npm)"
                        ),
                    },
                    {
                        "value": "ci",
                        "name": (
                            "ci: Changes to our CI configuration files and "
                            "scripts (example scopes: GitLabCI)"
                        ),
                    },
                ],
            },
            {
                "type": "input",
                "name": "scope",
                "message": (f'JIRA issues (multiple "XX-101, XY-102"): '),
                "filter": self.parse_scope,
            },
            {
                "type": "input",
                "name": "subject",
                "filter": self.parse_subject,
                "message": (
                    "Write a short and imperative summary of the code changes: (lower case and no period)\n"
                ),
            },
            {
                "type": "input",
                "name": "body",
                "message": (
                    "Provide additional contextual information about the code changes: (press [enter] to skip)\n"
                ),
                "filter": multiple_line_breaker,
            },
            {
                "type": "confirm",
                "message": "Is this a BREAKING CHANGE? Correlates with MAJOR in SemVer",
                "name": "is_breaking_change",
                "default": False,
            },
            {
                "type": "input",
                "name": "footer",
                "message": (
                    "Footer. Information about Breaking Changes and "
                    "reference issues that this commit closes: (press [enter] to skip)\n"
                ),
            },
        ]
        return questions

    @staticmethod
    def parse_subject(text):
        if isinstance(text, str):
            text = text.strip(".").strip()

        return required_validator(text, msg="Subject is required.")

    def parse_scope(self, text):
        """
        Require and validate the scope to be Jira ids.
        Parse the scope and add Jira prefixes if they were specified in the config.
        """
        issueRE = re.compile(r"\w+-\d+")

        if not text:
            return ""

        issues = [i.strip() for i in text.strip().split(",")]
        for issue in issues:
            if not issueRE.fullmatch(issue):
                raise InvalidAnswerError(f"JIRA scope of '{issue}' is invalid")

        if len(issues) == 1:
            return issues[0]

        return required_validator(
            ",".join([i for i in issues]),
            msg="JIRA scope is required",
        )

    def message(self, answers: dict) -> str:
        prefix = answers["prefix"]
        scope = answers["scope"]
        subject = answers["subject"]
        body = answers["body"]
        footer = answers["footer"]
        is_breaking_change = answers["is_breaking_change"]

        if scope:
            scope = f"({scope})"
        if body:
            body = f"\n\n{body}"
        if is_breaking_change:
            footer = f"BREAKING CHANGE: {footer}"
        if footer:
            footer = f"\n\n{footer}"

        message = f"{prefix}{scope}: {subject}{body}{footer}"

        return message

    def example(self) -> str:
        return (
            "fix: correct minor typos in code\n"
            "\n"
            "see the issue for details on the typos fixed\n"
            "\n"
            "closes issue #12"
        )

    def schema(self) -> str:
        return (
            "<type>(<scope>): <subject>\n"
            "<BLANK LINE>\n"
            "<body>\n"
            "<BLANK LINE>\n"
            "(BREAKING CHANGE: )<footer>"
        )

    def schema_pattern(self) -> str:
        PATTERN = (
            r"(build|ci|docs|feat|fix|perf|refactor|style|test|chore|revert|bump)"
            r"(\(\S+\))?!?:(\s.*)"
        )
        return PATTERN

    def info(self) -> str:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        filepath = os.path.join(dir_path, "conventional_commits_info.txt")
        with open(filepath, "r") as f:
            content = f.read()
        return content

    def process_commit(self, commit: str) -> str:
        pat = re.compile(self.schema_pattern())
        m = re.match(pat, commit)
        if m is None:
            return ""
        return m.group(3).strip()

    def changelog_message_builder_hook(
        self, parsed_message: dict, commit: git.GitCommit
    ) -> dict:
        """add git and jira links to the readme"""
        rev = commit.rev
        m = parsed_message["message"]
        if parsed_message["scope"]:
            parsed_message["scope"] = " ".join(
                [
                    f"[{issue_id}]({self.jira_base_url}/browse/{issue_id})"
                    for issue_id in parsed_message["scope"].split(",")
                ]
            )
        parsed_message[
            "message"
        ] = f"([{rev[:5]}]({self.git_repo}/commit/{commit.rev})) - {m}"
        return parsed_message


class InvalidAnswerError(CzException):
    ...


discover_this = GitJiraConventionalCz
