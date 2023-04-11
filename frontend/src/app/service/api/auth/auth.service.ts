import { Injectable } from '@angular/core';
import { EelService } from '../../eel/eel.service';
import { Observable } from 'rxjs';
import { UserModel } from 'src/app/model/entity/user.model';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private readonly LOGIN: string = "auth_login";

  constructor(private eelService: EelService) { }

  public login(email: string, password: string, keep: boolean = false): Promise<Observable<UserModel | null>> {

    return this.eelService.call(this.LOGIN, email, password, keep);

  }

}
