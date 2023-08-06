import { Plot } from "./plot";
import { MapType } from "../../core/enums";
import { Model } from "../../model";
import { Range1d } from "../ranges/range1d";
import { GMapPlotView } from "./gmap_plot_canvas";
export { GMapPlotView };
export class MapOptions extends Model {
    static __name__ = "MapOptions";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ Int, Number }) => ({
            lat: [Number],
            lng: [Number],
            zoom: [Int, 12],
        }));
    }
}
export class GMapOptions extends MapOptions {
    static __name__ = "GMapOptions";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ Boolean, Int, String, Nullable }) => ({
            map_type: [MapType, "roadmap"],
            scale_control: [Boolean, false],
            styles: [Nullable(String), null],
            tilt: [Int, 45],
        }));
    }
}
export class GMapPlot extends Plot {
    static __name__ = "GMapPlot";
    use_map = true;
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = GMapPlotView;
        this.define(({ String, Bytes, Ref }) => ({
            map_options: [Ref(GMapOptions)],
            api_key: [Bytes],
            api_version: [String, "weekly"],
        }));
        this.override({
            x_range: () => new Range1d(),
            y_range: () => new Range1d(),
            background_fill_alpha: 0.0,
        });
    }
}
//# sourceMappingURL=gmap_plot.js.map