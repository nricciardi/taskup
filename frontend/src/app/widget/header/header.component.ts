import { Component, ElementRef, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { UserModel } from 'src/app/model/entity/user.model';
import { AuthService } from 'src/app/service/api/auth/auth.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent {

  @ViewChild("throwErrorLogoutModal") throwErrorLogoutModal?: ElementRef;

  userLogged?: UserModel;

  constructor(private authService: AuthService, private router: Router) {

    let lastTime: boolean = false;
    this.authService.isLogged(false).then((response) => {
      let subscription = response.subscribe({
        next: (value: boolean) => {

          if(value != lastTime) {     // update userLogged if only if isLogged return a different value => user logged

            lastTime = value;

            this.authService.me().then((response) => {

              response.subscribe({
                next: (value: UserModel) => {
                  this.userLogged = value;

                },
                error: (e) => {
                  // nothig
                }
              })

            }).catch((e) => {
              // nothing
            });
          }

          if(value === false) {
            this.userLogged = undefined;
          }
        },
        error: (e) => {
          // nothig
        }
      })

    });


  }

  logout() {

    this.authService.logout().then((response) => {

      this.router.navigate(["/login"]);

    }).catch((e) => {
      this.throwErrorLogoutModal?.nativeElement.click();
    })

  }

}
