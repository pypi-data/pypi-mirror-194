import { BaseDatetimePicker, BaseDatetimePickerView } from "./base_datetime_picker";
import { DateLike } from "./base_date_picker";
import { assert } from "../../core/util/assert";
export class DatetimePickerView extends BaseDatetimePickerView {
    static __name__ = "DatetimePickerView";
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
export class DatetimePicker extends BaseDatetimePicker {
    static __name__ = "DatetimePicker";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = DatetimePickerView;
        this.define(({ Nullable }) => ({
            value: [Nullable(DateLike), null],
        }));
    }
}
//# sourceMappingURL=datetime_picker.js.map