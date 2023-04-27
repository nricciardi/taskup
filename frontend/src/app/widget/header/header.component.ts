import { Component, ElementRef, Input, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { UserModel } from 'src/app/model/entity/user.model';
import { AuthService } from 'src/app/service/api/auth/auth.service';
import { LoggerService } from 'src/app/service/logger/logger.service';
import { UtilsService } from 'src/app/service/utils/utils.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent {

  @ViewChild("throwErrorLogoutModal") throwErrorLogoutModal?: ElementRef;

  userLogged: UserModel | null = null;

  constructor(private authService: AuthService, private router: Router, public utilsService: UtilsService) {
  }

  ngOnInit() {
    this.authService.observeMe().subscribe({
      next: (value: UserModel | null) => {
        console.log(value);

        this.userLogged = value;
      },
      error: (e: any) => {
        LoggerService.logError(e);
      }
    });

    this.authService.refreshMe()
  }

  logout() {

    this.authService.logout().then((response) => {

      this.router.navigate(["/login"]);

    }).catch((e) => {
      this.throwErrorLogoutModal?.nativeElement.click();
    })

  }

}


/*
// observe isLogged

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


*/
