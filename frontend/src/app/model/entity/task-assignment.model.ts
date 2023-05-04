import { BaseEntity } from "./base-entity.model";

export interface TaskAssignmentModel extends BaseEntity {
  id: number;
  assigned_at: Date;

  user_id: number;
  task_id: number;
}
