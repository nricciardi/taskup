import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-manage-deadline',
  templateUrl: './manage-deadline.component.html',
  styleUrls: ['./manage-deadline.component.scss']
})
export class ManageDeadlineComponent {
  @Input("value") value: Date | null = null;
  @Input("target") target?: string;

  @Output() onSubmit = new EventEmitter<Date | null>();

  manageDeadlineForm = new FormGroup({
    deadline: new FormControl<Date | null>(null),
  });

  ngAfterContentInit() {
    this.manageDeadlineForm.controls["deadline"].setValue(this.value ?? null);

  }

  _onSubmit() {

    if(this.manageDeadlineForm.valid) {

      this.onSubmit.emit(this.manageDeadlineForm.controls["deadline"].value);

      this.value = null;
      this.manageDeadlineForm.reset();
    }


  }

}
