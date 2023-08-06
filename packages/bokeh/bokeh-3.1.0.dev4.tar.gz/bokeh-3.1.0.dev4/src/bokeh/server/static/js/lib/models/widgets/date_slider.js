import tz from "timezone";
import { AbstractSlider, AbstractSliderView } from "./abstract_slider";
import { isString } from "../../core/util/types";
export class DateSliderView extends AbstractSliderView {
    static __name__ = "DateSliderView";
    _calc_to() {
        const { start, end, value, step } = this.model;
        return {
            start,
            end,
            value: [value],
            step: step * 86400000,
        };
    }
}
export class DateSlider extends AbstractSlider {
    static __name__ = "DateSlider";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = DateSliderView;
        this.override({
            format: "%d %b %Y",
        });
    }
    behaviour = "tap";
    connected = [true, false];
    _formatter(value, format) {
        if (isString(format))
            return tz(value, format);
        else
            return format.compute(value);
    }
}
//# sourceMappingURL=date_slider.js.map