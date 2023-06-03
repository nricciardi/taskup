import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Router } from '@angular/router';
import { RepoNode } from 'src/app/model/entity/repo.model';
import { TaskModel } from 'src/app/model/entity/task.model';
import { TaskService } from 'src/app/service/api/entity/task/task.service';
import { environment } from 'src/environments/environment.development';

@Component({
  selector: 'app-show-info-of-commit-modal',
  templateUrl: './show-info-of-commit-modal.component.html',
  styleUrls: ['./show-info-of-commit-modal.component.scss']
})
export class ShowInfoOfCommitModalComponent {

  dateFormat: string = environment.fullDateFormat;

  @Input("target") target?: string;
  @Input("node") node?: RepoNode;

  tasksAssociated: TaskModel[] = [];

  constructor(private taskService: TaskService, private router: Router) {}

  loadTasksAssociated() {

    if(!this.node?.of_branch)
      return;

    this.tasksAssociated = [];

    this.taskService.filter({
      "git_branch": this.node.of_branch
    }, "like").then((response) => {
      response.subscribe({
        next: (tasks) => {

          if(!tasks)
            return;

          this.tasksAssociated = this.tasksAssociated.concat(tasks);

          // filter based on priority
          this.tasksAssociated.sort((a, b) => {
            return a.priority - b.priority;
          })

        }
      })
    })
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
