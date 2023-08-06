import os
from typing import List, Tuple

from jinja2 import Template, Environment, PackageLoader, select_autoescape

from lupin_grognard.core.commit.commit import Commit
from lupin_grognard.core.tools.utils import write_file


# TEMPLATE_STR = """# Changelog
# {% if commits_fix %}
# ## Fixed
# {% for commit in commits_fix -%}
# - {{ commit }}
# {% endfor %}
# {% endif %}
# {% if commits_feat_add or commits_feat_change or commits_feat_remove %}
# ## Features
# {% endif %}
# {% if commits_feat_add %}
# ### Added
# {% for commit in commits_feat_add -%}
# - {{ commit }}
# {% endfor %}
# {% endif %}
# {% if commits_feat_change %}
# ### Changed
# {% for commit in commits_feat_change -%}
# - {{ commit }}
# {% endfor %}
# {% endif %}
# {% if commits_feat_remove %}
# ### Removed
# {% for commit in commits_feat_remove -%}
# - {{ commit }}
# {% endfor %}
# {% endif %}
# ## Other
# {% for commit in commits_other -%}
# - {{ commit }}
# {% endfor %}
# """


class Changelog:
    def __init__(self, commit_list: List[str]):
        self.commit_list = commit_list

    def generate(self) -> None:
        """Generate changelog"""
        (
            feat_add,
            feat_change,
            feat_remove,
            fix,
            other,
        ) = self._classify_commits_by_type_and_scope()
        self._generate_markdown_file(
            commits_feat_add=feat_add,
            commits_feat_change=feat_change,
            commits_feat_remove=feat_remove,
            commits_fix=fix,
            commits_other=other,
        )

    def _get_local_template(self) -> str:
        env = Environment(loader=PackageLoader('grognard', 'templates'), autoescape=select_autoescape())
        return env.get_template('grog_changelog.j2')


    def _use_local_template_file(self) -> Template:
        """Use a local template file in the root path"""
        template_file_path = os.path.join(os.getcwd(), "CHANGELOG_TEMPLATE.jinja2")
        with open(template_file_path, "r") as f:
            template_str = f.read()
        return Template(template_str)

    def _generate_markdown_file(
        self,
        **commits: List[str],
    ) -> None:
        """Generate changelog markdown file from template and commits list"""
        template = self._get_local_template()
        markdown_str = template.render(commits)
        write_file(file="CHANGELOG.md", content=markdown_str)

    def _append_commit_without_type_scope(
        self, commits: List[str], commit: Commit
    ) -> None:
        """Append commit title without type and scope to commits list"""
        commits.append(commit.title_without_type_scope)

    def _classify_commits_by_type_and_scope(
        self,
    ) -> Tuple[List[str], List[str], List[str], List[str], List[str]]:
        commits_fix = []
        commits_feat_add = []
        commits_feat_change = []
        commits_feat_remove = []
        commits_other = []

        for c in self.commit_list:
            commit = Commit(c)
            match (commit.type, commit.scope):
                case ("feat", "(add)"):
                    self._append_commit_without_type_scope(commits_feat_add, commit)
                case ("feat", "(change)"):
                    self._append_commit_without_type_scope(commits_feat_change, commit)
                case ("feat", "(remove)"):
                    self._append_commit_without_type_scope(commits_feat_remove, commit)
                case ("fix", None):
                    self._append_commit_without_type_scope(commits_fix, commit)
                case (_, _) if commit.type is not None:
                    commits_other.append(commit.title.capitalize())
        return (
            commits_feat_add,
            commits_feat_change,
            commits_feat_remove,
            commits_fix,
            commits_other,
        )
