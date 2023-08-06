import { isArray } from "../../../core/util/types";
import { EditTool, EditToolView } from "./edit_tool";
export class LineToolView extends EditToolView {
    static __name__ = "LineToolView";
    _set_intersection(x, y) {
        const point_glyph = this.model.intersection_renderer.glyph;
        const point_cds = this.model.intersection_renderer.data_source;
        const [pxkey, pykey] = [point_glyph.x.field, point_glyph.y.field];
        if (pxkey) {
            if (isArray(x))
                point_cds.data[pxkey] = x;
            else
                point_glyph.x = { value: x };
        }
        if (pykey) {
            if (isArray(y))
                point_cds.data[pykey] = y;
            else
                point_glyph.y = { value: y };
        }
        this._emit_cds_changes(point_cds, true, true, false);
    }
    _hide_intersections() {
        this._set_intersection([], []);
    }
}
export class LineTool extends EditTool {
    static __name__ = "LineTool";
    renderers;
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ AnyRef }) => ({
            intersection_renderer: [AnyRef()],
        }));
    }
}
//# sourceMappingURL=line_tool.js.map