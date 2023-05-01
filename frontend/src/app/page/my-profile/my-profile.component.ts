import { Component } from '@angular/core';
import { AuthService } from 'src/app/service/api/auth/auth.service';
import { UserService } from 'src/app/service/api/entity/user/user.service';
import { LoggerService } from 'src/app/service/logger/logger.service';
import { UtilsService } from 'src/app/service/utils/utils.service';

@Component({
  selector: 'app-my-profile',
  templateUrl: './my-profile.component.html',
  styleUrls: ['./my-profile.component.scss']
})
export class MyProfileComponent {

  colorPicked?: string;

  constructor(public authService: AuthService, public utilsService: UtilsService, private userService: UserService) {
    this.authService.refreshMe();
  }

  modify(values: Object) {

    if(!this.authService.loggedUser)
      return;

    LoggerService.logInfo("Update user: ", this.authService.loggedUser.username);

    const id = this.authService.loggedUser.id;

    this.userService.update(id, values).then((response) => {

      response.subscribe({
        next: (value) => {
          window.location.reload();
        }
      })

    })
  }
}
