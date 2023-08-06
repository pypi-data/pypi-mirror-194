import { Int, Percent, NonNegative, Or, Tuple, PartialStruct, Auto } from "../../core/kinds";
import * as enums from "../../core/enums";
const Length = NonNegative(Int);
const XY = (type) => PartialStruct({ x: type, y: type });
const LRTB = (type) => PartialStruct({ left: type, right: type, top: type, bottom: type });
export const Anchor = (Or(enums.Anchor, Tuple(Or(enums.Align, enums.HAlign, Percent), Or(enums.Align, enums.VAlign, Percent))));
export const TextAnchor = Or(Anchor, Auto);
export const Padding = (Or(Length, Tuple(Length, Length), XY(Length), Tuple(Length, Length, Length, Length), LRTB(Length)));
export const BorderRadius = (Or(Length, Tuple(Length, Length, Length, Length), PartialStruct({
    top_left: Length,
    top_right: Length,
    bottom_right: Length,
    bottom_left: Length,
})));
//# sourceMappingURL=kinds.js.map