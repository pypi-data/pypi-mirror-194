import { DOMNode, DOMNodeView } from "./dom_node";
export class TextView extends DOMNodeView {
    static __name__ = "TextView";
    render() {
        this.el.textContent = this.model.content;
    }
    _createElement() {
        return document.createTextNode("");
    }
}
export class Text extends DOMNode {
    static __name__ = "Text";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = TextView;
        this.define(({ String }) => ({
            content: [String, ""],
        }));
    }
}
//# sourceMappingURL=text.js.map