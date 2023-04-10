import { Injectable } from '@angular/core';
import { TaskModel } from 'src/app/model/entity/task.model';
import { EntityApiService } from '../entity-api.service';

@Injectable({
  providedIn: 'root'
})
export class TaskService extends EntityApiService<TaskModel> {

  override ALL: string = "task_all_as_dict";
  override FIND: string = "task_find";
}
