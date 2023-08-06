import { Expression } from "./expression";
export class CumSum extends Expression {
    static __name__ = "CumSum";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ Boolean, String }) => ({
            field: [String],
            include_zero: [Boolean, false],
        }));
    }
    _v_compute(source) {
        const result = new Float64Array(source.get_length() ?? 0);
        const col = source.data[this.field];
        const offset = this.include_zero ? 1 : 0;
        result[0] = this.include_zero ? 0 : col[0];
        for (let i = 1; i < result.length; i++) {
            result[i] = result[i - 1] + col[i - offset];
        }
        return result;
    }
}
//# sourceMappingURL=cumsum.js.map