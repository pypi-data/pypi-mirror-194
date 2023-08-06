import { DOMNode, DOMNodeView } from "./dom_node";
import { HasProps } from "../../core/has_props";
import { empty } from "../../core/dom";
import { to_string } from "../../core/util/pretty";
export class ValueOfView extends DOMNodeView {
    static __name__ = "ValueOfView";
    connect_signals() {
        super.connect_signals();
        const { obj, attr } = this.model;
        if (attr in obj.properties) {
            this.on_change(obj.properties[attr], () => this.render());
        }
    }
    render() {
        empty(this.el);
        this.el.style.display = "contents";
        const text = (() => {
            const { obj, attr } = this.model;
            if (attr in obj.properties) {
                const value = obj.properties[attr].get_value();
                return to_string(value);
            }
            else
                return `<not found: ${obj.type}.${attr}>`;
        })();
        this.el.textContent = text;
    }
}
export class ValueOf extends DOMNode {
    static __name__ = "ValueOf";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = ValueOfView;
        this.define(({ String, Ref }) => ({
            obj: [Ref(HasProps)],
            attr: [String],
        }));
    }
}
//# sourceMappingURL=value_of.js.map