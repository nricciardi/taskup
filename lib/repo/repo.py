import git
from dataclasses import dataclass


# @dataclass
# class RepoNode:
#     binsha: str
#     author:


class RepoManager:
    def __init__(self, repo_path: str, verbose: bool = False):
        self.repo_path = repo_path
        self.verbose = verbose


if __name__ == '__main__':
    print(git)