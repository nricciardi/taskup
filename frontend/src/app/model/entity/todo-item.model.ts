import { TaskModel } from "./task.model";
import { UserModel } from "./user.model";

export interface TodoItemModel {
  id: number;
  description: string;
  deadline: Date | null;
  priority: number;
  created_at: Date;
  updated_at: Date;

  author_id: number;
  task_id: number;
  author: UserModel | null;
  task: TaskModel | null;
}
