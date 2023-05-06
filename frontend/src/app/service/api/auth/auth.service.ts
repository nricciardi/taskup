import { Injectable } from '@angular/core';
import { EelService, CallOptions } from '../../eel/eel.service';
import { Observable, Subject } from 'rxjs';
import { UserModel } from 'src/app/model/entity/user.model';
import { environment } from 'src/environments/environment.development';
import { LoggerService } from '../../logger/logger.service';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private readonly LOGIN: string = "auth_login";
  private readonly LOGOUT: string = "auth_logout";
  private readonly ME: string = "auth_me";
  private readonly IS_LOGGED: string = "auth_is_logged";
  private readonly REFRESH_ME: string = "auth_refresh_me";
  private readonly UPDATE_LAST_VISIT: string = "auth_update_last_visit";

  private _loggedUser: UserModel | null = null;
  get loggedUser() {
    return this._loggedUser
  }

  private emitMeChangeSource = new Subject<UserModel | null>();

  constructor(private eelService: EelService) { }

  public login(email: string, password: string, keep: boolean = false, refresh: boolean = true): Promise<boolean> {

    // return a boolean promise: true if login successful, else false
    let promise = new Promise<boolean>((resolve, reject) => {
      this.eelService.call(this.LOGIN, email, password, keep).then((response) => {
        response.subscribe({
          next: (value: UserModel) => {

            if(refresh)
              this.refreshMe();

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

  public logout(refresh: boolean = true): Promise<boolean> {

    // return a boolean promise: true if login successful, else false
    let promise = new Promise<boolean>((resolve, reject) => {
      this.eelService.call(this.LOGOUT).then((response) => {
        response.subscribe({
          next: (value: boolean) => {

            if(refresh)
              this.refreshMe();

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

  public observeMe(): Observable<UserModel | null> {

    return this.emitMeChangeSource.asObservable();
  }

  public refreshMe(): void {

    this.eelService.call(this.REFRESH_ME).then((response) => {

      response.subscribe({
        next: (value: any) => {
          this.me().then((response) => {

            response.subscribe({
              next: (value: UserModel | null) => {
                this._loggedUser = value;
                this.emitMeChangeSource.next(value);

              },
              error: (e) => {
                LoggerService.logError(e);
              }
            })

          }).catch((e) => {
            LoggerService.logError(e);
          });
        }
      })

    })


  }

  public isLogged(): Promise<Observable<boolean>> {
    return this.eelService.call(this.IS_LOGGED);
  }

  public observeIsLogged(stopOnTrue: boolean = false): Promise<Observable<boolean>> {

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

  public updateLastVisit(): void {
    this.eelService.call(this.UPDATE_LAST_VISIT).then((response) => {

      response.subscribe({
        next: (value: any) => {

          LoggerService.logInfo("Updated last visit of logged user");
        }
      })

    })
  }
}
