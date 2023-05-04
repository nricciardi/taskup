import { Component } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { FormField } from 'src/app/model/form-field.model';
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
}
