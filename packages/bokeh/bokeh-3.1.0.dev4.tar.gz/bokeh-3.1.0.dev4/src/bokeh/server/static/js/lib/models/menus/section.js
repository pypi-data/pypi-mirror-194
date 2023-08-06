import { MenuItem, MenuItemView } from "./menu_item";
export class SectionView extends MenuItemView {
    static __name__ = "SectionView";
    render() {
        super.render();
    }
}
export class Section extends MenuItem {
    static __name__ = "Section";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = SectionView;
        this.define(({ Array, Ref }) => ({
            items: [Array(Ref(MenuItem)), []],
        }));
    }
}
//# sourceMappingURL=section.js.map