import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from './auth.service';
import { environment } from 'src/environments/environment.development';

@Injectable({
  providedIn: 'root'
})
export class AuthGuardService {

  constructor(private authService: AuthService, private router: Router) { }

  async canActivate(){
    return new Promise((resolve, reject) => {

      this.authService.isLogged().then((response) => {

        response.subscribe({
          next: (value: boolean) => {

            if(!value) {
              this.router.navigate([environment.authRequiredRedirectRoute]);
            }

            resolve(value);

          }
        })

      })

    })
  }
}
