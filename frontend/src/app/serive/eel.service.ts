import { Injectable } from '@angular/core';

declare var eel: any;

@Injectable({
  providedIn: 'root'
})
export class EelService {

  constructor() {
   }

  public async call(name: string, ...args: any): Promise<any> {

    let result = await eel[name](args)();

    return result;

  }
}
