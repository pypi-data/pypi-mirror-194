import { Filter } from "./filter";
export class InversionFilter extends Filter {
    static __name__ = "InversionFilter";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ Ref }) => ({
            operand: [Ref(Filter)],
        }));
    }
    compute_indices(source) {
        const index = this.operand.compute_indices(source);
        index.invert();
        return index;
    }
}
//# sourceMappingURL=inversion_filter.js.map