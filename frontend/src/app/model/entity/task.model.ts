import { TaskLabelModel } from "./task-label.model";
import { TaskStatusModel } from "./task-status.model";
import { UserModel } from "./user.model";

export interface TaskModel {
  id: number;
  name: string;
  description?: string;
  deadline?: Date;
  priority: number;
  created_at: Date;
  updated_at: Date;

  author_id: number;
  task_status_id: number;
  author?: UserModel;
  task_status?: TaskStatusModel;
  labels?: TaskLabelModel[];
}
