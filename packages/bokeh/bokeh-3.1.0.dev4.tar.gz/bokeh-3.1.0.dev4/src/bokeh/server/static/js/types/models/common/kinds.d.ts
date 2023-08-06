export type Anchor = typeof Anchor["__type__"];
export declare const Anchor: import("../../core/kinds").Kinds.Or<["center" | "left" | "right" | "top" | "bottom" | "center_center" | "center_left" | "center_right" | "top_center" | "top_left" | "top_right" | "bottom_center" | "bottom_left" | "bottom_right", [number | "start" | "center" | "end" | "left" | "right", number | "start" | "center" | "end" | "top" | "bottom"]]>;
export type TextAnchor = typeof TextAnchor["__type__"];
export declare const TextAnchor: import("../../core/kinds").Kinds.Or<["center" | "left" | "right" | "top" | "bottom" | "center_center" | "center_left" | "center_right" | "top_center" | "top_left" | "top_right" | "bottom_center" | "bottom_left" | "bottom_right" | [number | "start" | "center" | "end" | "left" | "right", number | "start" | "center" | "end" | "top" | "bottom"], "auto"]>;
export type Padding = typeof Padding["__type__"];
export declare const Padding: import("../../core/kinds").Kinds.Or<[number, [number, number], Partial<{
    x: number;
    y: number;
}>, [number, number, number, number], Partial<{
    left: number;
    right: number;
    top: number;
    bottom: number;
}>]>;
export type BorderRadius = typeof BorderRadius["__type__"];
export declare const BorderRadius: import("../../core/kinds").Kinds.Or<[number, [number, number, number, number], Partial<{
    top_left: number;
    top_right: number;
    bottom_right: number;
    bottom_left: number;
}>]>;
//# sourceMappingURL=kinds.d.ts.map