import git
from dataclasses import dataclass, field
from lib.utils.logger import Logger
from lib.db.entity.user import UserModel
from lib.db.entity.task import TaskModel
from typing import List, Set, Optional, Dict
import copy
from lib.utils.mixin.dcparser import DCToDictMixin
from lib.utils.utils import Utils
from pprint import pprint
from time import time

# global variables to pass associations to RepoNode dataclass
associations_commits_tags: Dict[str, str] = dict()  # hexsha - tag's name
associations_commits_branches: Dict[str, str] = dict()     # hexsha - branch
associations_commits_users: Dict[str, int] = dict()         # email - user_id
associations_commits_tasks: Dict[str, List[int]] = dict()         # branch - [task_id]


@dataclass
class Author:
    email: str
    name: str
    associated_user_id: Optional[int] = field(default=None)


@dataclass
class RepoNode(DCToDictMixin):
    hexsha: str
    author: Author
    message: str
    committed_at: str
    of_branch: str
    parents: Optional[List['RepoNode']] = field(default=None)     # if None => no information, but it is said that there are no fathers
    children: Optional[List['RepoNode']] = field(default=None)
    tag: Optional[str] = field(default=None)
    associated_task_id: Optional[List[int]] = field(default=None)

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
    def from_commit(cls, commit: git.Commit, parents_depth: int = 1) -> 'RepoNode':
        """
        Generate a node from a commit

        :param parents_depth: fathers research depth
        :param commit:
        :return:
        """

        global associations_commits_tags
        global associations_commits_branches
        global associations_commits_users
        global associations_commits_tasks

        parents: Optional[List['RepoNode']] = None

        if parents_depth > 0:
            parents = []

            for p in commit.parents:
                parents.append(RepoNode.from_commit(p, parents_depth=parents_depth - 1))

        branch = associations_commits_branches.get(commit.hexsha)
        if associations_commits_branches.get(commit.hexsha) is None:
            Logger.log_warning(msg=f"{commit} has not an explicit associated branch", is_verbose=True)

            branch = commit.name_rev.split(" ")[1].split("~")[0]

        node = cls(hexsha=commit.hexsha,
                   author=Author(email=commit.author.email,
                                 name=commit.author.name,
                                 associated_user_id=associations_commits_users.get(commit.author.email)
                                 ),
                   message=commit.message,
                   committed_at=commit.committed_datetime.isoformat(),
                   parents=parents,
                   children=None,
                   of_branch=branch,
                   tag=associations_commits_tags.get(commit.hexsha),
                   associated_task_id=associations_commits_tasks.get(branch)
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
    def search_node_by_hexsha(node: 'RepoNode', hexsha: str, _partial_result: Optional[List] = None, _visited: Optional[Set] = None) -> List['RepoNode']:
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
    def __init__(self, verbose: bool = False, users_models: List[UserModel] = None, tasks_models: List[TaskModel] = None):
        global associations_commits_tasks
        global associations_commits_users

        if isinstance(users_models, list):
            associations_commits_users = dict()
            for user in users_models:
                associations_commits_users[user.email] = user.id

        if isinstance(tasks_models, list):
            associations_commits_tasks = dict()
            for task in tasks_models:
                if associations_commits_tasks.get(task.git_branch) is None:
                    associations_commits_tasks[task.git_branch] = [task.id]

                else:
                    associations_commits_tasks[task.git_branch].append(task.id)

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

    def get_tree(self) -> Optional[RepoNode]:
        """
        Generate repo tree

        :return:
        """

        if not self.valid_opened_repo():
            return None

        Logger.log_info(msg=f"Generate repo tree...", is_verbose=self.verbose)

        all_repo_commits = list(self.repo.iter_commits('--all', reverse=True))

        if len(all_repo_commits) == 0:
            Logger.log_warning(msg="repo is empty", is_verbose=self.verbose)
            return None

        # take root commit: always the first of the list
        root_node = RepoNode.from_commit(all_repo_commits.pop(0))       # root is removed

        for commit in all_repo_commits:

            commit_node = RepoNode.from_commit(commit)

            # append a repo node in each parent
            for parent in commit.parents:
                parent_nodes = RepoNode.search_node_by_hexsha(root_node, parent.hexsha)

                for pn in parent_nodes:
                    pn.add_child(commit_node)

        Logger.log_success(msg=f"tree generated successfully", is_verbose=self.verbose)

        pprint(root_node)

        return root_node

    def get_commits(self) -> List[RepoNode] | None:
        """
        Return list of project's repository commits

        :return:
        """

        if not self.valid_opened_repo():
            Logger.log_warning(msg="impossible to elaborate commits: repo not found", is_verbose=self.verbose)
            return None

        Logger.log_info(msg=f"start to fetch commits from project repo...", is_verbose=self.verbose)

        self.repo.git.fetch()

        # take tags of repo
        global associations_commits_tags
        associations_commits_tags = dict()  # hexsha - tag's name
        for tag in list(self.repo.tags):
            associations_commits_tags[tag.commit.hexsha] = tag.name

        Logger.log_info(msg=f"fetched {len(associations_commits_tags.keys())} tags", is_verbose=self.verbose)

        # get references of local and remote branches
        branches = list(self.repo.branches)

        if self.repo.remotes:
            branches.extend(self.repo.remote().refs)

        Logger.log_info(msg=f"fetched {len(branches)} branch(es)", is_verbose=self.verbose)

        # take association between commits hexsha and its branch
        global associations_commits_branches
        associations_commits_branches = dict()     # hexsha - branch
        for branch in branches:
            hexsha_of_commits = set(commit.hexsha for commit in list(self.repo.iter_commits(branch, reverse=True)))

            for hexsha in hexsha_of_commits:
                if associations_commits_branches.get(hexsha) is None:
                    associations_commits_branches[hexsha] = str(branch)

        Logger.log_info(msg=f"fetched data of {len(associations_commits_branches.keys())} commit(s)", is_verbose=self.verbose)

        # # pprint(associations_commits_tags)
        # print()
        # # pprint(associations_commits_branches)
        # print(len(associations_commits_branches))
        # print("\n\n\n")
        # print("41071ed81b2125e9a215ac9934b3e870bba50426" in associations_commits_branches)
        # print(len(list(self.repo.iter_commits('--all', reverse=True))))
        # Utils.exit()

        # generate list of nodes
        all_repo_commits = list(self.repo.iter_commits('--all', reverse=True))
        nodes = list()      # use a managed list to share data between processes
        n_of_commits = len(all_repo_commits)
        start = time()
        for i in range(n_of_commits):
            commit = all_repo_commits[i]
            repo_node: RepoNode = RepoNode.from_commit(commit)

            # search children of commit
            for j in range(i, n_of_commits):
                candidate_child_commit = all_repo_commits[j]
                candidate_child_node: RepoNode = RepoNode.from_commit(candidate_child_commit)

                if repo_node.hexsha in (parent.hexsha for parent in candidate_child_node.parents):
                    repo_node.add_child(candidate_child_node)

            nodes.append(repo_node)

            Logger.log_info(msg=f"elaborating commit {i+1}/{n_of_commits} ({round((i + 1) * 100 / n_of_commits, 2)}%)", is_verbose=self.verbose)

        Logger.log_success(msg=f"commits fetched successfully in {round(time() - start, 4)}s", is_verbose=self.verbose)
        return list(nodes)


if __name__ == '__main__':
    path = "/home/ncla/Desktop/data/uni/programmazione-ad-oggetti/project/test/repo-test"
    path = "/home/ncla/Desktop/data/uni/programmazione-ad-oggetti/project/Eel"
    path = "/home/ncla/Desktop/data/uni/programmazione-ad-oggetti/project/mypy"
    repo_manager = RepoManager(True)

    repo_manager.open_repo(path)

    pprint(len(repo_manager.get_commits()))