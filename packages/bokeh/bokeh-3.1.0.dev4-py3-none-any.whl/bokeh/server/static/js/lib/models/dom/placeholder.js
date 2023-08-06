import { DOMNode, DOMNodeView } from "./dom_node";
export class PlaceholderView extends DOMNodeView {
    static __name__ = "PlaceholderView";
    static tag_name = "span";
    render() {
        // XXX: no implementation?
    }
}
export class Placeholder extends DOMNode {
    static __name__ = "Placeholder";
    constructor(attrs) {
        super(attrs);
    }
}
//# sourceMappingURL=placeholder.js.map