import { TaskModel } from "./task.model";
import { UserModel } from "./user.model";

export interface TodoItemModel {
  id: number;
  description: string;
  deadline: Date | null;
  created_at: Date;
  updated_at: Date;
  done: boolean;

  author_id: number;
  task_id: number;
  author: UserModel | null;
  task: TaskModel | null;
}
