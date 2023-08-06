import { CSSGridBox, CSSGridBoxView, TracksSizing } from "./css_grid_box";
import { UIElement } from "../ui/ui_element";
export class VBoxView extends CSSGridBoxView {
    static __name__ = "VBoxView";
    connect_signals() {
        super.connect_signals();
        const { children, rows } = this.model.properties;
        this.on_change(children, () => this.update_children());
        this.on_change(rows, () => this.invalidate_layout());
    }
    get _children() {
        return this.model.children.map(({ child, row, span }, i) => [child, row ?? i, 0, span ?? 1, 1]);
    }
    get _rows() {
        return this.model.rows;
    }
    get _cols() {
        return null;
    }
}
export class VBox extends CSSGridBox {
    static __name__ = "VBox";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = VBoxView;
        this.define(({ Int, Struct, Array, Ref, Opt, Nullable }) => ({
            children: [Array(Struct({ child: Ref(UIElement), row: Opt(Int), span: Opt(Int) })), []],
            rows: [Nullable(TracksSizing), null],
        }));
    }
}
//# sourceMappingURL=vbox.js.map