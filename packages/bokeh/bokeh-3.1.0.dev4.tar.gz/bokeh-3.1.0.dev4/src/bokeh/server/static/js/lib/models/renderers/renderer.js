import { View } from "../../core/view";
import * as visuals from "../../core/visuals";
import { RenderLevel } from "../../core/enums";
import { Model } from "../../model";
import { CoordinateTransform, CoordinateMapping } from "../coordinates/coordinate_mapping";
export class RendererGroup extends Model {
    static __name__ = "RendererGroup";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ Boolean }) => ({
            visible: [Boolean, true],
        }));
    }
}
export class RendererView extends View {
    static __name__ = "RendererView";
    visuals;
    needs_webgl_blit;
    _coordinates;
    get coordinates() {
        const { _coordinates } = this;
        if (_coordinates != null)
            return _coordinates;
        else
            return this._coordinates = this._initialize_coordinates();
    }
    initialize() {
        super.initialize();
        this.visuals = new visuals.Visuals(this);
        this.needs_webgl_blit = false;
    }
    connect_signals() {
        super.connect_signals();
        const { group } = this.model;
        if (group != null) {
            this.on_change(group.properties.visible, () => {
                this.model.visible = group.visible;
            });
        }
        const { x_range_name, y_range_name } = this.model.properties;
        this.on_change([x_range_name, y_range_name], () => delete this._coordinates);
        this.connect(this.plot_view.frame.change, () => delete this._coordinates);
    }
    _initialize_coordinates() {
        const { coordinates } = this.model;
        const { frame } = this.plot_view;
        if (coordinates != null) {
            return coordinates.get_transform(frame);
        }
        else {
            const { x_range_name, y_range_name } = this.model;
            const x_scale = frame.x_scales.get(x_range_name);
            const y_scale = frame.y_scales.get(y_range_name);
            return new CoordinateTransform(x_scale, y_scale);
        }
    }
    get plot_view() {
        return this.parent;
    }
    get plot_model() {
        return this.parent.model;
    }
    get layer() {
        const { overlays, primary } = this.canvas;
        return this.model.level == "overlay" ? overlays : primary;
    }
    get canvas() {
        return this.plot_view.canvas_view;
    }
    request_render() {
        this.request_paint();
    }
    request_paint() {
        this.plot_view.request_paint(this);
    }
    request_layout() {
        this.plot_view.request_layout();
    }
    notify_finished() {
        this.plot_view.notify_finished();
    }
    notify_finished_after_paint() {
        this.plot_view.notify_finished_after_paint();
    }
    get needs_clip() {
        return false;
    }
    get has_webgl() {
        return false;
    }
    /*
    get visible(): boolean {
      const {visible, group} = this.model
      return !visible ? false : (group?.visible ?? true)
    }
    */
    get displayed() {
        return this.model.visible;
    }
    render() {
        if (this.displayed) {
            this._render();
        }
        this._has_finished = true;
    }
    renderer_view(_renderer) {
        return undefined;
    }
    /**
     * Geometry setup that doesn't change between paints.
     */
    update_geometry() { }
    /**
     * Geometry setup that changes between paints.
     */
    compute_geometry() { }
}
export class Renderer extends Model {
    static __name__ = "Renderer";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ Boolean, String, Ref, Nullable }) => ({
            group: [Nullable(Ref(RendererGroup)), null],
            level: [RenderLevel, "image"],
            visible: [Boolean, true],
            x_range_name: [String, "default"],
            y_range_name: [String, "default"],
            coordinates: [Nullable(Ref(CoordinateMapping)), null],
            propagate_hover: [Boolean, false],
        }));
    }
}
//# sourceMappingURL=renderer.js.map