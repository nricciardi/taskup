import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { FormField } from 'src/app/model/form-field.model';
import { AppService } from 'src/app/service/api/app/app.service';
import { environment } from 'src/environments/environment.development';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.scss']
})
export class SettingsComponent {

  readonly SETTINGS_FIELD: FormField[] = [
  {
    name: "app_mode",
    title: "app_mode",
    type: "text",
    blueprintFormControl: new FormControl('', [Validators.required]),
  },
  {
    name: "backup",
    title: "backup",
    type: "checkbox",
    blueprintFormControl: new FormControl('', [Validators.required]),
  },
  {
    name: "current_project_path",
    title: "current_project_path",
    type: "text",
    blueprintFormControl: new FormControl('', [Validators.required]),
  },
  {
    name: "use_localtime",
    title: "use_localtime",
    type: "checkbox",
    blueprintFormControl: new FormControl('', [Validators.required]),
  },
  {
    name: "vault_path",
    title: "vault_path",
    type: "text",
    blueprintFormControl: new FormControl('', [Validators.required]),
  },
  {
    name: "verbose",
    title: "verbose",
    type: "checkbox",
    blueprintFormControl: new FormControl('', [Validators.required]),
  },
  ]

  settingsForm?: FormGroup;
  submitResult?: boolean;

  constructor(public appService: AppService) {

  }

  ngOnInit() {
    this.loadSettings();
  }

  loadSettings() {

    this.appService.getSettings().then((response) => {

      response.subscribe({
        next: (settings) => {

          this.createForm(settings);

        }
      })

    })

  }

  createForm(settings: Record<string, any>) {

    this.settingsForm = new FormGroup({});

    this.SETTINGS_FIELD.forEach((settingsField) => {

      const control = new FormControl(settings[settingsField.name], settingsField.blueprintFormControl.validator, settingsField.blueprintFormControl.asyncValidator);
      this.settingsForm!.addControl(settingsField.name, control);
    })

  }

  submit() {
    if(this.settingsForm && this.settingsForm.valid) {

      this.submitResult = undefined;

      this.appService.updateSettings(this.settingsForm.value).then((response) => {
        response.subscribe({
          next: (result: boolean) => {

            this.submitResult = !!result;


            setTimeout(() => {
              this.submitResult = undefined;
            }, environment.alertTimeout);

          }
        })
      });

    }
  }

}
