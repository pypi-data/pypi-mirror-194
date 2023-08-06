import { GestureTool, GestureToolView } from "./gesture_tool";
import { GlyphRenderer } from "../../renderers/glyph_renderer";
import { GraphRenderer } from "../../renderers/graph_renderer";
import { DataRenderer } from "../../renderers/data_renderer";
import { compute_renderers } from "../../util";
import { SelectionMode } from "../../../core/enums";
import { SelectionGeometry } from "../../../core/bokeh_events";
import { Signal0 } from "../../../core/signaling";
import { unreachable } from "../../../core/util/assert";
export class SelectToolView extends GestureToolView {
    static __name__ = "SelectToolView";
    connect_signals() {
        super.connect_signals();
        this.model.clear.connect(() => this._clear_selection());
    }
    get computed_renderers() {
        const { renderers } = this.model;
        const all_renderers = this.plot_view.model.data_renderers;
        return compute_renderers(renderers, all_renderers);
    }
    _computed_renderers_by_data_source() {
        const renderers_by_source = new Map();
        for (const r of this.computed_renderers) {
            let source;
            if (r instanceof GlyphRenderer)
                source = r.data_source;
            else if (r instanceof GraphRenderer)
                source = r.node_renderer.data_source;
            else
                continue;
            const renderers = renderers_by_source.get(source) ?? [];
            renderers_by_source.set(source, [...renderers, r]);
        }
        return renderers_by_source;
    }
    _clear_overlay() { }
    _clear_other_overlays() {
        for (const view of this.plot_view.tool_views.values()) {
            if (view instanceof SelectToolView && view != this) {
                view._clear_overlay();
            }
        }
    }
    _clear_selection() {
        this._clear();
    }
    _select_mode(ev) {
        const { shift_key, ctrl_key } = ev;
        if (!shift_key && !ctrl_key)
            return this.model.mode;
        else if (shift_key && !ctrl_key)
            return "append";
        else if (!shift_key && ctrl_key)
            return "intersect";
        else if (shift_key && ctrl_key)
            return "subtract";
        else
            unreachable();
    }
    _keyup(ev) {
        if (!this.model.active)
            return;
        if (ev.key == "Escape") {
            this._clear();
        }
    }
    _clear() {
        for (const renderer of this.computed_renderers) {
            renderer.get_selection_manager().clear();
        }
        const renderer_views = this.computed_renderers.map((r) => this.plot_view.renderer_view(r));
        this.plot_view.request_paint(renderer_views);
    }
    _emit_selection_event(geometry, final = true) {
        const { x_scale, y_scale } = this.plot_view.frame;
        const geometry_data = (() => {
            switch (geometry.type) {
                case "point": {
                    const { sx, sy } = geometry;
                    const x = x_scale.invert(sx);
                    const y = y_scale.invert(sy);
                    return { ...geometry, x, y };
                }
                case "span": {
                    const { sx, sy } = geometry;
                    const x = x_scale.invert(sx);
                    const y = y_scale.invert(sy);
                    return { ...geometry, x, y };
                }
                case "rect": {
                    const { sx0, sx1, sy0, sy1 } = geometry;
                    const [x0, x1] = x_scale.r_invert(sx0, sx1);
                    const [y0, y1] = y_scale.r_invert(sy0, sy1);
                    return { ...geometry, x0, y0, x1, y1 };
                }
                case "poly": {
                    const { sx, sy } = geometry;
                    const x = x_scale.v_invert(sx);
                    const y = y_scale.v_invert(sy);
                    return { ...geometry, x, y };
                }
            }
        })();
        this.plot_view.model.trigger_event(new SelectionGeometry(geometry_data, final));
    }
}
export class SelectTool extends GestureTool {
    static __name__ = "SelectTool";
    clear;
    constructor(attrs) {
        super(attrs);
    }
    initialize() {
        super.initialize();
        this.clear = new Signal0(this, "clear");
    }
    static {
        this.define(({ Array, Ref, Or, Auto }) => ({
            renderers: [Or(Array(Ref(DataRenderer)), Auto), "auto"],
            mode: [SelectionMode, "replace"],
        }));
    }
    get menu() {
        return [
            {
                icon: "bk-tool-icon-replace-mode",
                tooltip: "Replace the current selection",
                active: () => this.mode == "replace",
                handler: () => {
                    this.mode = "replace";
                    this.active = true;
                },
            }, {
                icon: "bk-tool-icon-append-mode",
                tooltip: "Append to the current selection (Shift)",
                active: () => this.mode == "append",
                handler: () => {
                    this.mode = "append";
                    this.active = true;
                },
            }, {
                icon: "bk-tool-icon-intersect-mode",
                tooltip: "Intersect with the current selection (Ctrl)",
                active: () => this.mode == "intersect",
                handler: () => {
                    this.mode = "intersect";
                    this.active = true;
                },
            }, {
                icon: "bk-tool-icon-subtract-mode",
                tooltip: "Subtract from the current selection (Shift+Ctrl)",
                active: () => this.mode == "subtract",
                handler: () => {
                    this.mode = "subtract";
                    this.active = true;
                },
            },
            null,
            {
                icon: "bk-tool-icon-clear-selection",
                tooltip: "Clear the current selection and/or selection overlay (Esc)",
                handler: () => {
                    this.clear.emit();
                },
            },
        ];
    }
}
//# sourceMappingURL=select_tool.js.map