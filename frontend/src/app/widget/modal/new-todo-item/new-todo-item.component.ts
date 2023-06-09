import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { NewTodoItemModel } from 'src/app/model/entity/todo-item.model';

@Component({
  selector: 'app-new-todo-item-modal',
  templateUrl: './new-todo-item.component.html',
  styleUrls: ['./new-todo-item.component.scss']
})
export class NewTodoItemComponent {
  @Input("target") target?: string;
  @Input("baseData") baseData?: NewTodoItemModel;

  @Output() onClose = new EventEmitter<void>();
  @Output() onSubmit = new EventEmitter<NewTodoItemModel>();

  newItemForm = new FormGroup({
    description: new FormControl<string | null>(null, [Validators.required]),
    deadline: new FormControl<Date | null>(null),
    priority: new FormControl<number>(0),
  });

  ngAfterContentInit() {
    this.newItemForm.setValue({
      description: this.baseData?.description ?? null,
      deadline: this.baseData?.deadline ?? null,
      priority: this.baseData?.priority ?? 0,
    });


  }


  _onSubmit() {

    if(this.newItemForm.valid) {

      this.onSubmit.emit({
        description: this.newItemForm.controls["description"].value!,
        deadline: this.newItemForm.controls["deadline"].value,
        priority: this.newItemForm.controls["priority"].value ?? 0,
      });

      // erase old data to prevent autofill
      this.baseData = undefined;
      this.newItemForm.reset();

    }

  }
}
