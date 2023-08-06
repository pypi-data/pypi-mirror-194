import { inplace } from "../../core/util/projections";
import * as p from "../../core/properties";
import { Glyph, GlyphView } from "./glyph";
export class XYGlyphView extends GlyphView {
    static __name__ = "XYGlyphView";
    _project_data() {
        inplace.project_xy(this._x, this._y);
    }
    _index_data(index) {
        const { _x, _y, data_size } = this;
        for (let i = 0; i < data_size; i++) {
            const x = _x[i];
            const y = _y[i];
            index.add_point(x, y);
        }
    }
    scenterxy(i) {
        return [this.sx[i], this.sy[i]];
    }
}
export class XYGlyph extends Glyph {
    static __name__ = "XYGlyph";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({}) => ({
            x: [p.XCoordinateSpec, { field: "x" }],
            y: [p.YCoordinateSpec, { field: "y" }],
        }));
    }
}
//# sourceMappingURL=xy_glyph.js.map