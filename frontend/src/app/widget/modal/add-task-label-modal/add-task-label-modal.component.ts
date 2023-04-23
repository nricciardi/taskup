import { Component, EventEmitter, Input, Output } from '@angular/core';
import { TaskLabelModel } from 'src/app/model/entity/task-label.model';
import { TaskLabelService } from 'src/app/service/api/entity/task-label/task-label.service';
import { TaskService } from 'src/app/service/api/entity/task/task.service';

@Component({
  selector: 'app-add-task-label-modal',
  templateUrl: './add-task-label-modal.component.html',
  styleUrls: ['./add-task-label-modal.component.scss']
})
export class AddTaskLabelModalComponent {

  constructor(private taskService: TaskService, private taskLabelService: TaskLabelService) {}

  @Input("target") target?: string;
  @Input("alreadyAssignedLabels") alreadyAssignedLabels: TaskLabelModel[] = [];

  labelSelected?: TaskLabelModel;

  noLabels: boolean = false;

  labelsCanBeAssign?: TaskLabelModel[];

  @Output() onAdd = new EventEmitter<TaskLabelModel>();   // emit assigned user
  @Output() onClose = new EventEmitter<void>();

  ngOnDestroy() {
    this.onClose.emit();
  }

  select(user: TaskLabelModel) {
    this.labelSelected = user;
  }

  setLabelsCanBeAssign() {

    this.noLabels = false;

    this.taskLabelService.all().then((response) => {

      response.subscribe({
        next: (value: TaskLabelModel[]) => {
          this.labelsCanBeAssign = value.filter((item: TaskLabelModel) => {
            return !this.alreadyAssignedLabels.map(l => l.id).includes(item.id);
          });

          if(!this.labelsCanBeAssign || this.labelsCanBeAssign.length == 0)
            this.noLabels = true;
        }
      });

    });
  }
}
