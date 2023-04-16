import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { TranslateService } from '@ngx-translate/core';
import { AuthService } from './service/api/auth/auth.service';
import { UserModel } from './model/entity/user.model';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'frontend';

  constructor(public translate: TranslateService) {

    // add langs to i18n
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
