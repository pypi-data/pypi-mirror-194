import * as numbro from "@bokeh/numbro";
import { AbstractSlider, AbstractSliderView } from "./abstract_slider";
import { isString } from "../../core/util/types";
export class SliderView extends AbstractSliderView {
    static __name__ = "SliderView";
}
export class Slider extends AbstractSlider {
    static __name__ = "Slider";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = SliderView;
        this.override({
            format: "0[.]00",
        });
    }
    behaviour = "tap";
    connected = [true, false];
    _formatter(value, format) {
        if (isString(format))
            return numbro.format(value, format);
        else
            return format.compute(value);
    }
}
//# sourceMappingURL=slider.js.map