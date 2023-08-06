import { PickerBase, PickerBaseView } from "./picker_base";
import { String, Number, Or } from "../../core/kinds";
import { Clock } from "../../core/enums";
import { assert } from "../../core/util/assert";
export const TimeLike = Or(String, Number);
export class TimePickerView extends PickerBaseView {
    static __name__ = "TimePickerView";
    _format_time(date) {
        const { picker } = this;
        return picker.formatDate(date, picker.config.dateFormat);
    }
    connect_signals() {
        super.connect_signals();
        const { value, min_time, max_time, time_format, hour_increment, minute_increment, second_increment, seconds, clock, } = this.model.properties;
        this.connect(value.change, () => {
            const { value } = this.model;
            if (value != null) {
                this.picker.setDate(value);
            }
            else {
                this.picker.clear();
            }
        });
        this.connect(min_time.change, () => this.picker.set("minTime", this.model.min_time));
        this.connect(max_time.change, () => this.picker.set("maxTime", this.model.max_time));
        this.connect(time_format.change, () => this.picker.set("altFormat", this.model.time_format));
        this.connect(hour_increment.change, () => this.picker.set("hourIncrement", this.model.hour_increment));
        this.connect(minute_increment.change, () => this.picker.set("minuteIncrement", this.model.minute_increment));
        this.connect(second_increment.change, () => this._update_second_increment());
        this.connect(seconds.change, () => this.picker.set("enableSeconds", this.model.seconds));
        this.connect(clock.change, () => this.picker.set("time_24hr", this.model.clock == "24h"));
    }
    get flatpickr_options() {
        const { value, min_time, max_time, time_format, hour_increment, minute_increment, seconds, clock } = this.model;
        const options = super.flatpickr_options;
        options.enableTime = true;
        options.noCalendar = true;
        options.altInput = true;
        options.altFormat = time_format;
        options.dateFormat = "H:i:S";
        options.hourIncrement = hour_increment;
        options.minuteIncrement = minute_increment;
        options.enableSeconds = seconds;
        options.time_24hr = clock == "24h";
        if (value != null) {
            options.defaultDate = value;
        }
        if (min_time != null) {
            options.minTime = min_time;
        }
        if (max_time != null) {
            options.maxTime = max_time;
        }
        return options;
    }
    render() {
        super.render();
        this._update_second_increment();
    }
    _update_second_increment() {
        const { second_increment } = this.model;
        this.picker.secondElement?.setAttribute("step", second_increment.toString());
    }
    _on_change(selected) {
        switch (selected.length) {
            case 0: {
                this.model.value = null;
                break;
            }
            case 1: {
                const [datetime] = selected;
                const time = this._format_time(datetime);
                this.model.value = time;
                break;
            }
            default: {
                assert(false, "invalid length");
            }
        }
    }
}
export class TimePicker extends PickerBase {
    static __name__ = "TimePicker";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = TimePickerView;
        this.define(({ Boolean, String, Nullable, Positive, Int }) => ({
            value: [Nullable(TimeLike), null],
            min_time: [Nullable(TimeLike), null],
            max_time: [Nullable(TimeLike), null],
            time_format: [String, "H:i"],
            hour_increment: [Positive(Int), 1],
            minute_increment: [Positive(Int), 1],
            second_increment: [Positive(Int), 1],
            seconds: [Boolean, false],
            clock: [Clock, "24h"],
        }));
    }
}
//# sourceMappingURL=time_picker.js.map