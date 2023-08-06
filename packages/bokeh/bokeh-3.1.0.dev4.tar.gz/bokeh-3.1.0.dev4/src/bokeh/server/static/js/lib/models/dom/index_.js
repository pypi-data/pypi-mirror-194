import { Placeholder, PlaceholderView } from "./placeholder";
export class IndexView extends PlaceholderView {
    static __name__ = "IndexView";
    update(_source, i, _vars /*, formatters?: Formatters*/) {
        this.el.textContent = i == null ? "(null)" : i.toString();
    }
}
export class Index extends Placeholder {
    static __name__ = "Index";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = IndexView;
    }
}
//# sourceMappingURL=index_.js.map