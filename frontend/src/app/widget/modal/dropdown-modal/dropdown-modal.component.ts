import { Component, ElementRef, EventEmitter, Input, Output, ViewChild } from '@angular/core';

@Component({
  selector: 'app-dropdown-modal',
  templateUrl: './dropdown-modal.component.html',
  styleUrls: ['./dropdown-modal.component.scss']
})
export class DropdownModalComponent<V> {

  @ViewChild("closeBtn") closeBtn?: ElementRef;

  @Input("target") target?: string;
  @Input("options") options: V[] = [];
  @Input("currentValue") currentValue?: V;
  @Input("title") title?: string;
  @Input("description") description?: string;
  @Input("selectOne") selectOne: boolean = true;
  @Input("confirmBtnText") confirmBtnText: string = "add"
  @Input("showMaskFn") showMaskFn: Function = (element: V) => element;
  @Input("comparatorFn") comparatorFn: Function = (a: V, b: V) => a == b;
  @Input("showCurrentInList") showCurrentInList: boolean = false;
  @Input("disableCurrent") disableCurrent: boolean = true;


  @Output() onClose = new EventEmitter<void>();
  @Output() onSelect = new EventEmitter<V>();

  selectedItem?: V;

  ngOnInit() {
  }

  getItems(): V[] {

    if(!this.options)
      return [];

    let realOptions = this.options;

    if(!this.showCurrentInList && !!this.currentValue) {
      realOptions = this.options.filter((value) => !this.comparatorFn(value, this.currentValue));
    }

    return realOptions;
  }

  select(value: V): void {

    this.onSelect.emit(value);

    if(this.selectOne && this.closeBtn) {
      this.closeBtn.nativeElement.click();
      this.onClose.emit();
    }

  }
}
