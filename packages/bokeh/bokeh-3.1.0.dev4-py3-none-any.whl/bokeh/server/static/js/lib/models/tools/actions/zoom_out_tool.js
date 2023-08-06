import { ZoomBaseTool, ZoomBaseToolView } from "./zoom_base_tool";
import { tool_icon_zoom_out } from "../../../styles/icons.css";
export class ZoomOutToolView extends ZoomBaseToolView {
    static __name__ = "ZoomOutToolView";
}
export class ZoomOutTool extends ZoomBaseTool {
    static __name__ = "ZoomOutTool";
    maintain_focus;
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = ZoomOutToolView;
        this.define(({ Boolean }) => ({
            maintain_focus: [Boolean, true],
        }));
        this.register_alias("zoom_out", () => new ZoomOutTool({ dimensions: "both" }));
        this.register_alias("xzoom_out", () => new ZoomOutTool({ dimensions: "width" }));
        this.register_alias("yzoom_out", () => new ZoomOutTool({ dimensions: "height" }));
    }
    get_factor() {
        return -this.factor / (1 - this.factor);
    }
    tool_name = "Zoom Out";
    tool_icon = tool_icon_zoom_out;
}
//# sourceMappingURL=zoom_out_tool.js.map