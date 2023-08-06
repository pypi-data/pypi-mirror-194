import tz from "timezone";
import { AbstractSlider, AbstractRangeSliderView } from "./abstract_slider";
import { isString } from "../../core/util/types";
export class DateRangeSliderView extends AbstractRangeSliderView {
    static __name__ = "DateRangeSliderView";
    _calc_to() {
        const { start, end, value, step } = this.model;
        return {
            start,
            end,
            value,
            step: step * 86400000,
        };
    }
}
export class DateRangeSlider extends AbstractSlider {
    static __name__ = "DateRangeSlider";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = DateRangeSliderView;
        this.override({
            format: "%d %b %Y",
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
//# sourceMappingURL=date_range_slider.js.map