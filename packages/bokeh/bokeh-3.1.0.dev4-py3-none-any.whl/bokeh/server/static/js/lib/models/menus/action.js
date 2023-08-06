import { MenuItem, MenuItemView } from "./menu_item";
import { Menu } from "./menu";
import { Icon } from "../ui/icons/icon";
import { span } from "../../core/dom";
// import * as menus from "styles/menus.css"
export class ActionView extends MenuItemView {
    static __name__ = "ActionView";
    _click() {
    }
    render() {
        super.render();
        const { label, description } = this.model;
        this.el.tabIndex = 0;
        this.el.title = description ?? "";
        this.el.appendChild(span(label));
        this.el.addEventListener("click", () => {
            this._click();
        });
        this.el.addEventListener("keydown", (event) => {
            if (event.key == "Enter") {
                this._click();
            }
        });
    }
}
export class Action extends MenuItem {
    static __name__ = "Action";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = ActionView;
        this.define(({ String, Nullable, Ref }) => ({
            icon: [Nullable(Ref(Icon)), null],
            label: [String],
            description: [Nullable(String), null],
            menu: [Nullable(Ref(Menu)), null],
        }));
    }
}
//# sourceMappingURL=action.js.map