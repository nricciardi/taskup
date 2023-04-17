import { Injectable } from '@angular/core';

export declare var GitgraphJS: any;

interface GitgraphJSOption {
  orientation?: string;
  template?: string | Function;
  mode?: string;
}

@Injectable({
  providedIn: 'root'
})
export class GitgraphService {

  constructor() { }

  public createGraph(htmlElement: HTMLElement, options: GitgraphJSOption = {}): any {
    return GitgraphJS.createGitgraph(htmlElement, options);
  }
}
