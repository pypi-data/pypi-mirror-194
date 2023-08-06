import { UIElement, UIElementView } from "./ui_element";
import { build_views, remove_views } from "../../core/build_views";
import { isString } from "../../core/util/types";
export class PaneView extends UIElementView {
    static __name__ = "PaneView";
    get _ui_elements() {
        return this.model.children.filter((child) => child instanceof UIElement);
    }
    _child_views = new Map();
    get child_views() {
        return this._ui_elements.map((child) => this._child_views.get(child));
    }
    *children() {
        yield* super.children();
        yield* this._child_views.values();
    }
    async lazy_initialize() {
        await super.lazy_initialize();
        await this._rebuild_views();
    }
    async _rebuild_views() {
        await build_views(this._child_views, this._ui_elements, { parent: this });
    }
    remove() {
        remove_views(this._child_views);
        super.remove();
    }
    connect_signals() {
        super.connect_signals();
        const { children } = this.model.properties;
        this.on_change(children, () => {
            this._rebuild_views();
            this.render();
        });
    }
    render() {
        super.render();
        for (const child of this.model.children) {
            if (isString(child)) {
                const text = document.createTextNode(child);
                this.shadow_el.append(text);
            }
            else {
                const child_view = this._child_views.get(child);
                child_view.render();
                this.shadow_el.append(child_view.el);
                child_view.after_render();
            }
        }
    }
    has_finished() {
        if (!super.has_finished())
            return false;
        for (const child_view of this.child_views) {
            if (!child_view.has_finished())
                return false;
        }
        return true;
    }
    serializable_state() {
        return {
            ...super.serializable_state(),
            children: this.child_views.map((child) => child.serializable_state()),
        };
    }
}
export class Pane extends UIElement {
    static __name__ = "Pane";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = PaneView;
        this.define(({ String, Array, Ref, Or }) => ({
            children: [Array(Or(String, Ref(UIElement))), []],
        }));
    }
}
//# sourceMappingURL=pane.js.map