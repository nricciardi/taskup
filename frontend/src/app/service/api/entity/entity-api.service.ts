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
  readonly abstract UPDATE: string;
  readonly abstract CREATE: string;
  readonly abstract CHECK_ALREADY_USED: string;
  readonly abstract FILTER: string;

  constructor(public eelService: EelService) { }

  public async all(): Promise<Observable<T[]>> {

    return this.eelService.call(this.ALL);
  }

  public async find(id: number): Promise<Observable<T>> {

    return this.eelService.call(this.FIND, id);
  }

  public async deleteById(id: number): Promise<Observable<boolean>> {

    return this.eelService.call(this.DELETE_BY_ID, id);
  }

  public async update(id: number | null, data: object): Promise<Observable<T>> {
    // if id is null => try to create

    return this.eelService.call(this.UPDATE, id, data);
  }

  public async create(data: any): Promise<Observable<T>> {

    return this.eelService.call(this.CREATE, data);
  }

  public async filter(data: any, operator: string = "="): Promise<Observable<T[]>> {

    return this.eelService.call(this.FILTER, data, operator);
  }

  public async checkAlreadyUsed(field: string, value: any): Promise<Observable<boolean>> {

    return this.eelService.call(this.CHECK_ALREADY_USED, field, value);
  }
}
