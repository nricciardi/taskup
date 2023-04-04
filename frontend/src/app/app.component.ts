import { Component } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'frontend';

  /*constructor(public translate: TranslateService) {
    translate.addLangs(['en', 'it']);
    // translate.setDefaultLang('en');
  }

  public switchLanguage(lang: string) {
    this.translate.use(lang);
  }*/
}
