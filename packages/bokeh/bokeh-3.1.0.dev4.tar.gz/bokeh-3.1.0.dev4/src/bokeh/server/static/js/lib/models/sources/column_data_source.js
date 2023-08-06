import { ColumnarDataSource } from "./columnar_data_source";
export class ColumnDataSource extends ColumnarDataSource {
    static __name__ = "ColumnDataSource";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ Any, Dict, Arrayable }) => ({
            data: [Dict(Arrayable(Any)), {}],
        }));
    }
    stream(new_data, rollover, { sync } = {}) {
        this.stream_to(this.properties.data, new_data, rollover, { sync });
    }
    patch(patches, { sync } = {}) {
        this.patch_to(this.properties.data, patches, { sync });
    }
}
//# sourceMappingURL=column_data_source.js.map