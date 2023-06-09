import { Component, EventEmitter, Input, Output, SimpleChanges } from '@angular/core';
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

  readonly DEFAULT_COLOR: string = "#000000";

  @Input("manager") manager?: M;
  @Input("entity") entity?: E;
  @Input("title") title?: string;
  @Input("editableFields") editableFields: FormField[] = [];
  @Input("confirmBtnTxt") confirmBtnTxt: string = "modify";
  @Input("collapseStatus") collapseStatus: boolean = false;

  @Output() refreshRequest = new EventEmitter<void>();
  @Output() onConfirm = new EventEmitter<E>();

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

      // create form controls as copy of blueprint form control
      const blueprint = element.blueprintFormControl;

      if(element.type == 'color')
        blueprint.setValue(this.DEFAULT_COLOR);   // set a default color

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

      if(element.type != 'password')
        control.setValue(value);

    }
  }

  submit() {


    if(this.form?.valid) {
      this.modify(this.form.value);
    }
  }

  modify(values: any) {

    const id = this.entity?.id ?? null;

    const resetResultFlag = () => {
      setTimeout(() => {
        this.submitResult = undefined;
      }, environment.alertTimeout);
    }


    this.onConfirm.emit(values);

    if(!!this.manager) {
      this.manager.update(id, values).then((response) => {

        response.subscribe({
          next: (value) => {
            if(value) {
              this.entity = value;
              this.form?.markAsPristine();
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

  }

  delete() {
    if(!this.entity)
      return;

    const id = this.entity.id;

    const resetResultFlag = () => {
      setTimeout(() => {
        this.submitResult = undefined;
      }, environment.alertTimeout);
    }

    if(!!this.manager) {

      this.manager?.deleteById(id).then((response) => {

        response.subscribe({
          next: (result) => {

            result = !!result;

            this.submitResult = result;

            if(result) {
              this.entity = undefined;
              this.refreshRequest.emit();
            }

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
}
