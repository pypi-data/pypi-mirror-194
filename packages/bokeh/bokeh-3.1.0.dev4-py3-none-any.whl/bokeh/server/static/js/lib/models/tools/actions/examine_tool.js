import { ActionTool, ActionToolView } from "./action_tool";
import * as icons from "../../../styles/icons.css";
import { Dialog } from "../../ui/dialog";
import { Examiner } from "../../ui/examiner";
import { build_view } from "../../../core/build_views";
export class ExamineToolView extends ActionToolView {
    static __name__ = "ExamineToolView";
    _dialog;
    *children() {
        yield* super.children();
        yield this._dialog;
    }
    async lazy_initialize() {
        await super.lazy_initialize();
        const dialog = new Dialog({
            content: new Examiner({ target: this.parent.model }),
            closable: true,
            visible: false,
        });
        this._dialog = await build_view(dialog, { parent: this.parent });
    }
    doit() {
        this._dialog.model.visible = true;
    }
}
export class ExamineTool extends ActionTool {
    static __name__ = "ExamineTool";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = ExamineToolView;
        this.register_alias("examine", () => new ExamineTool());
    }
    tool_name = "Examine";
    tool_icon = icons.tool_icon_settings; // TODO: better icon
}
//# sourceMappingURL=examine_tool.js.map