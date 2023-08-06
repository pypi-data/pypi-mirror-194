import { SelectTool, SelectToolView } from "./select_tool";
export class RegionSelectToolView extends SelectToolView {
    static __name__ = "RegionSelectToolView";
    get overlays() {
        return [...super.overlays, this.model.overlay];
    }
    _is_continuous(ev) {
        return this.model.continuous != ev.alt_key;
    }
    _select(geometry, final, mode) {
        const renderers_by_source = this._computed_renderers_by_data_source();
        for (const [, renderers] of renderers_by_source) {
            const sm = renderers[0].get_selection_manager();
            const r_views = [];
            for (const r of renderers) {
                const r_view = this.plot_view.renderer_view(r);
                if (r_view != null) {
                    r_views.push(r_view);
                }
            }
            sm.select(r_views, geometry, final, mode);
        }
        this._emit_selection_event(geometry, final);
    }
    _clear_overlay() {
        super._clear_overlay();
        this.model.overlay.clear();
    }
}
export class RegionSelectTool extends SelectTool {
    static __name__ = "RegionSelectTool";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ Boolean }) => ({
            continuous: [Boolean, false],
            persistent: [Boolean, false],
        }));
    }
}
//# sourceMappingURL=region_select_tool.js.map