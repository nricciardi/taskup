import { Injectable } from '@angular/core';
import { EelService } from '../../eel/eel.service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AppService extends EelService {

  readonly OPEN_SETTINGS = "app_open_settings"

  public openSettings(): void {

    this.call(this.OPEN_SETTINGS).then((response) => {

      response.subscribe({
        next: () => {
          // nothing
        }
      })

    });

  }
}
