import { Injectable } from '@angular/core';
import { EntityApiService } from '../entity-api.service';
import { TaskStatusModel } from 'src/app/model/entity/task-status.model';

@Injectable({
  providedIn: 'root'
})
export class TaskStatusService extends EntityApiService<TaskStatusModel> {

  readonly ALL = "task_status_all";
  override FIND: string = "task_status_find";
  override DELETE_BY_ID: string = "task_status_delete_by_id";
  override UPDATE: string = "task_status_update";
  override CREATE: string = "task_status_create_from_dict";
}
