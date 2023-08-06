import { UIElement, UIElementView } from "../ui/ui_element";
import { MenuItem } from "./menu_item";
import { Orientation } from "../../core/enums";
import { build_views, remove_views } from "../../core/build_views";
import { reverse, map } from "../../core/util/iterator";
import menus_css, * as menus from "../../styles/menus.css";
export class MenuView extends UIElementView {
    static __name__ = "MenuView";
    styles() {
        return [...super.styles(), menus_css];
    }
    items = new Map();
    *children() {
        yield* super.children();
        yield* this.items.values();
    }
    async lazy_initialize() {
        await super.lazy_initialize();
        await build_views(this.items, this.model.items);
    }
    remove() {
        remove_views(this.items);
        super.remove();
    }
    render() {
        super.render();
        this.el.classList.add(menus[this.model.orientation]);
        const items = (() => {
            const { items, reversed } = this.model;
            const ordererd = reversed ? reverse(items) : items;
            return map(ordererd, (item) => this.items.get(item));
        })();
        for (const item of items) {
            item.render();
            this.shadow_el.appendChild(item.el);
        }
    }
}
export class Menu extends UIElement {
    static __name__ = "Menu";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ Boolean, Array, Ref }) => ({
            items: [Array(Ref(MenuItem)), []],
            reversed: [Boolean, false],
            orientation: [Orientation, "vertical"],
        }));
    }
}
//# sourceMappingURL=menu.js.map