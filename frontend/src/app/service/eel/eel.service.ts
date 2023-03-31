import { Injectable } from '@angular/core';
import { interval } from 'rxjs';
import { filter, take } from 'rxjs/operators';

declare var eel: any;

@Injectable({
  providedIn: 'root'
})
export class EelService<M> {

  constructor() {
   }

  public async call(name: string, ...args: any): Promise<any> {

    // Controllo periodico dello stato della connessione
    interval(10).pipe(
      filter(() => {
        return eel && eel._websocket.readyState === WebSocket.OPEN
      }),
      take(1),
    ).subscribe(async () => {
      console.log('Connessione WebSocket aperta!');

      let result = await eel[name]()();

      console.log("res", result);


      return result;

    });




  }

  /*public async all(): Promise<Array<M>> {

  }*/
}
