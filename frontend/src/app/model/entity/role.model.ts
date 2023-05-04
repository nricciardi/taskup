import { BaseEntity } from "./base-entity.model";

export interface RoleModel extends BaseEntity {
  id: number;
  name: string;
  permission_create: number;
  permission_read_all: number;
  permission_move_backward: number;
  permission_move_forward: number;
  permission_edit_own: number;
  permission_edit_all: number;
  permission_change_role: number;
  permission_change_assignment: number;
  permission_delete_own: number;
  permission_delete_all: number;
}
