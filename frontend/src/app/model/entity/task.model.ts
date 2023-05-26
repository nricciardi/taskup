import { AssignedUserModel } from "./assigned-user.model";
import { BaseEntity } from "./base-entity.model";
import { TaskLabelModel } from "./task-label.model";
import { TaskStatusModel } from "./task-status.model";
import { UserModel } from "./user.model";

export interface TaskModel extends BaseEntity {
  id: number;
  name: string;
  description: string | null;
  deadline: Date | null;
  priority: number;
  created_at: Date;
  updated_at: Date;
  git_branch: string | null;

  author_id: number;
  task_status_id: number;
  author: UserModel | null;
  task_status: TaskStatusModel | null;
  labels: TaskLabelModel[] | null;
  assigned_users: AssignedUserModel[] | null;
}


export interface BlueprintTaskModel {
  id?: number;
  name?: string;
  description?: string | null;
  deadline?: Date | null;
  priority?: number;
  created_at?: Date;
  updated_at?: Date;
  git_branch?: string | null;

  author_id?: number;
  task_status_id?: number;
  author?: UserModel | null;
  task_status?: TaskStatusModel | null;
  labels?: TaskLabelModel[] | null;
  assigned_users?: AssignedUserModel[] | null;
}

export interface NewTaskModel {
  name: string;
  description?: string;
  priority: number;
  author_id: number;
  task_status_id: number;
}
