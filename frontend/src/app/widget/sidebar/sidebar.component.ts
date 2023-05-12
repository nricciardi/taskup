import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/service/api/auth/auth.service';
import { environment } from 'src/environments/environment.development';

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent {
  appName = environment.appName;

  constructor(private router: Router, public authService: AuthService) {
    this.authService.refreshMe();
  }

  urlIncludes(str: string): boolean {
    return this.router.url.includes(str);
  }
}
