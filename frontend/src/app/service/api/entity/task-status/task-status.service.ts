import { Injectable } from '@angular/core';
import { EntityApiService } from '../entity-api.service';
import { TaskStatusModel } from 'src/app/model/entity/task-status.model';
import { first, firstValueFrom, lastValueFrom } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TaskStatusService extends EntityApiService<TaskStatusModel> {

  override ALL = "task_status_all";
  override FIND: string = "task_status_find";
  override DELETE_BY_ID: string = "task_status_delete_by_id";
  override UPDATE: string = "task_status_update";
  override CREATE: string = "task_status_create";
  override CHECK_ALREADY_USED: string = "task_status_check_already_used";
  override FILTER: string = "task_status_filter";

  public async getTaskById(id: number): Promise<TaskStatusModel> {

    let obs = await this.find(id);

    let task: TaskStatusModel = await firstValueFrom(obs);

    return task;
  }

  public async getAll(): Promise<TaskStatusModel[]> {
    return new Promise<TaskStatusModel[]>((resolve, reject) => {

      this.all().then((response) => {

        response.subscribe({
          next: (value) => {
            resolve(value);
          },
          error: (e) => {
            reject(e)
          }
        })

      });

    })
  }
}
