import { Action, ActionView } from "./action";
import { RendererGroup } from "../renderers/renderer";
import { enumerate } from "../../core/util/iterator";
export class ToggleGroupView extends ActionView {
    static __name__ = "ToggleGroupView";
    update(_source, i, _vars /*, formatters?: Formatters*/) {
        for (const [group, j] of enumerate(this.model.groups)) {
            group.visible = i == j;
        }
    }
}
export class ToggleGroup extends Action {
    static __name__ = "ToggleGroup";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = ToggleGroupView;
        this.define(({ Array, Ref }) => ({
            groups: [Array(Ref(RendererGroup)), []],
        }));
    }
}
//# sourceMappingURL=toggle_group.js.map