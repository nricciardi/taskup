import { TaskLabelModel } from "./task-label.model";
import { TaskStatusModel } from "./task-status.model";
import { UserModel } from "./user.model";

export interface TaskModel {
  id: number;
  name: string;
  description: string | null;
  deadline: Date | null;
  priority: number;
  created_at: Date;
  updated_at: Date;

  author_id: number;
  task_status_id: number;
  author: UserModel | null;
  task_status: TaskStatusModel | null;
  labels: TaskLabelModel[] | null;
  users: UserModel[] | null;
}
