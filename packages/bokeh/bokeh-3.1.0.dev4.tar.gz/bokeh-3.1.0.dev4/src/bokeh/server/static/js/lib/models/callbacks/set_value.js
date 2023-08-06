import { Callback } from "./callback";
import { HasProps } from "../../core/has_props";
import { logger } from "../../core/logging";
export class SetValue extends Callback {
    static __name__ = "SetValue";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ String, Unknown, Ref }) => ({
            obj: [Ref(HasProps)],
            attr: [String],
            value: [Unknown],
        }));
    }
    execute() {
        const { obj, attr, value } = this;
        if (attr in obj.properties)
            obj.setv({ [attr]: value });
        else
            logger.error(`${obj.type}.${attr} is not a property`);
    }
}
//# sourceMappingURL=set_value.js.map