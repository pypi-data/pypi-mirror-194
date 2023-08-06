export class BaseGLGlyph {
    glyph;
    static __name__ = "BaseGLGlyph";
    regl_wrapper;
    nvertices = 0;
    size_changed = false;
    data_changed = false;
    visuals_changed = false;
    constructor(regl_wrapper, glyph) {
        this.glyph = glyph;
        this.regl_wrapper = regl_wrapper;
    }
    set_data_changed() {
        const { data_size } = this.glyph;
        if (data_size != this.nvertices) {
            this.nvertices = data_size;
            this.size_changed = true;
        }
        this.data_changed = true;
    }
    set_visuals_changed() {
        this.visuals_changed = true;
    }
    render(_ctx, indices, mainglyph) {
        if (indices.length == 0) {
            return true;
        }
        const { width, height } = this.glyph.renderer.plot_view.canvas_view.webgl.canvas;
        const trans = {
            pixel_ratio: this.glyph.renderer.plot_view.canvas_view.pixel_ratio,
            width,
            height,
        };
        this.draw(indices, mainglyph, trans);
        return true;
    }
}
//# sourceMappingURL=base.js.map