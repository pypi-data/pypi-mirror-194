import { Model } from "../../model";
import { Styles } from "../dom/styles";
import { StyleSheet as BaseStyleSheet } from "../dom/stylesheets";
import { logger } from "../../core/logging";
import { DOMComponentView } from "../../core/dom_view";
import { InlineStyleSheet } from "../../core/dom";
import { CanvasLayer } from "../../core/util/canvas";
import { keys, entries } from "../../core/util/object";
import { BBox } from "../../core/util/bbox";
import { isString } from "../../core/util/types";
import ui_css from "../../styles/ui.css";
const { round } = Math;
function* _iter_styles(styles) {
    if (styles instanceof Styles) {
        const model_attrs = new Set(keys(Model.prototype._props));
        for (const prop of styles) {
            if (!model_attrs.has(prop.attr)) {
                yield [prop.attr, prop.get_value()];
            }
        }
    }
    else
        yield* entries(styles);
}
export class UIElementView extends DOMComponentView {
    static __name__ = "UIElementView";
    _display = new InlineStyleSheet();
    style = new InlineStyleSheet();
    get stylesheets() {
        return [...this._stylesheets()];
    }
    *_stylesheets() {
        yield this.style;
        yield this._display;
    }
    get computed_stylesheets() {
        return [...this._computed_stylesheets()];
    }
    *_computed_stylesheets() {
        for (const stylesheet of this.model.stylesheets) {
            if (isString(stylesheet)) {
                yield new InlineStyleSheet(stylesheet);
            }
            else if (stylesheet instanceof BaseStyleSheet) {
                yield stylesheet.underlying();
            }
            else {
                const output = [];
                for (const [selector, styles] of entries(stylesheet)) {
                    output.push(`${selector} {`);
                    for (const [attr, value] of _iter_styles(styles)) {
                        const name = attr.replace(/_/g, "-");
                        if (isString(value) && value.length != 0) {
                            output.push(`  ${name}: ${value};`);
                        }
                    }
                    output.push("}");
                }
                const css = output.join("\n");
                yield new InlineStyleSheet(css);
            }
        }
    }
    get classes() {
        return [...this.css_classes(), ...this._classes()];
    }
    *_classes() {
        yield `bk-${this.model.type.replace(/\./g, "-")}`;
    }
    styles() {
        return [...super.styles(), ui_css];
    }
    update_style() {
        this.style.clear();
    }
    box_sizing() {
        return {
            width_policy: "auto", height_policy: "auto",
            width: null, height: null,
            aspect_ratio: null,
        };
    }
    _bbox;
    get bbox() {
        // XXX: this shouldn't be necessary
        if (this._bbox == null)
            this._update_bbox();
        return this._bbox;
    }
    update_bbox() {
        return this._update_bbox();
    }
    _update_bbox() {
        const displayed = this.el.offsetParent != null; // TODO: position == "sticky"
        const bbox = !displayed ? new BBox() : (() => {
            const self = this.el.getBoundingClientRect();
            const { left, top } = (() => {
                if (this.parent != null) {
                    const parent = this.parent.el.getBoundingClientRect();
                    return {
                        left: self.left - parent.left,
                        top: self.top - parent.top,
                    };
                }
                else {
                    return { left: 0, top: 0 };
                }
            })();
            return new BBox({
                left: round(left),
                top: round(top),
                width: round(self.width),
                height: round(self.height),
            });
        })();
        const changed = this._bbox == null || !this._bbox.equals(bbox);
        this._bbox = bbox;
        this._is_displayed = displayed;
        return changed;
    }
    _resize_observer;
    initialize() {
        super.initialize();
        this._resize_observer = new ResizeObserver((_entries) => this.after_resize());
        this._resize_observer.observe(this.el, { box: "border-box" });
    }
    connect_signals() {
        super.connect_signals();
        const { visible, styles } = this.model.properties;
        this.on_change(visible, () => this._apply_visible());
        this.on_change(styles, () => this._apply_styles());
    }
    remove() {
        this._resize_observer.disconnect();
        super.remove();
    }
    _after_resize() { }
    after_resize() {
        if (this.update_bbox()) {
            this._after_resize();
        }
        this.finish();
    }
    render_to(element) {
        super.render_to(element);
        this.after_render();
    }
    render() {
        this.empty();
        this._apply_stylesheets(this.styles());
        this._apply_stylesheets(this.stylesheets);
        this._apply_stylesheets(this.computed_stylesheets);
        this._apply_styles();
        this._apply_classes(this.classes);
        this._apply_classes(this.model.classes);
        this._apply_visible();
    }
    _after_render() { }
    after_render() {
        this.update_style();
        this.update_bbox();
        this._after_render();
        // If not displayed, then after_resize() will not be called.
        if (!this.is_displayed) {
            this.finish();
        }
    }
    _is_displayed = false;
    get is_displayed() {
        return this._is_displayed;
    }
    _apply_styles() {
        const { styles } = this.model;
        const apply = (name, value) => {
            const known = name in this.el.style; // XXX: hasOwnProperty() doesn't work for unknown reasons
            if (known && isString(value)) {
                this.el.style[name] = value; // XXX: setProperty() doesn't support camel-case
            }
            return known;
        };
        for (const [attr, value] of _iter_styles(styles)) {
            const name = attr.replace(/_/g, "-");
            if (!apply(name, value)) {
                if (!apply(`-webkit-${name}`, value) && !apply(`-moz-${name}`, value))
                    logger.trace(`unknown CSS property '${name}'`);
            }
        }
    }
    _apply_visible() {
        if (this.model.visible)
            this._display.clear();
        else {
            // in case `display` element style was set, use `!important` to work around this
            this._display.replace(":host { display: none !important; }");
        }
    }
    export(type = "auto", hidpi = true) {
        const output_backend = type == "auto" || type == "png" ? "canvas" : "svg";
        const canvas = new CanvasLayer(output_backend, hidpi);
        const { width, height } = this.bbox;
        canvas.resize(width, height);
        return canvas;
    }
    serializable_state() {
        return { ...super.serializable_state(), bbox: this.bbox };
    }
}
export class UIElement extends Model {
    static __name__ = "UIElement";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ Boolean, Array, Dict, String, Ref, Or, Nullable }) => {
            const StylesLike = Or(Dict(Nullable(String)), Ref(Styles)); // TODO: add validation for CSSStyles
            return {
                visible: [Boolean, true],
                classes: [Array(String), []],
                styles: [StylesLike, {}],
                stylesheets: [Array(Or(Ref(BaseStyleSheet), String, Dict(StylesLike))), []],
            };
        });
    }
}
//# sourceMappingURL=ui_element.js.map