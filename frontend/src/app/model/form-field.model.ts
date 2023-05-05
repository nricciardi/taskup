import { AsyncValidator, FormControl, Validator } from "@angular/forms";

export interface SelectOption {
  value: number | null;
  text: string;
}

export interface FormField {
  title?: string;
  name: string;
  type: string;
  placeholder?: string;
  blueprintFormControl: FormControl;
  selectOptions?: SelectOption[];
  unique?: boolean;
}
