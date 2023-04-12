import { Injectable } from '@angular/core';
import { Observable, Observer, interval } from 'rxjs';
import { filter, take } from 'rxjs/operators';
import { LoggerService } from '../logger/logger.service';

declare var eel: any;

export interface CallOptions {
  interval: number;
  take: number | null;
  obs?: Observable<boolean>
}

@Injectable({
  providedIn: 'root'
})
export class EelService {

  private max_attempt: number = 3;
  private interval: number = 10;
  private logger_except: string[] = ['auth_is_logged'];

  constructor() {}

  public async callWithOptions(options: CallOptions, name: string, ...args: any): Promise<any> {
    if(options.take === null) {
      let observer = new Observable((observer) => {   // create observer to subscribe it in component

        // Periodic check of connection status
        let i = interval(options.interval).pipe(
          filter(() => {
            return eel && eel._websocket.readyState === WebSocket.OPEN      // call when eel's websocket is open
          }),    // stop interval on WebSocket OPEN (otherwise loop of request)
        ).subscribe(this.get_observable_body(observer, name, ...args));

        options.obs?.subscribe({
          next: (value: boolean) => {
            if(value) {
              i.unsubscribe();
            }
          }
        })
      });

      return observer;

    } else {

      let observer = new Observable((observer) => {   // create observer to subscribe it in component

        // Periodic check of connection status
        interval(options.interval).pipe(
          filter(() => {
            return eel && eel._websocket.readyState === WebSocket.OPEN      // call when eel's websocket is open
          }),    // stop interval on WebSocket OPEN (otherwise loop of request)
          take(options.take!)
        ).subscribe(this.get_observable_body(observer, name, ...args));
      });

      return observer;
    }
  }

  public async call(name: string, ...args: any): Promise<any> {

    let observer = new Observable((observer) => {   // create observer to subscribe it in component

      // Periodic check of connection status
      interval(10).pipe(
        filter(() => {
          return eel && eel._websocket.readyState === WebSocket.OPEN      // call when eel's websocket is open
        }),
        take(1),    // stop interval on WebSocket OPEN (otherwise loop of request)
      ).subscribe(this.get_observable_body(observer, name, ...args));
    });

    return observer;
  }

  private get_observable_body(observer: Observer<unknown>, name: string, ...args: any) {

    return {
      next: async () => {

        if(!this.logger_except.includes(name))
          LoggerService.logSuccess('WebSocket Connection is OPEN!');

        let attempts: number = 0;
        const _call = async () => {

          attempts += 1;

          try {

            if(!this.logger_except.includes(name))
              LoggerService.logInfo("Eel Call:", name);

            let result = await eel[name](...args)();   // call the eel exposed method and await response (double parentesis)

            if(!this.logger_except.includes(name))
              LoggerService.logInfo("Eel Result:", result);

            observer.next(result);    // send result on response observer

          } catch (error) {
            LoggerService.logError(String(error));
            observer.error(error);

            if (attempts <= this.max_attempt)
              setTimeout(_call, 1000);
          }
        }

        return await _call();

      },

      error: (e: any) => {
        LoggerService.logError(e);

        observer.error(e);
      }
    }

  }
}
