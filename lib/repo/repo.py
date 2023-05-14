import git
import json
from dataclasses import dataclass, field
from lib.utils.logger import Logger
from datetime import datetime
from lib.db.entity.user import UserModel
from typing import List, Set, Optional
import copy
from lib.utils.mixin.dcparser import DCToDictMixin
from lib.utils.utils import Utils


@dataclass
class RepoCommit:
    branch_name: str
    commit: git.Commit




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
    of_branch: str
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
    def add_node_to_parent(source_node: 'RepoNode', node_to_add: 'RepoNode') -> bool:
        """
        Add node in the tree, it may not be the direct child

        :param source_node:
        :param node_to_add:
        :return:
        """

        for parent in node_to_add.parents:
            nodes: List['RepoNode'] = RepoNode.search_node_by_hexsha(source_node, parent.hexsha)

            if len(nodes) == 0:
                return False

            for node in nodes:
                node.add_child(node_to_add)

        return True

    @classmethod
    def from_commit(cls, commit: git.Commit, branch_name: Optional[str], parents_depth: int = 1) -> 'RepoNode':
        """
        Generate a node from a commit

        :param branch_name:
        :param parents_depth: fathers research depth
        :param commit:
        :return:
        """

        parents: Optional[List['RepoNode']] = None

        if parents_depth > 0:
            parents = []

            for p in commit.parents:
                parents.append(RepoNode.from_commit(p, None, parents_depth - 1))

        node = cls(hexsha=commit.hexsha,
                   author=Author(email=commit.author.email,
                                 name=commit.author.name),
                   message=commit.message,
                   committed_at=commit.committed_datetime.isoformat(),
                   parents=parents,
                   children=[],
                   of_branch=branch_name
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
    def search_node_by_hexsha(node: 'RepoNode', hexsha: str, _partial_result: Optional[List] = None, _visited: Optional[Set] = None) -> List:
        """
        Search all occurrences of child node of a source node by its hexsha

        :param _visited:
        :param _partial_result:
        :param node:
        :param hexsha:
        :return:
        """

        if _partial_result is None:
            _partial_result = []       # init empty

        if _visited is None:
            _visited = set()     # init empty

        if node.hexsha == hexsha:       # found node
            _partial_result.append(node)

        _visited.add(id(node))

        for child in node.children:
            if id(child) not in _visited:
                RepoNode.search_node_by_hexsha(node=child, hexsha=hexsha, _partial_result=_partial_result, _visited=_visited)

        return _partial_result


class RepoManager:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose

        self.repo: Optional[git.Repo] = None

    def open_repo(self, project_path: str) -> None:
        """
        Open repo

        :param project_path:
        :return:
        """

        try:
            self.repo = git.Repo(project_path)

        except git.exc.InvalidGitRepositoryError:
            Logger.log_warning(msg=f"invalid repository in '{project_path}'", is_verbose=self.verbose)
            self.repo = None

        except Exception:
            Logger.log_warning(msg=f"unable to open repository '{project_path}'", is_verbose=self.verbose)
            self.repo = None

    def valid_opened_repo(self) -> bool:
        """
        Return True if a valid repository is opened

        :return:
        """

        return self.repo is not None

    def generate_tree(self) -> Optional[RepoNode]:
        """
        Generate repo tree

        :return:
        """

        if not self.valid_opened_repo():
            return None

        Logger.log_info(msg=f"Generate repo tree...", is_verbose=self.verbose)

        all_repo_commits = set()
        for branch in self.repo.references:
            commits: List[git.Commit] = list(self.repo.iter_commits(branch, reverse=True))

            commits: List[RepoCommit] = list(map(lambda c: RepoCommit(branch_name=str(branch), commit=c), commits))

            all_repo_commits.update(commits)

        # set of visited commit
        visited = set()

        # take root commit: always the first of the list
        root_node: Optional[RepoNode] = None
        for repo_commit in all_repo_commits:
            if len(repo_commit.commit.parents) == 0:
                root_commit = repo_commit.commit

                root_node = RepoNode.from_commit(root_commit, branch_name=repo_commit.branch_name)

                visited.add(repo_commit.commit.hexsha)

                break

        if root_node is None:
            Logger.log_warning(msg="repo root not found", is_verbose=self.verbose)
            return

        # for each commit search its parents, at each parent append the commit
        import time
        start = time.time()
        while len(visited) != len(all_repo_commits):

            # len(visited) : len(all_commits) = x : 100
            perc: float = len(visited) * 100 / len(all_repo_commits)
            Logger.log_info(msg=f"{len(visited)}/{len(all_repo_commits)}: {round(perc, 2)}% {round(time.time() - start, 4)}s", is_verbose=self.verbose)

            for repo_commit in all_repo_commits:

                if repo_commit.commit.hexsha in visited:
                    continue

                new_node = RepoNode.from_commit(repo_commit.commit, repo_commit.branch_name)

                if RepoNode.add_node_to_parent(root_node, new_node):
                    visited.add(repo_commit.commit.hexsha)

        Logger.log_success(msg=f"tree generated successfully", is_verbose=self.verbose)

        return root_node


if __name__ == '__main__':
    path = "/home/ncla/Desktop/project/project-pi/Eel"
    path = "/home/ncla/Desktop/project/project-pi/code/fakerepo"
    repo_manager = RepoManager(True)

    repo_manager.open_repo(path)

    root_node = repo_manager.generate_tree()

    j = json.dumps(root_node.to_dict(), indent=4)

    print(j)