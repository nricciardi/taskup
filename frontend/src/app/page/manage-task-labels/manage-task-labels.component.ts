import { Component } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { TaskLabelModel } from 'src/app/model/entity/task-label.model';
import { FormField } from 'src/app/model/form-field.model';
import { TaskLabelService } from 'src/app/service/api/entity/task-label/task-label.service';

@Component({
  selector: 'app-manage-task-labels',
  templateUrl: './manage-task-labels.component.html',
  styleUrls: ['./manage-task-labels.component.scss']
})
export class ManageTaskLabelsComponent {

  constructor(public taskLabelService: TaskLabelService) {}

  fields: FormField[] = [
    {
      name: "name",
      type: "text",
      placeholder: "Name",
      blueprintFormControl: new FormControl('', [Validators.required]),
      unique: true
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
