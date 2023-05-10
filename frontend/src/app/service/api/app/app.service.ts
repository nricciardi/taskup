import { Injectable } from '@angular/core';
import { EelService } from '../../eel/eel.service';
import { Observable } from 'rxjs';
import { LoggerService } from '../../logger/logger.service';

@Injectable({
  providedIn: 'root'
})
export class AppService extends EelService {

  readonly OPEN_SETTINGS = "app_open_settings";
  readonly OPEN_PROJECT = "app_open_project";
  readonly VERSION = "app_version";
  readonly CLOSE = "app_close";

  public openSettings(): void {

    this.call(this.OPEN_SETTINGS).then((response) => {

      response.subscribe({
        next: () => {
          // nothing
        }
      })

    });

  }

  public version(): Promise<Observable<string>> {
    return this.call(this.VERSION);
  }

  public openProject(path: string): Promise<Observable<boolean>> {

    return this.call(this.OPEN_PROJECT, path);

  }

  public close(): void {

    this.call(this.CLOSE).then((response) => {

      response.subscribe({
        next: () => {
          // nothing
        }
      })

    });

    setTimeout(() => {
      LoggerService.logInfo("Close app");
      window.close();
    }, 500);

  }
}
