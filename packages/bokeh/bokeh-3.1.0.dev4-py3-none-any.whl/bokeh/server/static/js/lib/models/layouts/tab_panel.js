import { Model } from "../../model";
import { UIElement } from "../ui/ui_element";
export class TabPanel extends Model {
    static __name__ = "TabPanel";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ Boolean, String, Ref }) => ({
            title: [String, ""],
            child: [Ref(UIElement)],
            closable: [Boolean, false],
            disabled: [Boolean, false],
        }));
    }
}
//# sourceMappingURL=tab_panel.js.map