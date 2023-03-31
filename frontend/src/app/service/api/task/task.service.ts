import { Injectable } from '@angular/core';
import { EelService } from '../../eel/eel.service';

@Injectable({
  providedIn: 'root'
})
export class TaskService {

  constructor(private eelService: EelService) { }

  public all() {
    
  }

}
