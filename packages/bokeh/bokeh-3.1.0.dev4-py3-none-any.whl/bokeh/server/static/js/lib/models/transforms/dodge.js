import { RangeTransform } from "./range_transform";
export class Dodge extends RangeTransform {
    static __name__ = "Dodge";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ Number }) => ({
            value: [Number, 0],
        }));
    }
    _compute(x) {
        return x + this.value;
    }
}
//# sourceMappingURL=dodge.js.map