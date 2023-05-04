import { Component, Input } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { FormField } from 'src/app/model/form-field.model';

@Component({
  selector: 'app-manage-entity',
  templateUrl: './manage-entity.component.html',
  styleUrls: ['./manage-entity.component.scss']
})
export class ManageEntityComponent<T> {
  @Input("entity") entity?: T;
  @Input("title") title?: string;
  @Input("editableFields") editableFields: FormField[] = [];

  form?: FormGroup;

  ngOnInit() {

    // create reactive form dynamically
    this.form = new FormGroup({});

    for (let index = 0; index < this.editableFields.length; index++) {
      const element = this.editableFields[index];

      let value = (this.entity as any)[element.name];

      if(element.type == "color")
        value = "#" + value;

      this.form.addControl(element.name, element.formControl);
      element.formControl.setValue(value);

    }

  }
}
