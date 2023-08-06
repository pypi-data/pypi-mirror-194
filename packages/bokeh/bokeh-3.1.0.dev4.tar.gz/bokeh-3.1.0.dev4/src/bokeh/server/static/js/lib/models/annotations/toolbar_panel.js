import { Annotation, AnnotationView } from "./annotation";
import { Toolbar } from "../tools/toolbar";
import { build_view } from "../../core/build_views";
import { div, empty, position, display, undisplay, remove } from "../../core/dom";
import { SideLayout } from "../../core/layout/side_panel";
import { BBox } from "../../core/util/bbox";
export class ToolbarPanelView extends AnnotationView {
    static __name__ = "ToolbarPanelView";
    update_layout() {
        this.layout = new SideLayout(this.panel, () => this.get_size(), true);
    }
    has_finished() {
        return super.has_finished() && this.toolbar_view.has_finished();
    }
    *children() {
        yield* super.children();
        yield this.toolbar_view;
    }
    toolbar_view;
    el = div();
    async lazy_initialize() {
        await super.lazy_initialize();
        this.toolbar_view = await build_view(this.model.toolbar, { parent: this.canvas });
    }
    connect_signals() {
        super.connect_signals();
        this.plot_view.mouseenter.connect(() => {
            this.toolbar_view.set_visibility(true);
        });
        this.plot_view.mouseleave.connect(() => {
            this.toolbar_view.set_visibility(false);
        });
    }
    remove() {
        this.toolbar_view.remove();
        remove(this.el);
        super.remove();
    }
    _previous_bbox = new BBox();
    _render() {
        display(this.el);
        // TODO: this should be handled by the layout
        const { bbox } = this.layout;
        if (!this._previous_bbox.equals(bbox)) {
            position(this.el, bbox);
            this._previous_bbox = bbox;
            empty(this.el);
            this.el.style.position = "absolute";
            const { style } = this.toolbar_view.el;
            if (this.toolbar_view.model.horizontal) {
                style.width = "100%";
                style.height = "unset";
            }
            else {
                style.width = "unset";
                style.height = "100%";
            }
            this.toolbar_view.render();
            this.plot_view.canvas_view.add_event(this.el);
            this.el.appendChild(this.toolbar_view.el);
            this.toolbar_view.after_render();
        }
        if (!this.model.visible) {
            undisplay(this.el);
        }
    }
    _get_size() {
        const { tools, logo } = this.model.toolbar;
        return {
            width: tools.length * 30 + (logo != null ? 25 : 0) + 15,
            height: 30,
        };
    }
}
export class ToolbarPanel extends Annotation {
    static __name__ = "ToolbarPanel";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = ToolbarPanelView;
        this.define(({ Ref }) => ({
            toolbar: [Ref(Toolbar)],
        }));
    }
}
//# sourceMappingURL=toolbar_panel.js.map