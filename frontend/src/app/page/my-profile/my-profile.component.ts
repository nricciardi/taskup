import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { UserModel } from 'src/app/model/entity/user.model';
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

  loggedUser?: UserModel;

  colorPicked?: string;

  blueprintUserForm = new FormGroup({
    username: new FormControl<string>('', [Validators.required]),
    name: new FormControl<string | null>(null),
    surname: new FormControl<string | null>(null),
    email: new FormControl<string>('', [Validators.required]),
    phone: new FormControl<string | null>(null),
  })

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

          this.loadDefaultMasterDataValues();

        }
      })
    });
  }

  loadDefaultMasterDataValues() {

    if(!this.loggedUser)
      return;

    // set default values
    this.blueprintUserForm.controls["email"].setValue(this.loggedUser["email"]);
    this.blueprintUserForm.controls["username"].setValue(this.loggedUser["username"]);
    this.blueprintUserForm.controls["name"].setValue(this.loggedUser["name"]);
    this.blueprintUserForm.controls["surname"].setValue(this.loggedUser["surname"]);
    this.blueprintUserForm.controls["phone"].setValue(this.loggedUser["phone"]);
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

  submit() {
    if(this.blueprintUserForm.valid) {
      this.modify(this.blueprintUserForm.value);

    }
  }

  checkUnique(field: string, value: string) {
    // this.userService.checkAlreadyUsed()
  }
}
