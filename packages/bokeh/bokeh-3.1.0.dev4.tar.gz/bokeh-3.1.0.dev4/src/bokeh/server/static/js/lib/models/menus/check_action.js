import { Action, ActionView } from "./action";
export class CheckActionView extends ActionView {
    static __name__ = "CheckActionView";
}
export class CheckAction extends Action {
    static __name__ = "CheckAction";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = CheckActionView;
        this.define(({ Boolean }) => ({
            checked: [Boolean, false],
        }));
    }
}
//# sourceMappingURL=check_action.js.map