import { AsyncValidator, FormControl, Validator } from "@angular/forms";

export interface FormField {
  name: string;
  type: string;
  placeholder?: string;
  blueprintFormControl: FormControl;
}
