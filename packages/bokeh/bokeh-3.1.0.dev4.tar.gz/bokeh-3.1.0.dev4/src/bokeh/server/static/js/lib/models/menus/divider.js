import { MenuItem, MenuItemView } from "./menu_item";
import * as menus from "../../styles/menus.css";
export class DividerView extends MenuItemView {
    static __name__ = "DividerView";
    render() {
        super.render();
        this.el.classList.add(menus.divider);
    }
}
export class Divider extends MenuItem {
    static __name__ = "Divider";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = DividerView;
    }
}
//# sourceMappingURL=divider.js.map