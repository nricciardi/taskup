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

  constructor(private taskLabelService: TaskLabelService) {}

  entities: TaskLabelModel[] = [];

  fields: FormField[] = [
    {
      name: "name",
      type: "text",
      placeholder: "Name",
      formControl: new FormControl('', [Validators.required])
    },
    {
      name: "description",
      type: "textarea",
      placeholder: "Description",
      formControl: new FormControl('')
    },
    {
      name: "hex_color",
      type: "color",
      placeholder: "Color",
      formControl: new FormControl('', [Validators.required])
    },
  ]

  ngOnInit() {
    this.loadEntities();
  }

  loadEntities() {

    this.taskLabelService.all().then((response) => {

      response.subscribe({
        next: (values: TaskLabelModel[]) => {

          if(!!values) {

            // modify already existing array since that it is passed as input in copy to child
            this.entities.splice(0, this.entities.length);
            values.forEach((v) => this.entities.push(v));
          }

        }
      })

    })

  }
}
