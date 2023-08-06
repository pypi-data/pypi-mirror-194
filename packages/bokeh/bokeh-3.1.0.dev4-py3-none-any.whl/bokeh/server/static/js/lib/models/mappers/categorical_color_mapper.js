import { cat_v_compute } from "./categorical_mapper";
import { ColorMapper } from "./color_mapper";
import { FactorSeq } from "../ranges/factor_range";
export class CategoricalColorMapper extends ColorMapper {
    static __name__ = "CategoricalColorMapper";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ Number, Nullable }) => ({
            factors: [FactorSeq],
            start: [Number, 0],
            end: [Nullable(Number), null],
        }));
    }
    _v_compute(data, values, palette, { nan_color }) {
        cat_v_compute(data, this.factors, palette, values, this.start, this.end, nan_color);
    }
}
//# sourceMappingURL=categorical_color_mapper.js.map