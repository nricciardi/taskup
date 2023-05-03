import { FormControl } from "@angular/forms";

export interface FormField {
  name: string;
  type: string;
  placeholder?: string;
  formControl: FormControl
}
