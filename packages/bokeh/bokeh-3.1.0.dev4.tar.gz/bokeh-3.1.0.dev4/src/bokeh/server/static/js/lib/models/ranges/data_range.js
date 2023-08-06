import { Range } from "./range";
export class DataRange extends Range {
    static __name__ = "DataRange";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ Array, AnyRef, Or, Auto }) => ({
            renderers: [Or(Array(AnyRef()), Auto), []],
        }));
    }
}
//# sourceMappingURL=data_range.js.map