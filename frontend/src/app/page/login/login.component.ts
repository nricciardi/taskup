import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/service/api/auth/auth.service';
import { LoggerService } from 'src/app/service/logger/logger.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {

  loginForm = new FormGroup({
    email: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', [Validators.required]),
    keep: new FormControl(false)
  });

  loading: boolean = false;
  loginError: boolean = false;

  constructor(private authService: AuthService, private router: Router) {}

  onSubmit() {

    LoggerService.logInfo("try to login...");

    if(this.loginForm.valid) {

      this.loading = true;
      this.loginError = false;

      const { email, password, keep } = this.loginForm.value;
      this.authService.login(email!, password!, keep!).then((response) => {

        if(response) {
          // on success go to /home
          this.router.navigate(["/home"]);

          this.loading = false;
        }
      }).catch((err) => {
        this.loginError = true;
      });
    }

  }
}
