import { Placeholder, PlaceholderView } from "./placeholder";
import { _get_column_value } from "../../core/util/templating";
export class ValueRefView extends PlaceholderView {
    static __name__ = "ValueRefView";
    update(source, i, _vars /*, formatters?: Formatters*/) {
        const value = _get_column_value(this.model.field, source, i);
        const text = value == null ? "???" : `${value}`; //.toString()
        this.el.textContent = text;
    }
}
export class ValueRef extends Placeholder {
    static __name__ = "ValueRef";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = ValueRefView;
        this.define(({ String }) => ({
            field: [String],
        }));
    }
}
//# sourceMappingURL=value_ref.js.map