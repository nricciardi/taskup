import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, Router } from '@angular/router';
import { environment } from 'src/environments/environment.development';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class RoleGuardService {

  constructor(private authService: AuthService, private router: Router) { }

  async canActivate(next: ActivatedRouteSnapshot){

    return new Promise((resolve, reject) => {

      if(!('roleRequired' in next.data))
        resolve(true);


      const roleRequired = next.data['roleRequired'];

      this.authService.emitMeChangeSource.asObservable().subscribe({
      next: (user) => {

        if(!user || !user.role) {
          this.router.navigate(["/home"]);
          reject();
          return;
        }

        if(roleRequired in user.role) {

          if(Boolean((user.role as any)[roleRequired])) {
            resolve(true);
          } else {
            this.router.navigate(["/home"]);
            reject();
          }

        }
      }
    });

    this.authService.refreshMe();

    })
  }
}
