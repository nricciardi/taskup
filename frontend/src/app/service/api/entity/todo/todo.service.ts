import { Injectable } from '@angular/core';
import { EntityApiService } from '../entity-api.service';
import { TodoItemModel } from 'src/app/model/entity/todo-item.model';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TodoService extends EntityApiService<TodoItemModel> {

  override ALL = "todo_all";
  override FIND = "todo_find";
  override DELETE_BY_ID = "todo_delete_by";
  readonly ALL_OF = "todo_all_of";

  public async allOf(taskId: number): Promise<Observable<TodoItemModel[]>> {

    return this.eelService.call(this.ALL_OF, taskId);
  }
}
