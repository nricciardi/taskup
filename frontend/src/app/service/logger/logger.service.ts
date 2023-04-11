import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment.development';

@Injectable({
  providedIn: 'root'
})
export class LoggerService {

  constructor() { }

  public static logError(...msg: Array<string>): void {

    if(!environment.verbose)
      return;


    console.error("E:", ...msg);

  }

  public static logInfo(...msg: Array<string>): void {

    if(!environment.verbose)
      return;


    console.info("I:", ...msg);

  }

  public static logWarning(...msg: Array<string>): void {

    if(!environment.verbose)
      return;


    console.warn("W:", ...msg);

  }

  public static logSuccess(...msg: Array<string>): void {

    if(!environment.verbose)
      return;


    console.log("S:", ...msg);

  }
}
