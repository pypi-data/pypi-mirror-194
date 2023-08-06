import { UIElement, UIElementView } from "../ui/ui_element";
import menus_css from "../../styles/menus.css";
import icons_css from "../../styles/icons.css";
export class MenuItemView extends UIElementView {
    static __name__ = "MenuItemView";
    styles() {
        return [...super.styles(), menus_css, icons_css];
    }
}
export class MenuItem extends UIElement {
    static __name__ = "MenuItem";
    constructor(attrs) {
        super(attrs);
    }
}
//# sourceMappingURL=menu_item.js.map