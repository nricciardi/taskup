import { Component } from '@angular/core';
import { AbstractControl, AsyncValidatorFn, FormControl, FormGroup, ValidationErrors, ValidatorFn, Validators } from '@angular/forms';
import { Observable, map, of } from 'rxjs';
import { UserModel } from 'src/app/model/entity/user.model';
import { AuthService } from 'src/app/service/api/auth/auth.service';
import { UserService } from 'src/app/service/api/entity/user/user.service';
import { LoggerService } from 'src/app/service/logger/logger.service';
import { UtilsService, matchValidator } from 'src/app/service/utils/utils.service';

@Component({
  selector: 'app-my-profile',
  templateUrl: './my-profile.component.html',
  styleUrls: ['./my-profile.component.scss']
})
export class MyProfileComponent {

  loggedUser?: UserModel;

  colorPicked?: string;

  blueprintMasterDataUserForm = new FormGroup({
    username: new FormControl<string>('', [Validators.required], this.checkUnique("username")),
    name: new FormControl<string | null>(null),
    surname: new FormControl<string | null>(null),
    email: new FormControl<string>('', [Validators.required], this.checkUnique("email")),
    phone: new FormControl<string | null>(null),
  });

  blueprintPasswordUserForm = new FormGroup({
    password: new FormControl<string>('', [Validators.required, this.utilsService.createPasswordStrengthValidator(8)]),
    repassword: new FormControl<string>('', [Validators.required, matchValidator('password')]),
  });

  constructor(private authService: AuthService, public utilsService: UtilsService, private userService: UserService) {
    this.loadLoggedUser();
  }

  ngOnInit() {
  }

  loadLoggedUser() {
    this.authService.me().then((response) => {
      response.subscribe({
        next: (value: UserModel) => {
          this.loggedUser = value;

          this.loadDefaultValues(this.blueprintMasterDataUserForm);

        }
      })
    });
  }

  loadDefaultValues(form: FormGroup) {

    if(!this.loggedUser)
      return;

    const keys = Object.keys(form.controls);

    for (let index = 0; index < keys.length; index++) {
      const fieldName = keys[index];

      (form.controls as any)[fieldName].setValue((this.loggedUser as any)[fieldName]);      // set default values

    }


  }

  modify(values: Object, reload: boolean = true) {

    if(!this.authService.loggedUser)
      return;

    LoggerService.logInfo("Update user: ", this.authService.loggedUser.username);

    const id = this.authService.loggedUser.id;

    this.userService.update(id, values).then((response) => {

      response.subscribe({
        next: (value) => {

          if(reload)
            window.location.reload();
        },
        error: (e) => {

        }
      })

    })
  }

  submitMasterData() {
    if(this.blueprintMasterDataUserForm.valid) {
      this.modify(this.blueprintMasterDataUserForm.value, true);

    }
  }

  submitPasswordData() {
    if(this.blueprintPasswordUserForm.valid) {
      this.modify({
        password: this.blueprintPasswordUserForm.controls["password"].value
      }, true)
    }
  }

  private checkUnique(field: string): AsyncValidatorFn {

    return (control: AbstractControl): Observable<ValidationErrors | null> => {

      return new Observable<boolean>((observer) => {
        this.userService.checkAlreadyUsed(field, control.value).then((response) => {
          response.subscribe({
            next: (exists: boolean) => {

              if(control.value != (this.loggedUser as any)[field]) {
                observer.next(exists);
              } else {
                observer.next(false);   // prevent false-error on first check
              }

              observer.complete();
            }
          });
        })

      }).pipe(map((exists) => {
        return exists ? { 'uniqueError': true } : null;
      }));
    };
  }
}

