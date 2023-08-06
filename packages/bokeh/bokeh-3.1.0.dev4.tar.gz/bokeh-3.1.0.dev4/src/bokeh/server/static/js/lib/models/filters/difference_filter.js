import { Filter } from "./filter";
import { Indices } from "../../core/types";
export class DifferenceFilter extends Filter {
    static __name__ = "DifferenceFilter";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ Array, Ref }) => ({
            operands: [Array(Ref(Filter))],
        }));
    }
    compute_indices(source) {
        const { operands } = this;
        if (operands.length == 0) {
            const size = source.get_length() ?? 1;
            return Indices.all_set(size);
        }
        else {
            const [index, ...rest] = operands.map((op) => op.compute_indices(source));
            for (const op of rest) {
                index.subtract(op);
            }
            return index;
        }
    }
}
//# sourceMappingURL=difference_filter.js.map