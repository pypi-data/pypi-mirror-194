import { View } from "./view";
import { createElement, remove, empty, InlineStyleSheet, ClassList } from "./dom";
import { isString } from "./util/types";
import base_css from "../styles/base.css";
export class DOMView extends View {
    static __name__ = "DOMView";
    static tag_name = "div";
    el;
    shadow_el;
    get children_el() {
        return this.shadow_el ?? this.el;
    }
    initialize() {
        super.initialize();
        this.el = this._createElement();
    }
    remove() {
        remove(this.el);
        super.remove();
    }
    css_classes() {
        return [];
    }
    styles() {
        return [];
    }
    render_to(element) {
        element.appendChild(this.el);
        this.render();
    }
    finish() {
        this._has_finished = true;
        this.notify_finished();
    }
    _createElement() {
        return createElement(this.constructor.tag_name, { class: this.css_classes() });
    }
}
export class DOMElementView extends DOMView {
    static __name__ = "DOMElementView";
    class_list;
    initialize() {
        super.initialize();
        this.class_list = new ClassList(this.el.classList);
    }
}
export class DOMComponentView extends DOMElementView {
    static __name__ = "DOMComponentView";
    initialize() {
        super.initialize();
        this.shadow_el = this.el.attachShadow({ mode: "open" });
    }
    styles() {
        return [...super.styles(), base_css];
    }
    empty() {
        empty(this.shadow_el);
        this.class_list.clear();
    }
    render() {
        this.empty();
        this._apply_stylesheets(this.styles());
        this._apply_classes(this.css_classes());
    }
    _apply_stylesheets(stylesheets) {
        /*
        if (supports_adopted_stylesheets) {
          const sheets: CSSStyleSheet[] = []
          for (const style of this.styles()) {
            const sheet = new CSSStyleSheet()
            sheet.replaceSync(style)
            sheets.push(sheet)
          }
          this.shadow_el.adoptedStyleSheets = sheets
        } else {
        */
        for (const style of stylesheets) {
            const stylesheet = isString(style) ? new InlineStyleSheet(style) : style;
            stylesheet.install(this.shadow_el);
        }
    }
    _apply_classes(classes) {
        this.class_list.add(...classes);
    }
}
//# sourceMappingURL=dom_view.js.map