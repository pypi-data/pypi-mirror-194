import { Renderer, RendererView } from "../renderers/renderer";
export class AnnotationView extends RendererView {
    static __name__ = "AnnotationView";
    layout;
    panel;
    bbox;
    get_size() {
        if (this.displayed) {
            const { width, height } = this._get_size();
            return { width: Math.round(width), height: Math.round(height) };
        }
        else
            return { width: 0, height: 0 };
    }
    _get_size() {
        throw new Error("not implemented");
    }
    connect_signals() {
        super.connect_signals();
        const p = this.model.properties;
        this.on_change(p.visible, () => {
            if (this.layout != null) {
                this.layout.visible = this.model.visible;
                this.plot_view.request_layout();
            }
        });
    }
    get needs_clip() {
        return this.layout == null; // TODO: change this, when center layout is fully implemented
    }
    serializable_state() {
        const state = super.serializable_state();
        const bbox = this.bbox?.round() ?? this.layout?.bbox;
        return bbox == null ? state : { ...state, bbox };
    }
}
export class Annotation extends Renderer {
    static __name__ = "Annotation";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.override({
            level: "annotation",
        });
    }
}
//# sourceMappingURL=annotation.js.map