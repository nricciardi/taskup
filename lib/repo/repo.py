import git
import json
from dataclasses import dataclass, field, asdict
from lib.utils.logger import Logger
from datetime import datetime
from lib.db.entity.user import UserModel
from typing import List, Union, Optional
import copy
from lib.utils.mixin.dcparser import DCToDictMixin


@dataclass
class Author:
    email: str
    name: str
    # associated_user: UserModel


@dataclass
class RepoNode(DCToDictMixin):
    hexsha: str
    author: Author
    message: str
    committed_at: str
    parents: Optional[List['RepoNode']] = field(default=None)     # if None => no information, but it is said that there are no fathers
    children: Optional[List['RepoNode']] = field(default=None)

    # tag: str

    def add_child(self, node: 'RepoNode') -> None:
        """
        Add child to node

        :param node:
        :return:
        """

        if self.children is None:
            self.children = []

        self.children.append(node)

    @staticmethod
    def add_node_to_parent(source_node: 'RepoNode', node_to_add: 'RepoNode') -> None:
        """
        Add node in the tree, it may not be the direct child

        :param source_node:
        :param node_to_add:
        :return:
        """

        for parent in node_to_add.parents:
            nodes: List['RepoNode'] = RepoNode.search_node_by_hexsha(source_node, parent.hexsha)

            for node in nodes:
                node.add_child(node_to_add)

    @classmethod
    def from_commit(cls, commit: git.Commit, parents_depth: int = 1) -> 'RepoNode':
        """
        Generate a node from a commit

        :param parents_depth: fathers research depth
        :param commit:
        :return:
        """

        parents: Optional[List['RepoNode']] = None

        if parents_depth > 0:
            parents = []

            for p in commit.parents:
                parents.append(RepoNode.from_commit(p, parents_depth - 1))

        node = cls(hexsha=commit.hexsha,
                   author=Author(email=commit.author.email,
                                 name=commit.author.name),
                   message=commit.message,
                   committed_at=commit.committed_datetime.isoformat(),
                   parents=parents,
                   children=[]
                   )

        return node

    @staticmethod
    def copy_of(node: 'RepoNode') -> 'RepoNode':
        """
        Return a copy of passed node

        :param node:
        :return:
        """

        return copy.deepcopy(node)

    @staticmethod
    def search_node_by_hexsha(node: 'RepoNode', hexsha: str, _partial_result: Optional[List] = None) -> List:
        """
        Search all occurrences of child node of a source node by its hexsha

        :param _partial_result:
        :param node:
        :param hexsha:
        :return:
        """

        if _partial_result is None:
            _partial_result = []       # init empty

        if node.hexsha == hexsha:       # found node
            _partial_result.append(node)

        for child in node.children:
            RepoNode.search_node_by_hexsha(node=child, hexsha=hexsha, _partial_result=_partial_result)

        return _partial_result


class RepoManager:
    def __init__(self, repo_path: str, verbose: bool = False):
        self.repo_path = repo_path
        self.verbose = verbose
        self.repo = git.Repo(self.repo_path)

    def generate_tree(self):

        Logger.log_info(msg=f"Generate repo tree...", is_verbose=self.verbose)

        commits = list(self.repo.iter_commits(reverse=True))

        # take root commit: always the first of the list
        root_commit = commits.pop(0)

        root_node = RepoNode.from_commit(root_commit)

        # for each commit search its parents, at each parent append the commit
        for commit in commits:

            new_node = RepoNode.from_commit(commit)

            RepoNode.add_node_to_parent(root_node, new_node)

        Logger.log_success(msg=f"tree generated successfully", is_verbose=self.verbose)

        return root_node


if __name__ == '__main__':
    path = "/home/ncla/Desktop/project/project-pi/code/fakerepo"
    repo_manager = RepoManager(path, True)

    root_node = repo_manager.generate_tree()

    j = json.dumps(root_node.to_dict(), indent=4)

    print(j)