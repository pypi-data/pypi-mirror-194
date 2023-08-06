import { GMapPlot, GMapPlotView } from "./gmap_plot";
export class GMapView extends GMapPlotView {
    static __name__ = "GMapView";
    // TODO: remove this before bokeh 3.0 and update *.blf files
    serializable_state() {
        const state = super.serializable_state();
        return { ...state, type: "GMapPlot" };
    }
}
export class GMap extends GMapPlot {
    static __name__ = "GMap";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = GMapView;
    }
}
//# sourceMappingURL=gmap.js.map