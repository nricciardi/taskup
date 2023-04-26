import { Injectable } from '@angular/core';
import { UserModel } from 'src/app/model/entity/user.model';
import { AuthService } from '../api/auth/auth.service';

@Injectable({
  providedIn: 'root'
})
export class UtilsService {

  constructor(private authService: AuthService) {}

  getAvatarText(user: UserModel): string {
    if(user?.name && user?.surname) {
      return user.name.substring(0, 1) + user.surname.substring(0, 1)
    } else {
      return user ? user.username.substring(0, 2) : "-";
    }
  }

  canDelete(authorId: number): boolean {
    let loggedUser = this.authService.loggedUser;

    if(!loggedUser) {
      return false;
    }

    if(!!loggedUser.role?.permission_delete_all)
      return true;

    if(authorId == loggedUser.id && !!loggedUser.role?.permission_delete_own)
      return true;


    return false;

  }

  canModify(authorId: number): boolean {
    let loggedUser = this.authService.loggedUser;

    if(!loggedUser) {
      return false;
    }

    if(!!loggedUser.role?.permission_edit_all)
      return true;

    if(authorId == loggedUser.id && !!loggedUser.role?.permission_edit_own)
      return true;


    return false;

  }
}
