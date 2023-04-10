import { Injectable } from '@angular/core';
import { EelService } from '../../eel/eel.service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export abstract class EntityApiService<T> {

  readonly abstract ALL: string;
  readonly abstract FIND: string;


  constructor(private eelService: EelService) { }

  public async all(): Promise<Observable<T[]>> {

    return this.eelService.call(this.ALL);
  }

  public async find(id: number): Promise<Observable<T>> {

    return this.eelService.call(this.FIND, id);
  }
}
