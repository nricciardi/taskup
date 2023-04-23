import { TaskModel } from "./task.model";

export interface UpdateTaskModel {
  target: number;
  new: TaskModel
}
