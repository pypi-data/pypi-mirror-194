import { Tool, ToolView } from "../tool";
import { OnOffButton } from "../on_off_button";
import { BoxAnnotation } from "../../annotations/box_annotation";
import { Range1d } from "../../ranges/range1d";
import { logger } from "../../../core/logging";
import { tool_icon_range } from "../../../styles/icons.css";
export class RangeToolView extends ToolView {
    static __name__ = "RangeToolView";
    get overlays() {
        return [...super.overlays, this.model.overlay];
    }
    initialize() {
        super.initialize();
        this.model.update_overlay_from_ranges();
    }
    connect_signals() {
        super.connect_signals();
        if (this.model.x_range != null)
            this.connect(this.model.x_range.change, () => this.model.update_overlay_from_ranges());
        if (this.model.y_range != null)
            this.connect(this.model.y_range.change, () => this.model.update_overlay_from_ranges());
        this.model.overlay.pan.connect(([state, _]) => {
            if (state == "pan") {
                this.model.update_ranges_from_overlay();
            }
            else if (state == "pan:end") {
                this.parent.trigger_ranges_update_event();
            }
        });
        const { active } = this.model.properties;
        this.on_change(active, () => {
            this.model.overlay.editable = this.model.active;
        });
    }
}
const DEFAULT_RANGE_OVERLAY = () => {
    return new BoxAnnotation({
        syncable: false,
        level: "overlay",
        visible: true,
        editable: true,
        propagate_hover: true,
        fill_color: "lightgrey",
        fill_alpha: 0.5,
        line_color: "black",
        line_alpha: 1.0,
        line_width: 0.5,
        line_dash: [2, 2],
    });
};
export class RangeTool extends Tool {
    static __name__ = "RangeTool";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = RangeToolView;
        this.define(({ Boolean, Ref, Nullable }) => ({
            x_range: [Nullable(Ref(Range1d)), null],
            y_range: [Nullable(Ref(Range1d)), null],
            x_interaction: [Boolean, true],
            y_interaction: [Boolean, true],
            overlay: [Ref(BoxAnnotation), DEFAULT_RANGE_OVERLAY],
        }));
        this.override({
            active: true,
        });
    }
    initialize() {
        super.initialize();
        this.overlay.editable = this.active;
        const has_x = this.x_range != null && this.x_interaction;
        const has_y = this.y_range != null && this.y_interaction;
        if (has_x && has_y) {
            this.overlay.movable = "both";
            this.overlay.resizable = "all";
        }
        else if (has_x) {
            this.overlay.movable = "x";
            this.overlay.resizable = "x";
        }
        else if (has_y) {
            this.overlay.movable = "y";
            this.overlay.resizable = "y";
        }
        else {
            this.overlay.movable = "none";
            this.overlay.resizable = "none";
        }
    }
    update_ranges_from_overlay() {
        const { left, right, top, bottom } = this.overlay;
        if (this.x_range != null && this.x_interaction)
            this.x_range.setv({ start: left, end: right });
        if (this.y_range != null && this.y_interaction)
            this.y_range.setv({ start: bottom, end: top });
    }
    update_overlay_from_ranges() {
        const { x_range, y_range } = this;
        const has_x = x_range != null;
        const has_y = y_range != null;
        if (!has_x && !has_y) {
            this.overlay.clear();
            logger.warn("RangeTool not configured with any Ranges.");
        }
        else {
            // TODO: relace null with symbolic frame bounds
            this.overlay.update({
                left: has_x ? x_range.start : null,
                right: has_x ? x_range.end : null,
                bottom: has_y ? y_range.start : null,
                top: has_y ? y_range.end : null,
            });
        }
    }
    tool_name = "Range Tool";
    tool_icon = tool_icon_range;
    tool_button() {
        return new OnOffButton({ tool: this });
    }
}
//# sourceMappingURL=range_tool.js.map