import { BaseDatePicker, BaseDatePickerView, DateLike } from "./base_date_picker";
import { assert } from "../../core/util/assert";
export class DatePickerView extends BaseDatePickerView {
    static __name__ = "DatePickerView";
    get flatpickr_options() {
        return {
            ...super.flatpickr_options,
            mode: "single",
        };
    }
    _on_change(selected) {
        switch (selected.length) {
            case 0: {
                this.model.value = null;
                break;
            }
            case 1: {
                const [datetime] = selected;
                const date = this._format_date(datetime);
                this.model.value = date;
                break;
            }
            default: {
                assert(false, "invalid length");
            }
        }
    }
}
export class DatePicker extends BaseDatePicker {
    static __name__ = "DatePicker";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = DatePickerView;
        this.define(({ Nullable }) => ({
            value: [Nullable(DateLike), null],
        }));
    }
}
//# sourceMappingURL=date_picker.js.map