import { Component } from '@angular/core';
import { DashboardModel } from 'src/app/model/entity/dashboard.model';
import { TaskStatusModel } from 'src/app/model/entity/task-status.model';
import { TaskModel } from 'src/app/model/entity/task.model';
import { DashboardService } from 'src/app/service/api/dashboard/dashboard.service';
import { GitgraphService } from 'src/app/service/git/gitgraph/gitgraph.service';


enum OrderBy {
  PRIORITY = "priority",
  DEADLINE = "deadline"
}


@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent {

  OrderBy = OrderBy

  loadingError:boolean = false;

  dashboard: DashboardModel | null = null;
  private _taskStatusIndex?: number;   // the index for task_status id

  get taskStatusIndex() {
    return this._taskStatusIndex;
  }

  set taskStatusIndex(newIndex) {
    this._taskStatusIndex = newIndex;
  }


  private _orderBy: OrderBy = this.OrderBy.PRIORITY;

  get orderBy() {
    return this._orderBy;
  }

  set orderBy(value: OrderBy) {
    this._orderBy = value;
  }

  private _orderReverse: boolean = true;

  get orderReverse() {
    return this._orderReverse;
  }

  set orderReverse(value: boolean) {
    this._orderReverse = value;
  }

  constructor(private dashboardService: DashboardService, gitgraph: GitgraphService) {
  }

  ngOnInit() {

    this.loadDashboard();

  }

  loadDashboard(): void {
    this.dashboard = null;

    this.dashboardService.getData().then((response) => {
      response.subscribe({
        next: (value: DashboardModel | null) => {
          if(value) {
            this.dashboard = value;

            // set default id index
            this.taskStatusIndex = this.dashboard.default_task_status_id;

            this.loadingError = false;
          } else {
            this.loadingError = true;
          }

        }
      })
    });
  }

  getTaskStatusById(taskStatusId: number): TaskStatusModel | null {

    const result = this.dashboard?.task_status?.filter(taskStatus => taskStatus.id == taskStatusId);

    if(result)
      return result[0];

    return null;
  }

  getCurrentTaskStatus(): TaskStatusModel | null {

    if(this.taskStatusIndex)
      return this.getTaskStatusById(this.taskStatusIndex);

    return null;
  }

  getNextTaskStatus(): TaskStatusModel | null {

    let currentTaskStatus: TaskStatusModel | null = this.getCurrentTaskStatus();

    if(currentTaskStatus)
      return currentTaskStatus.default_next_task_status;
    else
      return null

  }

  getPrevTaskStatus(): TaskStatusModel | null {

    let currentTaskStatus: TaskStatusModel | null = this.getCurrentTaskStatus();

    if(currentTaskStatus)
      return currentTaskStatus.default_prev_task_status;
    else
      return null
  }

  getAllTaskBasedOnStatusId(taskStatusId: number | undefined): TaskModel[] | null {

    if(!this.dashboard || !taskStatusId)
      return null;

    let tasksBasedOnStatusId = this.dashboard!.tasks.filter(task => task !== undefined && task.task_status_id === taskStatusId);

    if(!tasksBasedOnStatusId)
      return null;

    tasksBasedOnStatusId?.sort((a: TaskModel, b: TaskModel): number => {

      const aField: any = a[this.orderBy];
      const bField: any = b[this.orderBy];

      let res: number = 0;

      if(aField > bField) {
        res = 1;
      }

      if(aField < bField) {
        res = -1;
      }

      // null and undefiend field as last
      if(aField === undefined || aField === null)
        res = 1;

      if(bField === undefined || bField === null)
        res = -1;

      if(this.orderReverse)
        return res * -1;


      return res;
    })

    return tasksBasedOnStatusId;
  }
}
