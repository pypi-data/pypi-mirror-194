import { BaseDatetimePicker, BaseDatetimePickerView } from "./base_datetime_picker";
import { DateLike } from "./base_date_picker";
export class MultipleDatetimePickerView extends BaseDatetimePickerView {
    static __name__ = "MultipleDatetimePickerView";
    get flatpickr_options() {
        return {
            ...super.flatpickr_options,
            mode: "multiple",
            conjunction: this.model.separator,
        };
    }
    _on_change(selected) {
        this.model.value = selected.map((datetime) => this._format_date(datetime));
    }
}
export class MultipleDatetimePicker extends BaseDatetimePicker {
    static __name__ = "MultipleDatetimePicker";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = MultipleDatetimePickerView;
        this.define(({ String, Array }) => ({
            value: [Array(DateLike), []],
            separator: [String, ", "],
        }));
    }
}
//# sourceMappingURL=multiple_datetime_picker.js.map