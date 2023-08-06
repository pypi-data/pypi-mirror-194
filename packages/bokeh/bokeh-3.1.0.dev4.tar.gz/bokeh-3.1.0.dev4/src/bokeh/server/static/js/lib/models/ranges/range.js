import { Model } from "../../model";
export class Range extends Model {
    static __name__ = "Range";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ Number, Tuple, Or, Auto, Nullable }) => ({
            bounds: [Nullable(Or(Tuple(Nullable(Number), Nullable(Number)), Auto)), null],
            min_interval: [Nullable(Number), null],
            max_interval: [Nullable(Number), null],
        }));
    }
    have_updated_interactively = false;
    get is_reversed() {
        return this.start > this.end;
    }
    get is_valid() {
        return isFinite(this.min) && isFinite(this.max);
    }
    get span() {
        return Math.abs(this.end - this.start);
    }
    /** internal */
    plots = new Set();
}
//# sourceMappingURL=range.js.map