import { BaseEntity } from "./base-entity.model";

export interface TaskStatusModel extends BaseEntity {
  id: number;
  name: string;
  description: string | null;
  hex_color: string | null;

  default_next_task_status_id: number;
  default_next_task_status: TaskStatusModel | null;

  default_prev_task_status_id: number;
  default_prev_task_status: TaskStatusModel | null;
}
