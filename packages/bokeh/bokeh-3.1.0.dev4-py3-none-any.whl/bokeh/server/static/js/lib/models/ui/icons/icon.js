import { Model } from "../../../model";
import { DOMComponentView } from "../../../core/dom_view";
export class IconView extends DOMComponentView {
    static __name__ = "IconView";
}
export class Icon extends Model {
    static __name__ = "Icon";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ Number, Or, CSSLength }) => ({
            size: [Or(Number, CSSLength), "1em"],
        }));
    }
}
//# sourceMappingURL=icon.js.map