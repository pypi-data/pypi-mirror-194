import { Tool, ToolView } from "../tool";
import { OnOffButton } from "../on_off_button";
export class InspectToolView extends ToolView {
    static __name__ = "InspectToolView";
    get plot_view() {
        return this.parent;
    }
}
export class InspectTool extends Tool {
    static __name__ = "InspectTool";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ Boolean }) => ({
            toggleable: [Boolean, true],
        }));
        this.override({
            active: true,
        });
    }
    event_type = "move";
    tool_button() {
        return new OnOffButton({ tool: this });
    }
}
//# sourceMappingURL=inspect_tool.js.map