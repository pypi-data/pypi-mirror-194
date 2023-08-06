import re
from datetime import datetime
from typing import List

from lupin_grognard.core.config import PATTERN
from lupin_grognard.core.git import Git


class Commit:
    def __init__(self, commit: str):
        self.commit = commit
        self.git = Git()

    @property
    def hash(self) -> str:
        return self._extract(start="hash>>")

    @property
    def author(self) -> str:
        return self._extract(start="author>>")

    @property
    def author_mail(self) -> str:
        return self._extract(start="author_mail>>")

    @property
    def author_date(self) -> str:
        timestamp = self._extract(start="author_date>>")
        date_object = datetime.fromtimestamp(int(timestamp))
        return date_object.strftime("%A %d %B %Y %H:%M:%S")

    @property
    def title(self) -> str:
        return self._extract(start="title>>")

    @property
    def title_without_type_scope(self) -> str:
        """Returns commit title without type and scope"""
        start = self.title.find(":") + 1
        return self.title[start:].strip().capitalize()

    @property
    def type(self) -> str | None:
        """Returns the conventional commit type if present"""
        match = re.match(PATTERN, self.title)
        return match.groups()[0] if match else None

    @property
    def scope(self) -> str | None:
        """Returns the conventional commit scope if present"""
        match = re.match(PATTERN, self.title)
        return match.groups()[1] if match else None

    @property
    def body(self) -> List[str] | None:
        body = self._extract(start="body>>", end="<<body")
        if body == "":
            return None
        return [message for message in body.split("\n") if len(message) > 0]

    @property
    def closes_issues(self) -> str | None:
        if self.body:
            for line in self.body:
                if line.startswith("Closes #"):
                    return line.split("Closes #")[1]
        return None

    @property
    def approvers(self) -> List[str]:
        approvers = []
        if self.body:
            for line in self.body:
                if line.startswith("Approved-by: "):
                    approvers.append(line.split("Approved-by: ")[1])
            return approvers
        return list()

    @property
    def tag(self) -> str | None:
        return self.git.get_commit_tag(self.hash)

    def _extract(self, start: str, end: str = "\n") -> str:
        start_index = self.commit.find(start) + len(start)
        return self.commit[start_index:self.commit.find(end, start_index)]
