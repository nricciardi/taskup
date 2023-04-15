import { Component } from '@angular/core';
import { DashboardModel } from 'src/app/model/entity/dashboard.model';
import { TaskStatusModel } from 'src/app/model/entity/task-status.model';
import { TaskModel } from 'src/app/model/entity/task.model';
import { DashboardService } from 'src/app/service/api/dashboard/dashboard.service';


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

  dashboard?: DashboardModel;
  private _taskStatusIdIndex?: number;   // the index for task_status id


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

  constructor(private dashboardService: DashboardService) {
  }

  ngOnInit() {

    this.dashboardService.getData().then((response) => {
      response.subscribe({
        next: (value: DashboardModel) => {
          this.dashboard = value;

          // set default id index
          this.taskStatusIdIndex = this.dashboard.default_task_status_id;
        }
      })
    })

  }

  get taskStatusIdIndex() {
    return this._taskStatusIdIndex;
  }

  set taskStatusIdIndex(newIndex) {
    this._taskStatusIdIndex = newIndex;
  }

  getTaskStatus(taskStatusId: number): TaskStatusModel | undefined {

    const result = this.dashboard?.task_status.filter(taskStatus => taskStatus.id == taskStatusId);

    if(result)
      return result[0];

    return undefined;
  }

  getCurrentTaskStatus(): TaskStatusModel | undefined {

    if(this.taskStatusIdIndex)
      return this.getTaskStatus(this.taskStatusIdIndex);

    return undefined;
  }

  getNextTaskStatus(): TaskStatusModel | undefined {

    let currentTaskStatus: TaskStatusModel | undefined = this.getCurrentTaskStatus();

    if(currentTaskStatus === undefined)
      return undefined;


    return currentTaskStatus.default_next_task_status;

  }

  getPrevTaskStatus(): TaskStatusModel | undefined {

    let currentTaskStatus: TaskStatusModel | undefined = this.getCurrentTaskStatus();

    if(currentTaskStatus === undefined)
      return undefined;

    return currentTaskStatus.default_prev_task_status

  }

  getAllTaskBasedOnStatusId(taskStatusId: number): TaskModel[] | undefined {

    let tasksBasedOnStatusId = this.dashboard?.tasks.filter(task => task.task_status_id === taskStatusId);

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
