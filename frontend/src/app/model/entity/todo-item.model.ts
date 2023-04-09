import { TaskModel } from "./task.model";
import { UserModel } from "./user.model";

export interface TodoItemModel {
  id: number;
  name: string;
  description: string;
  deadline: Date;
  priority: number;
  created_at: Date;
  updated_at: Date;

  author_id: number;
  task_id: number;
  author: UserModel;
  task: TaskModel;
}
