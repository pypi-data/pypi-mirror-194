import { ImageBase, ImageBaseView } from "./image_base";
import { StackColorMapper } from "../mappers/stack_color_mapper";
export class ImageStackView extends ImageBaseView {
    static __name__ = "ImageStackView";
    connect_signals() {
        super.connect_signals();
        this.connect(this.model.color_mapper.change, () => this._update_image());
    }
    get image_dimension() {
        return 3;
    }
    _update_image() {
        // Only reset image_data if already initialized
        if (this.image_data != null) {
            this._set_data(null);
            this.renderer.request_render();
        }
    }
    _flat_img_to_buf8(img) {
        const cmap = this.model.color_mapper.rgba_mapper;
        return cmap.v_compute(img);
    }
}
export class ImageStack extends ImageBase {
    static __name__ = "ImageStack";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = ImageStackView;
        this.define(({ Ref }) => ({
            color_mapper: [Ref(StackColorMapper)],
        }));
    }
}
//# sourceMappingURL=image_stack.js.map