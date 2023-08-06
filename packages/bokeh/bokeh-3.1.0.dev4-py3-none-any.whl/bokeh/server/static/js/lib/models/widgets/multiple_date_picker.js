import { BaseDatePicker, BaseDatePickerView, DateLike } from "./base_date_picker";
export class MultipleDatePickerView extends BaseDatePickerView {
    static __name__ = "MultipleDatePickerView";
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
export class MultipleDatePicker extends BaseDatePicker {
    static __name__ = "MultipleDatePicker";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = MultipleDatePickerView;
        this.define(({ String, Array }) => ({
            value: [Array(DateLike), []],
            separator: [String, ", "],
        }));
    }
}
//# sourceMappingURL=multiple_date_picker.js.map