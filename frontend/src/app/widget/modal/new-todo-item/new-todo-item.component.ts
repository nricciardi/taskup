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

  @Output() onClose = new EventEmitter<void>();
  @Output() onSubmit = new EventEmitter<NewTodoItemModel>();

  newItemForm = new FormGroup({
    description: new FormControl(null, [Validators.required]),
    deadline: new FormControl(null),
  });


  _onSubmit() {

    if(this.newItemForm.valid) {
      console.log(this.newItemForm.controls);

      this.onSubmit.emit({
        description: this.newItemForm.controls["description"].value!,
        deadline: this.newItemForm.controls["deadline"].value
      })

    }

  }
}
