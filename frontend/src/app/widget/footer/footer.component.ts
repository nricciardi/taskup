import { Component } from '@angular/core';
import { AppService } from 'src/app/service/api/app/app.service';
import { UtilsService } from 'src/app/service/utils/utils.service';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.scss']
})
export class FooterComponent {

  constructor(public appService: AppService, public utilsService: UtilsService) {}
}
