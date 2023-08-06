import { Annotation, AnnotationView } from "./annotation";
import { auto_ranged } from "../ranges/data_range1d";
import * as mixins from "../../core/property_mixins";
import { CoordinateUnits } from "../../core/enums";
import { BBox, empty } from "../../core/util/bbox";
import { Enum } from "../../core/kinds";
import { Signal } from "../../core/signaling";
import { assert } from "../../core/util/assert";
import { BorderRadius } from "../common/kinds";
import { round_rect } from "../common/painting";
import * as resolve from "../common/resolve";
export const EDGE_TOLERANCE = 2.5;
const { abs } = Math;
const Resizable = Enum("none", "left", "right", "top", "bottom", "x", "y", "all");
const Movable = Enum("none", "x", "y", "both");
export class BoxAnnotationView extends AnnotationView {
    static __name__ = "BoxAnnotationView";
    bbox = new BBox();
    serializable_state() {
        return { ...super.serializable_state(), bbox: this.bbox.round() }; // TODO: probably round ealier
    }
    connect_signals() {
        super.connect_signals();
        this.connect(this.model.change, () => this.request_render());
    }
    [auto_ranged] = true;
    bounds() {
        const { left, left_units, right, right_units, top, top_units, bottom, bottom_units, } = this.model;
        const left_ok = left_units == "data" && left != null;
        const right_ok = right_units == "data" && right != null;
        const top_ok = top_units == "data" && top != null;
        const bottom_ok = bottom_units == "data" && bottom != null;
        const [x0, x1] = (() => {
            if (left_ok && right_ok)
                return left <= right ? [left, right] : [right, left];
            else if (left_ok)
                return [left, left];
            else if (right_ok)
                return [right, right];
            else
                return [NaN, NaN];
        })();
        const [y0, y1] = (() => {
            if (top_ok && bottom_ok)
                return top <= bottom ? [top, bottom] : [bottom, top];
            else if (top_ok)
                return [top, top];
            else if (bottom_ok)
                return [bottom, bottom];
            else
                return [NaN, NaN];
        })();
        return { x0, x1, y0, y1 };
    }
    log_bounds() {
        return empty();
    }
    get mappers() {
        function mapper(units, scale, view, canvas) {
            switch (units) {
                case "canvas": return canvas;
                case "screen": return view;
                case "data": return scale;
            }
        }
        const overlay = this.model;
        const { x_scale, y_scale } = this.coordinates;
        const { x_view, y_view } = this.plot_view.frame.bbox;
        const { x_screen, y_screen } = this.plot_view.canvas.bbox;
        const lrtb = {
            left: mapper(overlay.left_units, x_scale, x_view, x_screen),
            right: mapper(overlay.right_units, x_scale, x_view, x_screen),
            top: mapper(overlay.top_units, y_scale, y_view, y_screen),
            bottom: mapper(overlay.bottom_units, y_scale, y_view, y_screen),
        };
        return lrtb;
    }
    _render() {
        function compute(value, mapper, frame_extrema) {
            return value == null ? frame_extrema : mapper.compute(value);
        }
        const { left, right, top, bottom } = this.model;
        const { frame } = this.plot_view;
        const { mappers } = this;
        this.bbox = BBox.from_lrtb({
            left: compute(left, mappers.left, frame.bbox.left),
            right: compute(right, mappers.right, frame.bbox.right),
            top: compute(top, mappers.top, frame.bbox.top),
            bottom: compute(bottom, mappers.bottom, frame.bbox.bottom),
        });
        if (this.bbox.is_valid) {
            this._paint_box();
        }
    }
    get border_radius() {
        return resolve.border_radius(this.model.border_radius);
    }
    _paint_box() {
        const { ctx } = this.layer;
        ctx.save();
        ctx.beginPath();
        round_rect(ctx, this.bbox, this.border_radius);
        const { _is_hovered, visuals } = this;
        const fill = _is_hovered && visuals.hover_fill.doit ? visuals.hover_fill : visuals.fill;
        const hatch = _is_hovered && visuals.hover_hatch.doit ? visuals.hover_hatch : visuals.hatch;
        const line = _is_hovered && visuals.hover_line.doit ? visuals.hover_line : visuals.line;
        fill.apply(ctx);
        hatch.apply(ctx);
        line.apply(ctx);
        ctx.restore();
    }
    interactive_bbox() {
        const tolerance = this.model.line_width + EDGE_TOLERANCE;
        return this.bbox.grow_by(tolerance);
    }
    interactive_hit(sx, sy) {
        if (!this.model.visible || !this.model.editable)
            return false;
        const bbox = this.interactive_bbox();
        return bbox.contains(sx, sy);
    }
    _hit_test(sx, sy) {
        const { left, right, bottom, top } = this.bbox;
        const tolerance = Math.max(EDGE_TOLERANCE, this.model.line_width / 2);
        const dl = abs(left - sx);
        const dr = abs(right - sx);
        const dt = abs(top - sy);
        const db = abs(bottom - sy);
        const hits_left = dl < tolerance && dl < dr;
        const hits_right = dr < tolerance && dr < dl;
        const hits_top = dt < tolerance && dt < db;
        const hits_bottom = db < tolerance && db < dt;
        if (hits_top && hits_left)
            return "top_left";
        if (hits_top && hits_right)
            return "top_right";
        if (hits_bottom && hits_left)
            return "bottom_left";
        if (hits_bottom && hits_right)
            return "bottom_right";
        if (hits_left)
            return "left";
        if (hits_right)
            return "right";
        if (hits_top)
            return "top";
        if (hits_bottom)
            return "bottom";
        if (this.bbox.contains(sx, sy))
            return "area";
        return null;
    }
    get resizable() {
        const { resizable } = this.model;
        return {
            left: resizable == "left" || resizable == "x" || resizable == "all",
            right: resizable == "right" || resizable == "x" || resizable == "all",
            top: resizable == "top" || resizable == "y" || resizable == "all",
            bottom: resizable == "bottom" || resizable == "y" || resizable == "all",
        };
    }
    _can_hit(target) {
        const { left, right, top, bottom } = this.resizable;
        switch (target) {
            case "top_left": return top && left;
            case "top_right": return top && right;
            case "bottom_left": return bottom && left;
            case "bottom_right": return bottom && right;
            case "left": return left;
            case "right": return right;
            case "top": return top;
            case "bottom": return bottom;
            case "area": return this.model.movable != "none";
        }
    }
    _pan_state = null;
    _pan_start(ev) {
        if (this.model.visible && this.model.editable) {
            const { sx, sy } = ev;
            const target = this._hit_test(sx, sy);
            if (target != null && this._can_hit(target)) {
                this._pan_state = {
                    bbox: this.bbox.clone(),
                    target,
                };
                this.model.pan.emit(["pan:start", ev]);
                return true;
            }
        }
        return false;
    }
    _pan(ev) {
        assert(this._pan_state != null);
        const sltrb = (() => {
            const { dx, dy } = ev;
            const { bbox, target } = this._pan_state;
            const { left, top, right, bottom } = bbox;
            const { symmetric } = this.model;
            const [Dx, Dy] = symmetric ? [-dx, -dy] : [0, 0];
            const [dl, dr, dt, db] = (() => {
                switch (target) {
                    case "top_left":
                        return [dx, Dx, dy, Dy];
                    case "top_right":
                        return [Dx, dx, dy, Dy];
                    case "bottom_left":
                        return [dx, Dx, Dy, dy];
                    case "bottom_right":
                        return [Dx, dx, Dy, dy];
                    case "left":
                        return [dx, Dx, 0, 0];
                    case "right":
                        return [Dx, dx, 0, 0];
                    case "top":
                        return [0, 0, dy, Dy];
                    case "bottom":
                        return [0, 0, Dy, dy];
                    case "area": {
                        switch (this.model.movable) {
                            case "both": return [dx, dx, dy, dy];
                            case "x": return [dx, dx, 0, 0];
                            case "y": return [0, 0, dy, dy];
                            case "none": return [0, 0, 0, 0];
                        }
                    }
                }
            })();
            return BBox.from_lrtb({
                left: left + dl,
                right: right + dr,
                top: top + dt,
                bottom: bottom + db,
            });
        })();
        const { mappers } = this;
        const ltrb = {
            left: mappers.left.invert(sltrb.left),
            right: mappers.right.invert(sltrb.right),
            top: mappers.top.invert(sltrb.top),
            bottom: mappers.bottom.invert(sltrb.bottom),
        };
        this.model.update(ltrb);
        this.model.pan.emit(["pan", ev]);
    }
    _pan_end(ev) {
        this._pan_state = null;
        this.model.pan.emit(["pan:end", ev]);
    }
    _pinch_state = null;
    _pinch_start(ev) {
        if (this.model.visible && this.model.editable && this.model.resizable != "none") {
            const { sx, sy } = ev;
            if (this.bbox.contains(sx, sy)) {
                this._pinch_state = {
                    bbox: this.bbox.clone(),
                };
                this.model.pan.emit(["pan:start", ev]); // TODO: pinch signal
                return true;
            }
        }
        return false;
    }
    _pinch(ev) {
        assert(this._pinch_state != null);
        const sltrb = (() => {
            const { scale } = ev;
            const { bbox } = this._pinch_state;
            const { left, top, right, bottom, width, height } = bbox;
            const dw = width * (scale - 1);
            const dh = height * (scale - 1);
            const { resizable } = this;
            const dl = resizable.left ? -dw / 2 : 0;
            const dr = resizable.right ? dw / 2 : 0;
            const dt = resizable.top ? -dh / 2 : 0;
            const db = resizable.bottom ? dh / 2 : 0;
            return BBox.from_lrtb({
                left: left + dl,
                right: right + dr,
                top: top + dt,
                bottom: bottom + db,
            });
        })();
        const { mappers } = this;
        const ltrb = {
            left: mappers.left.invert(sltrb.left),
            right: mappers.right.invert(sltrb.right),
            top: mappers.top.invert(sltrb.top),
            bottom: mappers.bottom.invert(sltrb.bottom),
        };
        this.model.update(ltrb);
        this.model.pan.emit(["pan", ev]);
    }
    _pinch_end(ev) {
        this._pinch_state = null;
        this.model.pan.emit(["pan:end", ev]);
    }
    get _has_hover() {
        const { hover_line, hover_fill, hover_hatch } = this.visuals;
        return hover_line.doit || hover_fill.doit || hover_hatch.doit;
    }
    _is_hovered = false;
    _move_start(_ev) {
        const { _has_hover } = this;
        if (_has_hover) {
            this._is_hovered = true;
            this.request_paint();
        }
        return _has_hover;
    }
    _move(_ev) { }
    _move_end(_ev) {
        if (this._has_hover) {
            this._is_hovered = false;
            this.request_paint();
        }
    }
    cursor(sx, sy) {
        const target = this._pan_state?.target ?? this._hit_test(sx, sy);
        if (target == null || !this._can_hit(target)) {
            return null;
        }
        switch (target) {
            case "top_left": return this.model.tl_cursor;
            case "top_right": return this.model.tr_cursor;
            case "bottom_left": return this.model.bl_cursor;
            case "bottom_right": return this.model.br_cursor;
            case "left":
            case "right": return this.model.ew_cursor;
            case "top":
            case "bottom": return this.model.ns_cursor;
            case "area": {
                switch (this.model.movable) {
                    case "both": return this.model.in_cursor;
                    case "x": return this.model.ew_cursor;
                    case "y": return this.model.ns_cursor;
                    case "none": return null;
                }
            }
        }
    }
}
export class BoxAnnotation extends Annotation {
    static __name__ = "BoxAnnotation";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = BoxAnnotationView;
        this.mixins([
            mixins.Line,
            mixins.Fill,
            mixins.Hatch,
            ["hover_", mixins.Line],
            ["hover_", mixins.Fill],
            ["hover_", mixins.Hatch],
        ]);
        this.define(({ Boolean, Number, Nullable }) => ({
            top: [Nullable(Number), null],
            bottom: [Nullable(Number), null],
            left: [Nullable(Number), null],
            right: [Nullable(Number), null],
            top_units: [CoordinateUnits, "data"],
            bottom_units: [CoordinateUnits, "data"],
            left_units: [CoordinateUnits, "data"],
            right_units: [CoordinateUnits, "data"],
            border_radius: [BorderRadius, 0],
            editable: [Boolean, false],
            resizable: [Resizable, "all"],
            movable: [Movable, "both"],
            symmetric: [Boolean, false],
        }));
        this.internal(({ String }) => ({
            tl_cursor: [String, "nwse-resize"],
            tr_cursor: [String, "nesw-resize"],
            bl_cursor: [String, "nesw-resize"],
            br_cursor: [String, "nwse-resize"],
            ew_cursor: [String, "ew-resize"],
            ns_cursor: [String, "ns-resize"],
            in_cursor: [String, "move"],
        }));
        this.override({
            fill_color: "#fff9ba",
            fill_alpha: 0.4,
            line_color: "#cccccc",
            line_alpha: 0.3,
            hover_fill_color: null,
            hover_fill_alpha: 0.4,
            hover_line_color: null,
            hover_line_alpha: 0.3,
        });
    }
    pan = new Signal(this, "pan");
    update({ left, right, top, bottom }) {
        this.setv({ left, right, top, bottom, visible: true });
    }
    clear() {
        this.visible = false;
    }
}
//# sourceMappingURL=box_annotation.js.map