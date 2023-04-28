import { Directive, ElementRef, HostListener, Input } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Directive({
  selector: '[appAutoHeight]'
})
export class AutoHeightDirective {

  @Input("offset") offset: number = 20;
  @Input("base") base: number = 10;

  constructor(private el: ElementRef) {
  }

  ngAfterViewInit() {
    this.refreshHeight();
  }


  @HostListener('input')
  onChange($event: any) {

    this.refreshHeight();

  }

  refreshHeight() {
    const host = this.el.nativeElement;

    let h: number = this.base;

    if(host.scrollHeight) {
      h = host.scrollHeight;
    }

    host.style.height = (h + this.offset) + "px";
  }

}
