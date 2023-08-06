import { Control, ControlView } from "./control";
import inputs_css from "../../styles/widgets/inputs.css";
import checkbox_css from "../../styles/widgets/checkbox.css";
export class ToggleInputGroupView extends ControlView {
    static __name__ = "ToggleInputGroupView";
    _inputs;
    *controls() {
        yield* this._inputs;
    }
    connect_signals() {
        super.connect_signals();
        const { labels, inline } = this.model.properties;
        this.on_change([labels, inline], () => this.render());
    }
    styles() {
        return [...super.styles(), inputs_css, checkbox_css];
    }
}
export class ToggleInputGroup extends Control {
    static __name__ = "ToggleInputGroup";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ Boolean, String, Array }) => ({
            labels: [Array(String), []],
            inline: [Boolean, false],
        }));
    }
}
//# sourceMappingURL=toggle_input_group.js.map