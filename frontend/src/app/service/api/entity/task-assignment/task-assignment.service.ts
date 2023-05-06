import { Injectable } from '@angular/core';
import { EntityApiService } from '../entity-api.service';
import { TaskAssignmentModel } from 'src/app/model/entity/task-assignment.model';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TaskAssignmentService extends EntityApiService<TaskAssignmentModel> {

  override ALL: string = "task_assignmentall";
  override FIND: string = "task_assignmentfind";
  override DELETE_BY_ID: string = "task_assignmentdelete_by_id";
  override UPDATE: string = "task_assignmentupdate";
  readonly REMOVE_ASSIGNMENT = "task_assignmentremove_assignment";
  readonly ADD_ASSIGNMENT = "task_assignmentadd_assignment";
  readonly ADD_LABEL = "task_assignmentadd_label";
  readonly REMOVE_LABEL = "task_assignmentremove_label";
  override CREATE: string = "task_assignmentcreate_from_dict";
  override CHECK_ALREADY_USED: string = "task_assignmentcheck_already_used";
  readonly UPDATE_BY_TASK_USER_ID_FROM_DICT: string = "task_assignment_update_by_task_user_id_from_dict"

  public updateByTaskUserId(taskId: number, userId: number, data: any): Promise<Observable<boolean>> {

    return this.eelService.call(this.UPDATE_BY_TASK_USER_ID_FROM_DICT, taskId, userId, data);
  }
}
