import { Component } from '@angular/core';
import { UserModel } from 'src/app/model/entity/user.model';
import { AuthService } from 'src/app/service/api/auth/auth.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent {

  userLogged?: UserModel;

  constructor(private authService: AuthService) {

    this.authService.isLogged(true).then((response) => {
      let subscription = response.subscribe({
        next: (value: boolean) => {
          if(value) {
            this.authService.me().then((response) => {

              response.subscribe({
                next: (value: UserModel) => {
                  this.userLogged = value;

                  subscription.unsubscribe();

                },
                error: (e) => {
                  // nothig
                }
              })

            }).catch((e) => {
              // nothing
            });
          } else {
            this.userLogged = undefined;
          }
        },
        error: (e) => {
          // nothig
        }
      })

    });


  }

}
