import { DataRenderer, DataRendererView } from "./data_renderer";
import { GlyphRenderer } from "./glyph_renderer";
import { LayoutProvider } from "../graphs/layout_provider";
import { GraphHitTestPolicy, NodesOnly } from "../graphs/graph_hit_test_policy";
import { build_view } from "../../core/build_views";
import { XYGlyph } from "../glyphs/xy_glyph";
import { MultiLine } from "../glyphs/multi_line";
import { Patches } from "../glyphs/patches";
export class GraphRendererView extends DataRendererView {
    static __name__ = "GraphRendererView";
    edge_view;
    node_view;
    get glyph_view() {
        return this.node_view.glyph;
    }
    *children() {
        yield* super.children();
        yield this.edge_view;
        yield this.node_view;
    }
    async lazy_initialize() {
        await super.lazy_initialize();
        this.apply_coordinates();
        const { parent } = this;
        const { edge_renderer, node_renderer } = this.model;
        this.edge_view = await build_view(edge_renderer, { parent });
        this.node_view = await build_view(node_renderer, { parent });
    }
    connect_signals() {
        super.connect_signals();
        this.connect(this.model.layout_provider.change, () => {
            this.apply_coordinates();
            this.edge_view.set_data();
            this.node_view.set_data();
            this.request_render();
        });
    }
    apply_coordinates() {
        const { edge_renderer, node_renderer } = this.model;
        // TODO: XsYsGlyph or something
        if (!(edge_renderer.glyph instanceof MultiLine || edge_renderer.glyph instanceof Patches)) {
            throw new Error(`${this}.edge_renderer.glyph must be a MultiLine glyph`);
        }
        if (!(node_renderer.glyph instanceof XYGlyph)) {
            throw new Error(`${this}.node_renderer.glyph must be a XYGlyph glyph`);
        }
        const edge_coords = this.model.layout_provider.edge_coordinates;
        const node_coords = this.model.layout_provider.node_coordinates;
        edge_renderer.glyph.properties.xs.internal = true;
        edge_renderer.glyph.properties.ys.internal = true;
        node_renderer.glyph.properties.x.internal = true;
        node_renderer.glyph.properties.y.internal = true;
        edge_renderer.glyph.xs = { expr: edge_coords.x };
        edge_renderer.glyph.ys = { expr: edge_coords.y };
        node_renderer.glyph.x = { expr: node_coords.x };
        node_renderer.glyph.y = { expr: node_coords.y };
    }
    remove() {
        this.edge_view.remove();
        this.node_view.remove();
        super.remove();
    }
    _render() {
        this.edge_view.render();
        this.node_view.render();
    }
    renderer_view(renderer) {
        if (renderer instanceof GlyphRenderer) {
            if (renderer == this.edge_view.model)
                return this.edge_view;
            if (renderer == this.node_view.model)
                return this.node_view;
        }
        return super.renderer_view(renderer);
    }
}
export class GraphRenderer extends DataRenderer {
    static __name__ = "GraphRenderer";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = GraphRendererView;
        this.define(({ Ref }) => ({
            layout_provider: [Ref(LayoutProvider)],
            node_renderer: [Ref(GlyphRenderer)],
            edge_renderer: [Ref(GlyphRenderer)],
            selection_policy: [Ref(GraphHitTestPolicy), () => new NodesOnly()],
            inspection_policy: [Ref(GraphHitTestPolicy), () => new NodesOnly()],
        }));
    }
    get_selection_manager() {
        return this.node_renderer.data_source.selection_manager;
    }
}
//# sourceMappingURL=graph_renderer.js.map