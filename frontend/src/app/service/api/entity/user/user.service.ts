import { Injectable } from '@angular/core';
import { EntityApiService } from '../entity-api.service';
import { UserModel } from 'src/app/model/entity/user.model';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService extends EntityApiService<UserModel> {
  override ALL: string = "user_all";
  override FIND: string = "user_find";
  override DELETE_BY_ID: string = "user_delete_by_id";
  override UPDATE: string = "user_update";
  override CREATE: string = "user_create";
  override CHECK_ALREADY_USED: string = "user_check_already_used";
  readonly FIND_BY_EMAIL: string = "user_find_by_email";

  public async findByEmail(email: string): Promise<Observable<UserModel | null>> {

    return this.eelService.call(this.FIND_BY_EMAIL, email);
  }
}
