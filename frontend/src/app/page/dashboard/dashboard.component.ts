import { Component, ElementRef, ViewChild } from '@angular/core';
import { DashboardModel } from 'src/app/model/entity/dashboard.model';
import { TaskStatusModel } from 'src/app/model/entity/task-status.model';
import { TaskModel } from 'src/app/model/entity/task.model';
import { UpdateTaskModel } from 'src/app/model/entity/update-task.model';
import { AuthService } from 'src/app/service/api/auth/auth.service';
import { DashboardService } from 'src/app/service/api/dashboard/dashboard.service';
import { GitgraphService } from 'src/app/service/git/gitgraph/gitgraph.service';
import { LoggerService } from 'src/app/service/logger/logger.service';


enum OrderBy {
  PRIORITY = "priority",
  DEADLINE = "deadline"
}

interface RGBColor {
  r: number;
  g: number;
  b: number;
}


@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent {

  constructor(private dashboardService: DashboardService, public authService: AuthService) {
  }

  blueprintTask?: TaskModel;

  OrderBy = OrderBy

  loadingError:boolean = false;

  dashboard: DashboardModel | null = null;
  private _taskStatusIdIndex?: number;   // the index for task_status id

  get taskStatusIdIndex() {
    return this._taskStatusIdIndex;
  }

  set taskStatusIdIndex(newIndex) {
    this._taskStatusIdIndex = newIndex;
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

            // set default id index if it is not setted
            if(!this.taskStatusIdIndex)
              this.taskStatusIdIndex = this.dashboard.default_task_status_id;

            this.loadingError = false;
          } else {
            this.loadingError = true;
          }

        }
      })
    });
  }

  getTaskStatusById(taskStatusId: number): TaskStatusModel | null {


    if(!this.taskStatusIdIndex)
      this.taskStatusIdIndex = this.dashboard?.default_task_status_id;

    const result = this.dashboard?.task_status?.filter(taskStatus => taskStatus.id == taskStatusId);

    if(result)
      return result[0];

    return null;
  }

  getCurrentTaskStatus(): TaskStatusModel | null {

    if(this.taskStatusIdIndex)
      return this.getTaskStatusById(this.taskStatusIdIndex);

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

  getColorFromHex(hex: string | null | undefined): string | null {

    if(!hex)
      return null;

    let rgb = this.hexToRgb(hex);


    if(!rgb)
      return null;

    return `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, 1)`;

  }

  hexToRgb(hex: string): RGBColor | null {

    if(hex.length != 6)
      return null;

    let rgb: RGBColor = {
      r: parseInt(hex.substring(0, 2), 16),
      g: parseInt(hex.substring(2, 4), 16),
      b: parseInt(hex.substring(4), 16),
    }

    return rgb;
  }

  removeTask(taskId: number) {
    if(!this.dashboard?.tasks)
      return;

    this.dashboard.tasks = this.dashboard.tasks.filter(t => t.id != taskId);
  }

  updateTask(managedTask: UpdateTaskModel) {
    if(!this.dashboard?.tasks)
      return;

    for (let index = 0; index < this.dashboard.tasks.length; index++) {
      const element = this.dashboard.tasks[index];

      if(element.id == managedTask.target)
        this.dashboard.tasks[index] = managedTask.new;

    }
  }

  newTask() {
    window.scroll(0, 0);
  }
}
