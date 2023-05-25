import { Component, EventEmitter, Input, Output } from '@angular/core';
import { TaskModel } from 'src/app/model/entity/task.model';
import { TaskService } from 'src/app/service/api/entity/task/task.service';

@Component({
  selector: 'app-show-info-of-commit-modal',
  templateUrl: './show-info-of-commit-modal.component.html',
  styleUrls: ['./show-info-of-commit-modal.component.scss']
})
export class ShowInfoOfCommitModalComponent {
  @Input("target") target?: string;
  @Input("commiterEmail") commiterEmail?: string;
  @Input("branchesOfCommit") branchesOfCommit?: string[];
  @Input("message") message?: string;
  @Input("hash") hash?: string;
  @Input("commiterName") commiterName?: string;

  tasksAssociated: TaskModel[] = [];

  constructor(private taskService: TaskService) {}

  loadTasksAssociated() {

    if(!this.branchesOfCommit)
      return;

    this.tasksAssociated = [];

    for (let index = 0; index < this.branchesOfCommit.length; index++) {
      const branch = this.branchesOfCommit[index];

      this.taskService.filter({
        "git_branch": branch
      }, "like").then((response) => {
        response.subscribe({
          next: (tasks) => {
            console.log(tasks);

            this.tasksAssociated.concat(tasks);
          }
        })
      })
    }

  }

  ngOnChanges() {
    this.loadTasksAssociated();
  }
}
