import { Component } from '@angular/core';
import { DashboardModel } from 'src/app/model/entity/dashboard.model';
import { DashboardService } from 'src/app/service/api/dashboard/dashboard.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent {

  public dashboard?: DashboardModel;

  constructor(private dashboardService: DashboardService) {
  }

  ngOnInit() {

    this.dashboardService.getData().then((response) => {
      response.subscribe({
        next: (value: DashboardModel) => {
          this.dashboard = value;

        }
      })
    })

  }
}
