import tz from "timezone";
import { AbstractSlider, AbstractRangeSliderView } from "./abstract_slider";
import { isString } from "../../core/util/types";
export class DatetimeRangeSliderView extends AbstractRangeSliderView {
    static __name__ = "DatetimeRangeSliderView";
}
export class DatetimeRangeSlider extends AbstractSlider {
    static __name__ = "DatetimeRangeSlider";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = DatetimeRangeSliderView;
        this.override({
            format: "%d %b %Y %H:%M:%S",
            step: 3600000, // 1 hour.
        });
    }
    behaviour = "drag";
    connected = [false, true, false];
    _formatter(value, format) {
        if (isString(format))
            return tz(value, format);
        else
            return format.compute(value);
    }
}
//# sourceMappingURL=datetime_range_slider.js.map