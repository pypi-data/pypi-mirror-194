var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
import { serialize } from "./serialization";
import { equals } from "./util/eq";
function event(event_name) {
    return (cls) => {
        cls.prototype.event_name = event_name;
        cls.prototype.publish = true;
    };
}
export class BokehEvent {
    static __name__ = "BokehEvent";
    [serialize](serializer) {
        const { event_name: name, event_values } = this;
        const values = serializer.encode(event_values);
        return { type: "event", name, values };
    }
    [equals](that, cmp) {
        return this.event_name == that.event_name && cmp.eq(this.event_values, that.event_values);
    }
}
export class ModelEvent extends BokehEvent {
    static __name__ = "ModelEvent";
    origin = null;
    get event_values() {
        return { model: this.origin };
    }
}
export class DocumentEvent extends BokehEvent {
    static __name__ = "DocumentEvent";
}
let DocumentReady = class DocumentReady extends DocumentEvent {
    static __name__ = "DocumentReady";
    get event_values() {
        return {};
    }
};
DocumentReady = __decorate([
    event("document_ready")
], DocumentReady);
export { DocumentReady };
export class ConnectionEvent extends DocumentEvent {
    static __name__ = "ConnectionEvent";
}
export class ConnectionLost extends ConnectionEvent {
    static __name__ = "ConnectionLost";
    timestamp = new Date();
    get event_values() {
        const { timestamp } = this;
        return { timestamp };
    }
    static {
        this.prototype.event_name = "connection_lost";
        this.prototype.publish = false;
    }
}
let ButtonClick = class ButtonClick extends ModelEvent {
    static __name__ = "ButtonClick";
};
ButtonClick = __decorate([
    event("button_click")
], ButtonClick);
export { ButtonClick };
let MenuItemClick = class MenuItemClick extends ModelEvent {
    item;
    static __name__ = "MenuItemClick";
    constructor(item) {
        super();
        this.item = item;
    }
    get event_values() {
        const { item } = this;
        return { ...super.event_values, item };
    }
};
MenuItemClick = __decorate([
    event("menu_item_click")
], MenuItemClick);
export { MenuItemClick };
let ValueSubmit = class ValueSubmit extends ModelEvent {
    value;
    static __name__ = "ValueSubmit";
    constructor(value) {
        super();
        this.value = value;
    }
    get event_values() {
        const { value } = this;
        return { ...super.event_values, value };
    }
};
ValueSubmit = __decorate([
    event("value_submit")
], ValueSubmit);
export { ValueSubmit };
// A UIEvent is an event originating on a canvas this includes.
// DOM events such as keystrokes as well as hammer, LOD, and range events.
export class UIEvent extends ModelEvent {
    static __name__ = "UIEvent";
}
let LODStart = class LODStart extends UIEvent {
    static __name__ = "LODStart";
};
LODStart = __decorate([
    event("lodstart")
], LODStart);
export { LODStart };
let LODEnd = class LODEnd extends UIEvent {
    static __name__ = "LODEnd";
};
LODEnd = __decorate([
    event("lodend")
], LODEnd);
export { LODEnd };
let RangesUpdate = class RangesUpdate extends UIEvent {
    x0;
    x1;
    y0;
    y1;
    static __name__ = "RangesUpdate";
    constructor(x0, x1, y0, y1) {
        super();
        this.x0 = x0;
        this.x1 = x1;
        this.y0 = y0;
        this.y1 = y1;
    }
    get event_values() {
        const { x0, x1, y0, y1 } = this;
        return { ...super.event_values, x0, x1, y0, y1 };
    }
};
RangesUpdate = __decorate([
    event("rangesupdate")
], RangesUpdate);
export { RangesUpdate };
let SelectionGeometry = class SelectionGeometry extends UIEvent {
    geometry;
    final;
    static __name__ = "SelectionGeometry";
    constructor(geometry, final) {
        super();
        this.geometry = geometry;
        this.final = final;
    }
    get event_values() {
        const { geometry, final } = this;
        return { ...super.event_values, geometry, final };
    }
};
SelectionGeometry = __decorate([
    event("selectiongeometry")
], SelectionGeometry);
export { SelectionGeometry };
let Reset = class Reset extends UIEvent {
    static __name__ = "Reset";
};
Reset = __decorate([
    event("reset")
], Reset);
export { Reset };
export class PointEvent extends UIEvent {
    sx;
    sy;
    x;
    y;
    static __name__ = "PointEvent";
    constructor(sx, sy, x, y) {
        super();
        this.sx = sx;
        this.sy = sy;
        this.x = x;
        this.y = y;
    }
    get event_values() {
        const { sx, sy, x, y } = this;
        return { ...super.event_values, sx, sy, x, y };
    }
}
let Pan = class Pan extends PointEvent {
    delta_x;
    delta_y;
    static __name__ = "Pan";
    /* TODO: direction: -1 | 1 */
    constructor(sx, sy, x, y, delta_x, delta_y) {
        super(sx, sy, x, y);
        this.delta_x = delta_x;
        this.delta_y = delta_y;
    }
    get event_values() {
        const { delta_x, delta_y /*, direction*/ } = this;
        return { ...super.event_values, delta_x, delta_y /*, direction*/ };
    }
};
Pan = __decorate([
    event("pan")
], Pan);
export { Pan };
let Pinch = class Pinch extends PointEvent {
    scale;
    static __name__ = "Pinch";
    constructor(sx, sy, x, y, scale) {
        super(sx, sy, x, y);
        this.scale = scale;
    }
    get event_values() {
        const { scale } = this;
        return { ...super.event_values, scale };
    }
};
Pinch = __decorate([
    event("pinch")
], Pinch);
export { Pinch };
let Rotate = class Rotate extends PointEvent {
    rotation;
    static __name__ = "Rotate";
    constructor(sx, sy, x, y, rotation) {
        super(sx, sy, x, y);
        this.rotation = rotation;
    }
    get event_values() {
        const { rotation } = this;
        return { ...super.event_values, rotation };
    }
};
Rotate = __decorate([
    event("rotate")
], Rotate);
export { Rotate };
let MouseWheel = class MouseWheel extends PointEvent {
    delta;
    static __name__ = "MouseWheel";
    constructor(sx, sy, x, y, delta) {
        super(sx, sy, x, y);
        this.delta = delta;
    }
    get event_values() {
        const { delta } = this;
        return { ...super.event_values, delta };
    }
};
MouseWheel = __decorate([
    event("wheel")
], MouseWheel);
export { MouseWheel };
let MouseMove = class MouseMove extends PointEvent {
    static __name__ = "MouseMove";
};
MouseMove = __decorate([
    event("mousemove")
], MouseMove);
export { MouseMove };
let MouseEnter = class MouseEnter extends PointEvent {
    static __name__ = "MouseEnter";
};
MouseEnter = __decorate([
    event("mouseenter")
], MouseEnter);
export { MouseEnter };
let MouseLeave = class MouseLeave extends PointEvent {
    static __name__ = "MouseLeave";
};
MouseLeave = __decorate([
    event("mouseleave")
], MouseLeave);
export { MouseLeave };
let Tap = class Tap extends PointEvent {
    static __name__ = "Tap";
};
Tap = __decorate([
    event("tap")
], Tap);
export { Tap };
let DoubleTap = class DoubleTap extends PointEvent {
    static __name__ = "DoubleTap";
};
DoubleTap = __decorate([
    event("doubletap")
], DoubleTap);
export { DoubleTap };
let Press = class Press extends PointEvent {
    static __name__ = "Press";
};
Press = __decorate([
    event("press")
], Press);
export { Press };
let PressUp = class PressUp extends PointEvent {
    static __name__ = "PressUp";
};
PressUp = __decorate([
    event("pressup")
], PressUp);
export { PressUp };
let PanStart = class PanStart extends PointEvent {
    static __name__ = "PanStart";
};
PanStart = __decorate([
    event("panstart")
], PanStart);
export { PanStart };
let PanEnd = class PanEnd extends PointEvent {
    static __name__ = "PanEnd";
};
PanEnd = __decorate([
    event("panend")
], PanEnd);
export { PanEnd };
let PinchStart = class PinchStart extends PointEvent {
    static __name__ = "PinchStart";
};
PinchStart = __decorate([
    event("pinchstart")
], PinchStart);
export { PinchStart };
let PinchEnd = class PinchEnd extends PointEvent {
    static __name__ = "PinchEnd";
};
PinchEnd = __decorate([
    event("pinchend")
], PinchEnd);
export { PinchEnd };
let RotateStart = class RotateStart extends PointEvent {
    static __name__ = "RotateStart";
};
RotateStart = __decorate([
    event("rotatestart")
], RotateStart);
export { RotateStart };
let RotateEnd = class RotateEnd extends PointEvent {
    static __name__ = "RotateEnd";
};
RotateEnd = __decorate([
    event("rotateend")
], RotateEnd);
export { RotateEnd };
//# sourceMappingURL=bokeh_events.js.map