import { PlotActionTool, PlotActionToolView } from "./plot_action_tool";
import { Dimensions } from "../../../core/enums";
import { scale_range } from "../../../core/util/zoom";
export class ZoomBaseToolView extends PlotActionToolView {
    static __name__ = "ZoomBaseToolView";
    doit() {
        const frame = this.plot_view.frame;
        const dims = this.model.dimensions;
        // restrict to axis configured in tool's dimensions property
        const h_axis = dims == "width" || dims == "both";
        const v_axis = dims == "height" || dims == "both";
        const factor = this.model.get_factor();
        const zoom_info = scale_range(frame, factor, h_axis, v_axis);
        this.plot_view.state.push("zoom_out", { range: zoom_info });
        this.plot_view.update_range(zoom_info, { scrolling: true, maintain_focus: this.model.maintain_focus });
        this.model.document?.interactive_start(this.plot_view.model);
        this.plot_view.trigger_ranges_update_event();
    }
}
export class ZoomBaseTool extends PlotActionTool {
    static __name__ = "ZoomBaseTool";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ Percent }) => ({
            factor: [Percent, 0.1],
            dimensions: [Dimensions, "both"],
        }));
    }
    get tooltip() {
        return this._get_dim_tooltip(this.dimensions);
    }
}
//# sourceMappingURL=zoom_base_tool.js.map