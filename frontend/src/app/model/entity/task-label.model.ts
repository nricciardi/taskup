import { BaseEntity } from "./base-entity.model";

export interface TaskLabelModel extends BaseEntity {
  id: number;
  name: string;
  description: string | null;
  hex_color: string;
}
