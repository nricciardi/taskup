import { BaseEntity } from "./base-entity.model";

export interface RoleModel extends BaseEntity {
  id: number;
  name: string;
  permission_create: boolean;
  permission_read_all: boolean;
  permission_move_backward: boolean;
  permission_move_forward: boolean;
  permission_move: boolean;
  permission_edit_own: boolean;
  permission_edit_all: boolean;
  permission_change_role: boolean;
  permission_change_assignment: boolean;
  permission_delete_own: boolean;
  permission_delete_all: boolean;
}
