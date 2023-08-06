import { ActionTool, ActionToolView } from "./action_tool";
import { tool_icon_save } from "../../../styles/icons.css";
export class SaveToolView extends ActionToolView {
    static __name__ = "SaveToolView";
    async copy() {
        const blob = await this.parent.export().to_blob();
        const item = new ClipboardItem({ [blob.type]: blob });
        await navigator.clipboard.write([item]);
    }
    async save(name) {
        const blob = await this.parent.export().to_blob();
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = name; // + ".png" | "svg" (inferred from MIME type)
        link.target = "_blank";
        link.dispatchEvent(new MouseEvent("click"));
    }
    doit(action = "save") {
        switch (action) {
            case "save": {
                const filename = this.model.filename ?? prompt("Enter filename", "bokeh_plot");
                if (filename != null) {
                    this.save(filename);
                }
                break;
            }
            case "copy": {
                this.copy();
                break;
            }
        }
    }
}
export class SaveTool extends ActionTool {
    static __name__ = "SaveTool";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = SaveToolView;
        this.define(({ String, Nullable }) => ({
            filename: [Nullable(String), null],
        }));
        this.register_alias("save", () => new SaveTool());
    }
    tool_name = "Save";
    tool_icon = tool_icon_save;
    get menu() {
        return [
            {
                icon: "bk-tool-icon-copy",
                tooltip: "Copy image to clipboard",
                if: () => typeof ClipboardItem !== "undefined",
                handler: () => {
                    this.do.emit("copy");
                },
            },
        ];
    }
}
//# sourceMappingURL=save_tool.js.map