export interface RepoNode {
  hexsha: string;
  author: Author;
  message: string;
  committed_at: Date;
  parents: RepoNode[] | null;
  children: RepoNode[] | null;
}

export interface Author {
  email: string;
  name: string;
}
