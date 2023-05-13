export interface RepoNode {
  hexsha: string;
  author: Author;
  message: string;
  committed_at: Date;
  parents: RepoNode[] | null;
  children: RepoNode[] | null;
  of_branch: string;
}

export interface Author {
  email: string;
  name: string;
}

