import { Injectable } from '@angular/core';
import { TaskModel } from 'src/app/model/entity/task.model';
import { EntityApiService } from '../entity-api.service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TaskService extends EntityApiService<TaskModel> {

  override ALL: string = "task_all";
  override FIND: string = "task_find";
  override DELETE_BY_ID: string = "task_delete_by_id";
  override UPDATE: string = "task_update";
  readonly REMOVE_ASSIGNMENT = "task_remove_assignment";
  readonly ADD_ASSIGNMENT = "task_add_assignment";
  readonly ADD_LABEL = "task_add_label";
  readonly REMOVE_LABEL = "task_remove_label";
  override CREATE: string = "task_create_from_dict";
  override CHECK_ALREADY_USED: string = "task_check_already_used";

  public async removeAssignment(taskId: number, userId: number): Promise<Observable<boolean>> {

    return this.eelService.call(this.REMOVE_ASSIGNMENT, taskId, userId);
  }

  public async addAssignment(taskId: number, userId: number): Promise<Observable<boolean>> {

    return this.eelService.call(this.ADD_ASSIGNMENT, taskId, userId);
  }

  public async addLabel(taskId: number, labelId: number): Promise<Observable<boolean>> {

    return this.eelService.call(this.ADD_LABEL, taskId, labelId);
  }

  public async removeLabel(taskId: number, labelId: number): Promise<Observable<boolean>> {

    return this.eelService.call(this.REMOVE_LABEL, taskId, labelId);
  }
}
