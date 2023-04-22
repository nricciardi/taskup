import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-dialog-modal',
  templateUrl: './dialog-modal.component.html',
  styleUrls: ['./dialog-modal.component.scss']
})
export class DialogModalComponent {
  @Input("body") body?: string;
  @Input("title") title?: string;
  @Input("target") target: string = "dialog";
}
