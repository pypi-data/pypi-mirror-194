import { isArray } from "../../../core/util/types";
import { assert } from "../../../core/util/assert";
import { EditTool, EditToolView } from "./edit_tool";
export class PolyToolView extends EditToolView {
    static __name__ = "PolyToolView";
    _set_vertices(xs, ys) {
        const { vertex_renderer } = this.model;
        assert(vertex_renderer != null);
        const point_glyph = vertex_renderer.glyph;
        const point_cds = vertex_renderer.data_source;
        const [pxkey, pykey] = [point_glyph.x.field, point_glyph.y.field];
        if (pxkey) {
            if (isArray(xs))
                point_cds.data[pxkey] = xs;
            else
                point_glyph.x = { value: xs };
        }
        if (pykey) {
            if (isArray(ys))
                point_cds.data[pykey] = ys;
            else
                point_glyph.y = { value: ys };
        }
        this._emit_cds_changes(point_cds, true, true, false);
    }
    _hide_vertices() {
        this._set_vertices([], []);
    }
    _snap_to_vertex(ev, x, y) {
        if (this.model.vertex_renderer != null) {
            // If an existing vertex is hit snap to it
            const vertex_selected = this._select_event(ev, "replace", [this.model.vertex_renderer]);
            const point_ds = this.model.vertex_renderer.data_source;
            // Type once dataspecs are typed
            const point_glyph = this.model.vertex_renderer.glyph;
            const [pxkey, pykey] = [point_glyph.x.field, point_glyph.y.field];
            if (vertex_selected.length != 0) {
                const index = point_ds.selected.indices[0];
                if (pxkey)
                    x = point_ds.data[pxkey][index];
                if (pykey)
                    y = point_ds.data[pykey][index];
                point_ds.selection_manager.clear();
            }
        }
        return [x, y];
    }
}
export class PolyTool extends EditTool {
    static __name__ = "PolyTool";
    renderers;
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ AnyRef, Nullable }) => ({
            vertex_renderer: [Nullable(AnyRef()), null],
        }));
    }
}
//# sourceMappingURL=poly_tool.js.map