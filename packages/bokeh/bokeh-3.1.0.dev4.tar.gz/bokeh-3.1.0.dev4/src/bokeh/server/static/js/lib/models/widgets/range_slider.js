import * as numbro from "@bokeh/numbro";
import { AbstractSlider, AbstractRangeSliderView } from "./abstract_slider";
import { isString } from "../../core/util/types";
export class RangeSliderView extends AbstractRangeSliderView {
    static __name__ = "RangeSliderView";
}
export class RangeSlider extends AbstractSlider {
    static __name__ = "RangeSlider";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = RangeSliderView;
        this.override({
            format: "0[.]00",
        });
    }
    behaviour = "drag";
    connected = [false, true, false];
    _formatter(value, format) {
        if (isString(format))
            return numbro.format(value, format);
        else
            return format.compute(value);
    }
}
//# sourceMappingURL=range_slider.js.map