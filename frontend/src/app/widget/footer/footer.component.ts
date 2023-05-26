import { Component } from '@angular/core';
import { AppService } from 'src/app/service/api/app/app.service';
import { LoggerService } from 'src/app/service/logger/logger.service';
import { UtilsService } from 'src/app/service/utils/utils.service';
import { environment } from 'src/environments/environment.development';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.scss']
})
export class FooterComponent {

  appName = environment.appName;
  version?: string;

  constructor(public appService: AppService, public utilsService: UtilsService) {}

  ngOnInit() {
    this.loadVersion();
  }

  close() {

    this.appService.close().then(() => {

      window.close();
    })
  }

  loadVersion() {
    this.appService.version().then((response) => {
      response.subscribe({
        next: (value) => {
          this.version = value;
        }
      })
    })
  }
}
