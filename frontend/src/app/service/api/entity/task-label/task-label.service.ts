import { Injectable } from '@angular/core';
import { EntityApiService } from '../entity-api.service';
import { TaskLabelModel } from 'src/app/model/entity/task-label.model';

@Injectable({
  providedIn: 'root'
})
export class TaskLabelService extends EntityApiService<TaskLabelModel> {

  override ALL = "task_label_all";
  override FIND: string = "task_label_find";
  override DELETE_BY_ID: string = "task_label_delete_by_id";
  override UPDATE: string = "task_label_update";
  override CREATE: string = "task_label_create";
  override CHECK_ALREADY_USED: string = "task_label_check_already_used";
  override FILTER: string = "task_label_filter";

}
