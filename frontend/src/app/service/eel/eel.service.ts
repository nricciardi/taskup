import { Injectable } from '@angular/core';
import { Observable, interval } from 'rxjs';
import { filter, take } from 'rxjs/operators';
import { BaseService } from '../base/base.service';

declare var eel: any;

@Injectable({
  providedIn: 'root'
})
export class EelService {

  constructor() {
   }

  public async call(name: string, ...args: any): Promise<any> {

    //const c = eel[name]();

    let observer = new Observable((observer) => {   // create observer to subscribe it in component

      // Periodic check of connection status
      interval(10).pipe(
        filter(() => {
          return eel && eel._websocket.readyState === WebSocket.OPEN      // call when eel's websocket is open
        }),
        take(1),    // stop interval on WebSocket OPEN (otherwise loop of request)
      ).subscribe({
        next: async () => {
          BaseService.logSuccess('WebSocket Connection OPEN!');

          let result = await eel[name](...args)();   // call the eel exposed method and await response (double parentesis)


          BaseService.logInfo("Eel result:", result);

          observer.next(result);    // send result on response observer

        },

        error: (e) => {
          BaseService.logError(e);

          observer.error(e);
        }
      });
    });

    return observer;
  }
}
