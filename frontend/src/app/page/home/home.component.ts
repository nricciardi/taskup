import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { UserModel } from 'src/app/model/entity/user.model';
import { FormField } from 'src/app/model/form-field.model';
import { ProjectInformation } from 'src/app/model/project-information.model';
import { AppService } from 'src/app/service/api/app/app.service';
import { AuthService } from 'src/app/service/api/auth/auth.service';
import { UserService } from 'src/app/service/api/entity/user/user.service';
import { ProjectService } from 'src/app/service/api/project/project.service';
import { BackEndUtilsService } from 'src/app/service/api/utils/utils.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {

  constructor(private projectService: ProjectService, public appService: AppService, private userService: UserService, private authService: AuthService) {
    this.authService.refreshMe();
  }

  differentUser: boolean = false;

  projectsPaths: string[] = [];

  projectInformation?: ProjectInformation;

  showError: boolean = false;

  initProjectForm: FormGroup = new FormGroup({
    path: new FormControl('/home/ncla/Desktop/project/project-pi/code/fakeproject3', [Validators.required]),
    openOnInit: new FormControl(true, [Validators.required])
  })

  private _initPM?: UserModel;

  get initPM() {
    return this._initPM;
  }

  set initPM(value) {
    this._initPM = value;
  }

  editableFields: FormField[] = [
    {
      name: "username",
      type: "text",
      placeholder: "Username",
      blueprintFormControl: new FormControl('', [Validators.required]),
      unique: true
    },
    {
      name: "name",
      type: "text",
      placeholder: "Name",
      blueprintFormControl: new FormControl<string | null>(null)
    },
    {
      name: "surname",
      type: "text",
      placeholder: "Surname",
      blueprintFormControl: new FormControl<string | null>(null)
    },
    {
      name: "avatar_hex_color",
      type: "color",
      placeholder: "Color",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
    {
      name: "email",
      type: "email",
      placeholder: "Email",
      blueprintFormControl: new FormControl('', [Validators.required, Validators.email]),
      unique: true
    },
    {
      name: "phone",
      type: "text",
      placeholder: "Phone",
      blueprintFormControl: new FormControl('')
    },
  ]

  openProjectForm: FormGroup = new FormGroup({
    path: new FormControl('', [Validators.required])
  });

  ngOnInit() {
    this.loadProjectsPaths();
    this.loadProjectInformation();
  }

  loadProjectsPaths(): void {
    this.projectService.projectsPathsStored().then((response) => {

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

          if(!!value) {
            this.projectInformation = value;
          }
        }
      })

    })
  }

  updatePath(value: string) {
    this.openProjectForm.controls['path'].setValue(value);
    this.openProjectForm.controls['path'].updateValueAndValidity();   // force refresh form check
  }

  open() {

    this.showError = false;

    if(this.openProjectForm.valid) {

      this.appService.openProject(this.openProjectForm.controls['path'].value).then((response) => {
        response.subscribe({
          next: (result) => {

            if(!!result) {

              window.location.reload();   // reload app

            } else {
              this.showError = true;
            }

          },
          error: (e) => this.showError = true
        })
      })

    }
  }

  init() {
    if(this.initProjectForm.valid) {

      if(!this.initPM) {

        if(!!this.authService.loggedUser) {
          this.initPM = this.authService.loggedUser;
        }

      }


      if(!!this.initProjectForm.controls["openOnInit"].value) {
        // do
      }

    }
  }
}
