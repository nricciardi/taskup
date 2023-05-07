import { Component, ElementRef, EventEmitter, Input, Output, ViewChild } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { FormField } from 'src/app/model/form-field.model';

@Component({
  selector: 'app-input-modal',
  templateUrl: './input-modal.component.html',
  styleUrls: ['./input-modal.component.scss']
})
export class InputModalComponent {
  @ViewChild("closeBtn") closeBtn?: ElementRef;

  @Input("target") target?: string;
  @Input("title") title?: string;
  @Input("description") description?: string;
  @Input("fields") fields: FormField[] = [];


  @Output() onClose = new EventEmitter<void>();
  @Output() onConfirm = new EventEmitter<void>();


  form?: FormGroup;

  ngOnInit() {
    // create dynamically form
    if(this.fields) {

      this.form = new FormGroup({});

      for (let index = 0; index < this.fields.length; index++) {
        const field = this.fields[index];

        this.form.addControl(field.name, new FormControl(''));

      }

    }


  }
}
