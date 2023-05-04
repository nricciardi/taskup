import { Component, Input } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { BaseEntity } from 'src/app/model/entity/base-entity.model';
import { FormField } from 'src/app/model/form-field.model';
import { EntityApiService } from 'src/app/service/api/entity/entity-api.service';
import { environment } from 'src/environments/environment.development';

@Component({
  selector: 'app-manage-entity',
  templateUrl: './manage-entity.component.html',
  styleUrls: ['./manage-entity.component.scss']
})
export class ManageEntityComponent<M extends EntityApiService<E>, E extends BaseEntity> {
  @Input("manager") manager?: M;
  @Input("entity") entity?: E;
  @Input("title") title?: string;
  @Input("editableFields") editableFields: FormField[] = [];

  form?: FormGroup;

  submitResult?: boolean;

  ngOnInit() {

    this.createForm();

  }

  createForm() {
    // create reactive form dynamically
    this.form = new FormGroup({});

    for (let index = 0; index < this.editableFields.length; index++) {
      const element = this.editableFields[index];

      let value = (this.entity as any)[element.name];


      // create form controls as copy of blueprint form control
      const blueprint = element.blueprintFormControl;
      let control = new FormControl(blueprint.value, blueprint.validator, blueprint.asyncValidator);

      this.form.addControl(element.name, control);

    }

    this.setFormDefaultValue();
  }

  setFormDefaultValue() {

    if(!this.form)
      return;

    for (let index = 0; index < this.editableFields.length; index++) {
      const element = this.editableFields[index];

      let value = (this.entity as any)[element.name];
      const control = (this.form.controls as any)[element.name];

      control.setValue(value);

    }
  }

  submit() {
    if(this.form?.valid) {

      this.modify(this.form.value);
    }
  }

  modify(values: any) {

    if(!this.entity || !this.manager)
      return;

    const id = this.entity.id;

    const resetResultFlag = () => {
      setTimeout(() => {
        this.submitResult = undefined;
      }, environment.alertTimeout);
    }

    this.manager?.update(id, values).then((response) => {

      response.subscribe({
        next: (value) => {
          if(value) {
            this.entity = value;

            this.submitResult = true;

            resetResultFlag();

          }
        },
        error: (e) => {
          this.submitResult = false;

          resetResultFlag();
        }
      })

    }).catch((reason) => {
      this.submitResult = false;

      resetResultFlag();
    })

  }

  delete() {
    if(!this.entity || !this.manager)
      return;

    const id = this.entity.id;

    const resetResultFlag = () => {
      setTimeout(() => {
        this.submitResult = undefined;
      }, environment.alertTimeout);
    }

    this.manager?.deleteById(id).then((response) => {

      response.subscribe({
        next: (value) => {
          this.entity = undefined;

          this.submitResult = true;

          resetResultFlag();
        },
        error: (e) => {
          this.submitResult = false;

          resetResultFlag();
        }
      })

    }).catch((reason) => {
      this.submitResult = false;

      resetResultFlag();
    })
  }
}
