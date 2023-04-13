import { Injectable } from '@angular/core';
import { EelService } from '../../eel/eel.service';
import { DashboardModel } from 'src/app/model/entity/dashboard.model';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {

  private readonly GET_DATA = "dashboard_get_data";

  constructor(private eelService: EelService) { }

  public getData(): Promise<Observable<DashboardModel>> {
    return this.eelService.call(this.GET_DATA);
  }
}
