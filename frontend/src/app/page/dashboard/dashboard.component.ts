import { Component, ElementRef, ViewChild } from '@angular/core';
import { DashboardModel } from 'src/app/model/entity/dashboard.model';
import { TaskStatusModel } from 'src/app/model/entity/task-status.model';
import { TaskModel } from 'src/app/model/entity/task.model';
import { DashboardService } from 'src/app/service/api/dashboard/dashboard.service';
import { GitgraphService } from 'src/app/service/git/gitgraph/gitgraph.service';
import { LoggerService } from 'src/app/service/logger/logger.service';


enum OrderBy {
  PRIORITY = "priority",
  DEADLINE = "deadline"
}

interface HSLColor {
  h: number;
  s: number;
  l: number;
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

  constructor(private dashboardService: DashboardService) {
  }

  @ViewChild("statusGraph") statusGraphContainer?: ElementRef;

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

            // set default id index
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

    return `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, 0.5)`;

  }

  hexToRgb(hex: string): RGBColor | null {
    let result = /^#?([a-f\d]{2}])([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);

    if(!result)
      return null;

    let rgb: RGBColor = {
      r: parseInt(result[1], 16),
      g: parseInt(result[2], 16),
      b: parseInt(result[3], 16),
    }

    return rgb;
  }

  hexToHsl(hex: string): HSLColor | null {
    let result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);

    if(!result)
      return null;

    let r = parseInt(result[1], 16);
    let g = parseInt(result[2], 16);
    let b = parseInt(result[3], 16);
    r /= 255, g /= 255, b /= 255;
    let max = Math.max(r, g, b), min = Math.min(r, g, b);
    let h, s, l = (max + min) / 2;

    if(max == min){
      h = s = 0; // achromatic
    }else{
      var d = max - min;
      s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
      switch(max){
        case r: h = (g - b) / d + (g < b ? 6 : 0); break;
        case g: h = (b - r) / d + 2; break;
        case b: h = (r - g) / d + 4; break;
      }

      if(!h)
        return null;

      h /= 6;
    }

    let HSL: HSLColor = {
      h: h,
      s: s,
      l: l
    };

    return HSL;
  }
}
