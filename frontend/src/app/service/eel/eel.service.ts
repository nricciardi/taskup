import { Injectable } from '@angular/core';
import { Observable, interval } from 'rxjs';
import { filter, take } from 'rxjs/operators';
import { LoggerService } from '../logger/logger.service';

declare var eel: any;

@Injectable({
  providedIn: 'root'
})
export class EelService {

  constructor() {
   }

  public async call(name: string, ...args: any): Promise<any> {

    let observer = new Observable((observer) => {   // create observer to subscribe it in component

      // Periodic check of connection status
      interval(10).pipe(
        filter(() => {
          return eel && eel._websocket.readyState === WebSocket.OPEN      // call when eel's websocket is open
        }),
        take(1),    // stop interval on WebSocket OPEN (otherwise loop of request)
      ).subscribe({
        next: async () => {
          LoggerService.logSuccess('WebSocket Connection OPEN!');

          let result = await eel[name](...args)();   // call the eel exposed method and await response (double parentesis)


          LoggerService.logInfo("Eel result:", result);

          observer.next(result);    // send result on response observer

        },

        error: (e) => {
          LoggerService.logError(e);

          observer.error(e);
        }
      });
    });

    return observer;
  }
}
