import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { PM, UserModel } from 'src/app/model/entity/user.model';
import { FormField } from 'src/app/model/form-field.model';
import { ProjectInformation } from 'src/app/model/project-information.model';
import { AppService } from 'src/app/service/api/app/app.service';
import { AuthService } from 'src/app/service/api/auth/auth.service';
import { UserService } from 'src/app/service/api/entity/user/user.service';
import { ProjectService } from 'src/app/service/api/project/project.service';
import { BackEndUtilsService } from 'src/app/service/api/utils/utils.service';
import { UtilsService, matchValidator } from 'src/app/service/utils/utils.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {

  constructor(private projectService: ProjectService, public appService: AppService, private userService: UserService, public authService: AuthService,
              private utilsService: UtilsService) {
    this.authService.refreshMe();
  }

  differentUser: boolean = false;

  projectsPaths: string[] = [];

  projectInformation?: ProjectInformation | null;

  showInitResult?: boolean;
  showOpenError: boolean = false;

  initProjectForm: FormGroup = new FormGroup({
    path: new FormControl('/home/ncla/Desktop/project/project-pi/code/fakeproject3', [Validators.required]),
    openOnInit: new FormControl(false, [Validators.required]),
    forceInit: new FormControl(false, [Validators.required]),
    username: new FormControl('', [Validators.required]),
    email: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', [Validators.required, this.utilsService.createPasswordStrengthValidator(8)]),
    repassword: new FormControl('', [Validators.required, matchValidator('password')]),
  })

  openProjectForm: FormGroup = new FormGroup({
    path: new FormControl('', [Validators.required])
  });

  ngOnInit() {
    this.loadProjectsPaths();
    this.loadProjectInformation();
  }

  loadProjectsPaths(): void {
    this.appService.projectsPathsStored().then((response) => {

      response.subscribe({
        next: (paths) => {
          if(!!paths) {
            this.projectsPaths = paths;
          }
        }
      })

    })
  }

  loadProjectInformation(): void {
    this.projectService.getProjectInformation().then((response) => {

      response.subscribe({
        next: (value) => {
            this.projectInformation = value;
        }
      })

    })
  }

  updatePath(value: string) {
    this.openProjectForm.controls['path'].setValue(value);
    this.openProjectForm.controls['path'].updateValueAndValidity();   // force refresh form check
  }

  open() {

    this.showOpenError = false;

    if(this.openProjectForm.valid) {

      this.appService.openProject(this.openProjectForm.controls['path'].value).then((response) => {
        response.subscribe({
          next: (result) => {

            if(!!result) {

              window.location.reload();   // reload app

            } else {
              this.showOpenError = true;
            }

          },
          error: (e) => this.showOpenError = true
        })
      })

    }
  }

  fillInitForm() {
    this.initProjectForm.controls["username"].setValue(this.authService.loggedUser?.username);

    this.initProjectForm.controls["email"].setValue(this.authService.loggedUser?.email);
  }

  init() {
    if(this.initProjectForm.valid) {

      this.showInitResult = undefined;

      const openOnInit = this.initProjectForm.controls["openOnInit"].value;
      const path = this.initProjectForm.controls["path"].value;
      const forceInit = !!this.initProjectForm.controls["forceInit"].value;

      const pm: PM = {
        email: this.initProjectForm.controls["email"].value,
        username: this.initProjectForm.controls["username"].value,
        password: this.initProjectForm.controls["password"].value,
      }

      this.appService.initProject(path, pm, openOnInit, forceInit).then((response) => {

        response.subscribe({
          next: (value) => {
            this.showInitResult = !!value;

            if(!!value) {
              setTimeout(() => {
                window.location.reload();
              }, 500);
            }

          },
          error: (e) => this.showInitResult = true
        })

      })

    }
  }
}
