import { ZoomBaseTool, ZoomBaseToolView } from "./zoom_base_tool";
import { tool_icon_zoom_in } from "../../../styles/icons.css";
export class ZoomInToolView extends ZoomBaseToolView {
    static __name__ = "ZoomInToolView";
}
export class ZoomInTool extends ZoomBaseTool {
    static __name__ = "ZoomInTool";
    maintain_focus = true;
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = ZoomInToolView;
        this.register_alias("zoom_in", () => new ZoomInTool({ dimensions: "both" }));
        this.register_alias("xzoom_in", () => new ZoomInTool({ dimensions: "width" }));
        this.register_alias("yzoom_in", () => new ZoomInTool({ dimensions: "height" }));
    }
    get_factor() {
        return this.factor;
    }
    tool_name = "Zoom In";
    tool_icon = tool_icon_zoom_in;
}
//# sourceMappingURL=zoom_in_tool.js.map