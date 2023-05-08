import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ProjectService } from 'src/app/service/api/project/project.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {

  constructor(private projectService: ProjectService) {}

  projectsPaths: string[] = [];

  showError: boolean = false;

  openProjectForm: FormGroup = new FormGroup({
    path: new FormControl('', [Validators.required])
  });

  ngOnInit() {
    this.loadProjectsPaths();
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

  updatePath(value: string) {
    this.openProjectForm.controls['path'].setValue(value);
    this.openProjectForm.controls['path'].updateValueAndValidity();   // force refresh form check
  }

  open() {

    this.showError = false;

    if(this.openProjectForm.valid) {

      this.projectService.setProjectPath(this.openProjectForm.controls['path'].value, true).then((response) => {
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
}
