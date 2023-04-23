import { Injectable } from '@angular/core';
import { EntityApiService } from '../entity-api.service';
import { TaskLabelModel } from 'src/app/model/entity/task-label.model';

@Injectable({
  providedIn: 'root'
})
export class TaskLabelService extends EntityApiService<TaskLabelModel> {

  readonly ALL = "task_label_all";
  override FIND: string = "task_find";
  override DELETE_BY_ID: string = "task_delete_by_id";
  
}
