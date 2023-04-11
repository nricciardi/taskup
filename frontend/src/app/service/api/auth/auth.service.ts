import { Injectable } from '@angular/core';
import { EelService } from '../../eel/eel.service';
import { Observable } from 'rxjs';
import { UserModel } from 'src/app/model/entity/user.model';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private readonly LOGIN: string = "auth_login";

  constructor(private eelService: EelService) { }

  public login(email: string, password: string, keep: boolean = false): Promise<boolean> {

    // return a boolean promise: true if login successful, else false
    let promise = new Promise<boolean>((resolve, reject) => {
      this.eelService.call(this.LOGIN, email, password, keep).then((response) => {
        response.subscribe({
          next: () => {

            resolve(true);

          },
          error: () => reject()

        })
      }).catch((err) => {
        reject();
      });
    });

    return promise;

  }

}
