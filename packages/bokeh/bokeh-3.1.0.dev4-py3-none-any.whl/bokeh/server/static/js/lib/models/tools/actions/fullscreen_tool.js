import { ActionTool, ActionToolView } from "./action_tool";
import * as icons from "../../../styles/icons.css";
export class FullscreenToolView extends ActionToolView {
    static __name__ = "FullscreenToolView";
    doit() {
        if (document.fullscreenElement != null) {
            document.exitFullscreen();
        }
        else {
            (async () => {
                await this.parent.el.requestFullscreen();
            })();
        }
    }
}
export class FullscreenTool extends ActionTool {
    static __name__ = "FullscreenTool";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = FullscreenToolView;
        this.register_alias("fullscreen", () => new FullscreenTool());
    }
    tool_name = "Fullscreen";
    tool_icon = icons.tool_icon_fullscreen;
}
//# sourceMappingURL=fullscreen_tool.js.map