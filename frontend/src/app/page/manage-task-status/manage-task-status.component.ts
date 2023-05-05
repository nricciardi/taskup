import { Component } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { FormField, SelectOption } from 'src/app/model/form-field.model';
import { TaskStatusService } from 'src/app/service/api/entity/task-status/task-status.service';

@Component({
  selector: 'app-manage-task-status',
  templateUrl: './manage-task-status.component.html',
  styleUrls: ['./manage-task-status.component.scss']
})
export class ManageTaskStatusComponent {

  constructor(public taskStatusService: TaskStatusService) {}

  fields: FormField[] = [
    {
      name: "name",
      type: "text",
      placeholder: "Name",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
    {
      name: "description",
      type: "textarea",
      placeholder: "Description",
      blueprintFormControl: new FormControl('')
    },
    {
      name: "hex_color",
      type: "color",
      placeholder: "Color",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
  ]

  ngOnInit() {
    this.appendDefaultStatus();   // append role options on list of fields
  }

  appendDefaultStatus() {

    this.taskStatusService.all().then((response) => {

      response.subscribe({
        next: (values) => {

          if(!!values) {

            let options: SelectOption[] = values.map((status) => {

              return {
                value: status.id,
                text: status.name
              }
            });

            options.push({    // append null-option
              value: null,
              text: "null"
            });

            this.fields.push(
              {
                title: "prev-task-status",
                name: "default_prev_task_status_id",
                type: "selectbox",
                placeholder: "prev-task-status",
                blueprintFormControl: new FormControl<number | string | null>(null),
                selectOptions: options
              });

            this.fields.push(
              {
                title: "next-task-status",
                name: "default_next_task_status_id",
                type: "selectbox",
                placeholder: "next-task-status",
                blueprintFormControl: new FormControl<number | string | null>(null),
                selectOptions: options
              });
          }

        }
      })

    })

  }

}
