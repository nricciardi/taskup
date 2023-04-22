import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-dialog-modal',
  templateUrl: './dialog-modal.component.html',
  styleUrls: ['./dialog-modal.component.scss']
})
export class DialogModalComponent {
  @Input("body") body?: string;
  @Input("title") title?: string;
  @Input("target") target: string = "dialog";
  @Input("centered") centered: boolean = false;
  @Input("confirmBtn") confirmBtn: boolean = false;
  @Input("confirmBtnTxt") confirmBtnTxt: string = "submit";
  @Input("borderless") borderless: boolean = false;

  @Output() onConfirm = new EventEmitter<void>();
}
