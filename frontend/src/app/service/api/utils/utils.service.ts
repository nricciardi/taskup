import { Injectable } from '@angular/core';
import { EelService } from '../../eel/eel.service';
import { Observable } from 'rxjs';
import { LoggerService } from '../../logger/logger.service';

@Injectable({
  providedIn: 'root'
})
export class BackEndUtilsService extends EelService {

  // readonly EXIT = "utils_exit";
  readonly OPEN = "utils_open_in_webbrowser";

  public open(path: string): Promise<Observable<null>> {

    return this.call(this.OPEN, path);

  }
}
