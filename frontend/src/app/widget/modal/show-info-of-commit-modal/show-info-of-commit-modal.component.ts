import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Router } from '@angular/router';
import { TaskModel } from 'src/app/model/entity/task.model';
import { TaskService } from 'src/app/service/api/entity/task/task.service';
import { environment } from 'src/environments/environment.development';

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

  constructor(private taskService: TaskService, private router: Router) {}

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

            this.tasksAssociated = this.tasksAssociated.concat(tasks);

          }
        })
      })
    }

  }

  ngOnChanges() {
    this.loadTasksAssociated();
  }

  navigateToTask(id: number | string) {
    setTimeout(() => {
      this.router.navigate(['/task/' + new String(id)]);
    }, 500);
  }
}
