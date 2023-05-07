import { Injectable } from '@angular/core';
import { RoleModel } from 'src/app/model/entity/role.model';
import { EntityApiService } from '../entity-api.service';

@Injectable({
  providedIn: 'root'
})
export class RoleService extends EntityApiService<RoleModel> {
  override ALL: string = "role_all";
  override FIND: string = "role_find";
  override DELETE_BY_ID: string = "role_delete_by_id";
  override UPDATE: string = "role_update";
  override CREATE: string = "role_create";
  override CHECK_ALREADY_USED: string = "role_check_already_used";
}
