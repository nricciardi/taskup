import { BaseEntity } from "./base-entity.model";
import { RoleModel } from "./role.model";

export interface UserModel extends BaseEntity {
  id: number;
  username: string;
  name: string | null;
  surname: string | null;
  email: string;
  avatar_hex_color: string;
  phone: string | null;
  last_visit_at: Date;
  // password: string;    hidden
  role_id: number;
  role: RoleModel | null;
}
