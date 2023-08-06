import { Plot, PlotView } from "./plot";
export class FigureView extends PlotView {
    static __name__ = "FigureView";
    // TODO: remove this before bokeh 3.0 and update *.blf files
    serializable_state() {
        const state = super.serializable_state();
        return { ...state, type: "Plot" };
    }
}
export class Figure extends Plot {
    static __name__ = "Figure";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = FigureView;
    }
}
//# sourceMappingURL=figure.js.map