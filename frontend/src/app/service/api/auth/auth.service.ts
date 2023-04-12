import { Injectable } from '@angular/core';
import { EelService, CallOptions } from '../../eel/eel.service';
import { Observable } from 'rxjs';
import { UserModel } from 'src/app/model/entity/user.model';
import { environment } from 'src/environments/environment.development';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private readonly LOGIN: string = "auth_login";
  private readonly LOGOUT: string = "auth_logout";
  private readonly ME: string = "auth_me";
  private readonly IS_LOGGED: string = "auth_is_logged";

  constructor(private eelService: EelService) { }

  public login(email: string, password: string, keep: boolean = false): Promise<boolean> {

    // return a boolean promise: true if login successful, else false
    let promise = new Promise<boolean>((resolve, reject) => {
      this.eelService.call(this.LOGIN, email, password, keep).then((response) => {
        response.subscribe({
          next: (value: UserModel) => {

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

  public logout(): Promise<boolean> {

    // return a boolean promise: true if login successful, else false
    let promise = new Promise<boolean>((resolve, reject) => {
      this.eelService.call(this.LOGOUT).then((response) => {
        response.subscribe({
          next: (value: UserModel) => {

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

  public me(): Promise<Observable<UserModel>> {
    return this.eelService.call(this.ME);
  }

  public isLogged(stopOnTrue: boolean = false): Promise<Observable<boolean>> {

    let stop: boolean = false;

    let callOptions: CallOptions = {
      take: null,
      interval: environment.eelCallRefreshInterval,
      obs: new Observable((observer) => {   // observable to unsubscribe eel.isLogged

        setInterval(() => {
          observer.next(stop);
        }, environment.eelCallRefreshInterval + 1)
      })
    };

    // return an observable which return periodically if the user is logged
    let promise = new Promise<Observable<boolean>>((resolve, reject) => {
      this.eelService.callWithOptions(callOptions, this.IS_LOGGED).then((response: Observable<boolean>) => {

        // to prevent subscribe loop, if stopOnTrue is true, if isLogged return true (user is logged) unsubscribe the eel.isLogged method
        response.subscribe({
          next: (value: boolean) => {

            stop = value && stopOnTrue;
          }
        });

        resolve(response);

      }).catch((err) => {
        reject();
      });
    });

    return promise;
  }
}
