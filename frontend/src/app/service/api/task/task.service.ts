import { Injectable } from '@angular/core';
import { TaskModel } from 'src/app/model/task.model';
import { EelService } from '../../eel/eel.service';

@Injectable({
  providedIn: 'root'
})
export class TaskService {

  readonly EXPOSED_TASK_ALL: string = "task_all_as_dict";

  constructor(private eelService: EelService<number>) { }

  public async all() {

    return await this.eelService.call(this.EXPOSED_TASK_ALL);
  }

}
