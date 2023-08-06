import { Model } from "../../model";
export class Selector extends Model {
    static __name__ = "Selector";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ String }) => ({
            query: [String],
        }));
    }
}
//# sourceMappingURL=selector.js.map