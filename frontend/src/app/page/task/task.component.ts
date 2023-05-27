import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Subscription } from 'rxjs';
import { TaskModel } from 'src/app/model/entity/task.model';
import { TaskService } from 'src/app/service/api/entity/task/task.service';

@Component({
  selector: 'app-task',
  templateUrl: './task.component.html',
  styleUrls: ['./task.component.scss']
})
export class TaskComponent {

  task?: TaskModel;
  paramsSubscription?: Subscription;

  constructor(private taskService: TaskService, private activatedRoute: ActivatedRoute) {}

  ngOnInit() {

    this.paramsSubscription = this.activatedRoute.paramMap.subscribe({
      next: (params) => {

        const id = params.get("id");

        if(!!id)
          this.loadTaskById(+id);
      }
    })
  }

  loadTaskById(id: number) {

    this.task = undefined;

    this.taskService.find(id).then((response) => {

      response.subscribe({
        next: (task) => {
          if(!!task) {
            this.task = task;
          }
        }
      })

    })

  }

  ngOnDestroy() {
    this.paramsSubscription?.unsubscribe();
  }

}
