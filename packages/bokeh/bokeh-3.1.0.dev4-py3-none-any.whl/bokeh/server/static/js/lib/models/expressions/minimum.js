import { ScalarExpression } from "./expression";
import { dict } from "../../core/util/object";
import { min } from "../../core/util/array";
export class Minimum extends ScalarExpression {
    static __name__ = "Minimum";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ Number, String }) => ({
            field: [String],
            initial: [Number, Infinity],
        }));
    }
    _compute(source) {
        const column = dict(source.data).get(this.field) ?? [];
        return Math.min(this.initial, min(column));
    }
}
//# sourceMappingURL=minimum.js.map