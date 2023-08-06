import { ScalarExpression } from "./expression";
import { dict } from "../../core/util/object";
import { max } from "../../core/util/array";
export class Maximum extends ScalarExpression {
    static __name__ = "Maximum";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ Number, String }) => ({
            field: [String],
            initial: [Number, -Infinity],
        }));
    }
    _compute(source) {
        const column = dict(source.data).get(this.field) ?? [];
        return Math.max(this.initial, max(column));
    }
}
//# sourceMappingURL=maximum.js.map