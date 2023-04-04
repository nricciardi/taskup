import { Component } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'frontend';

  constructor(public translate: TranslateService) {
    translate.addLangs(['en', 'it']);

    this.setBrowserDefaultLanguage();
  }

  public switchLanguage(lang: string): void {
    this.translate.use(lang);
  }

  public setBrowserDefaultLanguage(): void {
    const browserLang = this.translate.getBrowserLang();

    if(browserLang)
      this.translate.setDefaultLang(browserLang);
  }
}
