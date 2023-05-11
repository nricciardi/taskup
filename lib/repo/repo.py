import git
from dataclasses import dataclass, field
from lib.utils.logger import Logger
from datetime import datetime
from lib.db.entity.user import UserModel
from typing import Tuple


@dataclass
class Author:
    email: str
    name: str
    associated_user: UserModel


@dataclass
class RepoNode:
    hexsha: str
    author: Author
    message: str
    committed_at: datetime
    parents: Tuple['RepoNode']
    children: Tuple['RepoNode']
    # tag: str


class RepoManager:
    def __init__(self, repo_path: str, verbose: bool = False):
        self.repo_path = repo_path
        self.verbose = verbose
        self.repo = git.Repo(self.repo_path)

    def generate_tree(self):

        tree = self.repo.tree().tra

        print(tree)

        return

        commits = list(self.repo.iter_commits(reverse=True))

        for commit in commits:
            print(commit.hexsha)
            print(commit.message)
            print(commit.parents)
            print("---")


if __name__ == '__main__':
    path = "/home/ncla/Desktop/data/uni/programmazione-ad-oggetti/project/test/repo-test"
    repo_manager = RepoManager(path, True)

    repo_manager.generate_tree()
