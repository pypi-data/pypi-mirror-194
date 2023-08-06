import * as Numbro from "@bokeh/numbro";
import { TickFormatter } from "./tick_formatter";
import { RoundingFunction } from "../../core/enums";
export class NumeralTickFormatter extends TickFormatter {
    static __name__ = "NumeralTickFormatter";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ String }) => ({
            // TODO (bev) all of these could be tightened up
            format: [String, "0,0"],
            language: [String, "en"],
            rounding: [RoundingFunction, "round"],
        }));
    }
    get _rounding_fn() {
        switch (this.rounding) {
            case "round":
            case "nearest":
                return Math.round;
            case "floor":
            case "rounddown":
                return Math.floor;
            case "ceil":
            case "roundup":
                return Math.ceil;
        }
    }
    doFormat(ticks, _opts) {
        const { format, language, _rounding_fn } = this;
        return ticks.map((tick) => Numbro.format(tick, format, language, _rounding_fn));
    }
}
//# sourceMappingURL=numeral_tick_formatter.js.map