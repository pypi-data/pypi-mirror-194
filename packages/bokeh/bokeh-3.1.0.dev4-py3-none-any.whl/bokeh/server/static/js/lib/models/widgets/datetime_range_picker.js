import { BaseDatetimePicker, BaseDatetimePickerView } from "./base_datetime_picker";
import { DateLike } from "./base_date_picker";
import { assert } from "../../core/util/assert";
export class DatetimeRangePickerView extends BaseDatetimePickerView {
    static __name__ = "DatetimeRangePickerView";
    get flatpickr_options() {
        return {
            ...super.flatpickr_options,
            mode: "range",
        };
    }
    _on_change(selected) {
        switch (selected.length) {
            case 0:
                this.model.value = null;
                break;
            case 1: {
                const [datetime] = selected;
                const date = this._format_date(datetime);
                this.model.value = [date, date];
                break;
            }
            case 2: {
                const [from, to] = selected;
                const from_date = this._format_date(from);
                const to_date = this._format_date(to);
                this.model.value = [from_date, to_date];
                break;
            }
            default: {
                assert(false, "invalid length");
            }
        }
    }
}
export class DatetimeRangePicker extends BaseDatetimePicker {
    static __name__ = "DatetimeRangePicker";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = DatetimeRangePickerView;
        this.define(({ Nullable, Tuple }) => ({
            value: [Nullable(Tuple(DateLike, DateLike)), null],
        }));
    }
}
//# sourceMappingURL=datetime_range_picker.js.map