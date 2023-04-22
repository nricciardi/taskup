import { Injectable } from '@angular/core';
import { EelService } from '../../eel/eel.service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export abstract class EntityApiService<T> {

  readonly abstract ALL: string;
  readonly abstract FIND: string;
  readonly abstract DELETE_BY_ID: string;

  constructor(public eelService: EelService) { }

  public async all(): Promise<Observable<T[]>> {

    return this.eelService.call(this.ALL);
  }

  public async find(id: number): Promise<Observable<T>> {

    return this.eelService.call(this.FIND, id);
  }

  public async deleteById(id: number): Promise<Observable<T>> {

    return this.eelService.call(this.DELETE_BY_ID, id);
  }
}
