import { BaseEntity } from "./base-entity.model";
import { TaskModel } from "./task.model";
import { UserModel } from "./user.model";

export interface TodoItemModel extends BaseEntity {
  id: number;
  description: string;
  deadline: Date | null;
  created_at: Date;
  updated_at: Date;
  done: boolean;
  priority: number;

  author_id: number;
  task_id: number;
  author: UserModel | null;
  task: TaskModel | null;
}

export interface NewTodoItemModel {
  description: string;
  deadline: Date | null;
  priority: number;
}
