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
  readonly REMOVE_ASSIGNMENT = "task_remove_assignment";
  readonly ADD_ASSIGNMENT = "task_add_assignment";

  public async removeAssignment(taskId: number, userId: number): Promise<Observable<boolean>> {

    return this.eelService.call(this.REMOVE_ASSIGNMENT, taskId, userId);
  }

  public async addAssignment(taskId: number, userId: number): Promise<Observable<boolean>> {

    return this.eelService.call(this.ADD_ASSIGNMENT, taskId, userId);
  }
}
