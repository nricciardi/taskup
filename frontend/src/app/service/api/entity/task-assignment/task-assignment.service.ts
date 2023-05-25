import { Injectable } from '@angular/core';
import { EntityApiService } from '../entity-api.service';
import { TaskAssignmentModel } from 'src/app/model/entity/task-assignment.model';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TaskAssignmentService extends EntityApiService<TaskAssignmentModel> {

  override ALL: string = "task_assignment_all";
  override FIND: string = "task_assignment_find";
  override DELETE_BY_ID: string = "task_assignment_delete_by_id";
  override FILTER: string = "task_assignment_filter";
  override UPDATE: string = "task_assignment_update";
  readonly REMOVE_ASSIGNMENT = "task_assignment_remove_assignment";
  readonly ADD_ASSIGNMENT = "task_assignment_add_assignment";
  readonly ADD_LABEL = "task_assignment_add_label";
  readonly REMOVE_LABEL = "task_assignment_remove_label";
  override CREATE: string = "task_assignment_create";
  override CHECK_ALREADY_USED: string = "task_assignment_check_already_used";
  readonly UPDATE_BY_TASK_USER_ID_FROM_DICT: string = "task_assignment_update_by_task_user_id_from_dict"

  public updateByTaskUserId(taskId: number, userId: number, data: any): Promise<Observable<boolean>> {

    return this.eelService.call(this.UPDATE_BY_TASK_USER_ID_FROM_DICT, taskId, userId, data);
  }
}
