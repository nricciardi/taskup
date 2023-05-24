export interface RepoNode {
  hexsha: string;
  author: Author;
  message: string;
  committed_at: Date;
  parents: RepoNode[] | null;
  children: RepoNode[] | null;
  of_branch: string;
  tag: string;
  associated_task_id: number[] | null;
}

export interface Author {
  email: string;
  name: string;
  associated_user_id: number | null;
}

