import { Injectable } from '@angular/core';
import { EelService } from '../../eel/eel.service';
import { Observable } from 'rxjs';
import { LoggerService } from '../../logger/logger.service';
import { PM, UserModel } from 'src/app/model/entity/user.model';
import { UtilsService } from '../../utils/utils.service';
import { environment } from 'src/environments/environment.development';

@Injectable({
  providedIn: 'root'
})
export class AppService extends EelService {

  readonly OPEN_SETTINGS = "app_open_settings";
  readonly OPEN_PROJECT = "app_open_project";
  readonly VERSION = "app_version";
  readonly CLOSE = "app_close";
  readonly INIT_PROJECT = "app_init_project";
  readonly PATHS_STORED = "app_get_projects_paths_stored";
  readonly REMOVE_WORK_DIR = "app_remove_work_dir";
  readonly GET_SETTINGS = "app_get_settings";
  readonly UPDATE_SETTINGS = "app_update_settings";

  public openSettings(): void {

    this.call(this.OPEN_SETTINGS).then((response) => {

      response.subscribe({
        next: () => {
          // nothing
        }
      })

    });

  }

  public removeWorkDir(): void {

    this.call(this.REMOVE_WORK_DIR).then((response) => {

      response.subscribe({
        next: () => {
          window.location.reload();
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

  public close(): Promise<void> {

    return new Promise<void>((resolve, reject) => {
      this.call(this.CLOSE).then((response) => {

        response.subscribe({
          next: () => {
            // nothing
          }
        })

        setTimeout(() => {
          resolve();
        }, environment.timeBeforeClose);

      });
    })



  }

  public initProject(path: string, pm: PM, openOnInit: boolean, forceInit: boolean): Promise<Observable<boolean>> {

    return this.call(this.INIT_PROJECT, path, pm, openOnInit, forceInit);

  }

  public projectsPathsStored(): Promise<Observable<string[]>> {

    return this.call(this.PATHS_STORED);

  }

  public getSettings(): Promise<Observable<Record<string, any>>> {
    return this.call(this.GET_SETTINGS);
  }

  public updateSettings(data: Record<string, any>): Promise<Observable<boolean>> {
    return this.call(this.UPDATE_SETTINGS, data);
  }
}
