import { Component, EventEmitter, Input, Output } from '@angular/core';
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

  @Output() refreshRequest = new EventEmitter<void>();

  form?: FormGroup;

  submitResult?: boolean;

  collapseStatus: boolean = false;

  ngOnInit() {

    this.createForm();

    this.collapseStatus = !this.entity;
  }

  createForm() {
    // create reactive form dynamically
    this.form = new FormGroup({});

    for (let index = 0; index < this.editableFields.length; index++) {
      const element = this.editableFields[index];

      // create form controls as copy of blueprint form control
      const blueprint = element.blueprintFormControl;
      let control = new FormControl<number | string | null>(blueprint.value, blueprint.validator, blueprint.asyncValidator);

      this.form.addControl(element.name, control);

    }

    this.setFormDefaultValue();
  }

  setFormDefaultValue() {

    if(!this.form || !this.entity)
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

    if(!this.manager)
      return;

    const id = this.entity?.id ?? null;


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
          }

          if(!id && !!value) {
            this.entity = undefined;
            this.form?.reset();
            this.refreshRequest.emit();
          }

          this.submitResult = !!value;

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
        next: (result) => {

          this.submitResult = result;

          if(result)
            this.entity = undefined;

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
