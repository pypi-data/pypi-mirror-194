import * as tp from "./util/types";
import { is_Color } from "./util/color";
import { keys, entries } from "./util/object";
const ESMap = globalThis.Map;
const ESSet = globalThis.Set;
const { hasOwnProperty } = Object.prototype;
export class Kind {
    static __name__ = "Kind";
    __type__;
}
export var Kinds;
(function (Kinds) {
    class Any extends Kind {
        static __name__ = "Any";
        valid(value) {
            return value !== undefined;
        }
        toString() {
            return "Any";
        }
    }
    Kinds.Any = Any;
    class Unknown extends Kind {
        static __name__ = "Unknown";
        valid(value) {
            return value !== undefined;
        }
        toString() {
            return "Unknown";
        }
    }
    Kinds.Unknown = Unknown;
    class Boolean extends Kind {
        static __name__ = "Boolean";
        valid(value) {
            return tp.isBoolean(value);
        }
        toString() {
            return "Boolean";
        }
    }
    Kinds.Boolean = Boolean;
    class Ref extends Kind {
        obj_type;
        static __name__ = "Ref";
        constructor(obj_type) {
            super();
            this.obj_type = obj_type;
        }
        valid(value) {
            return value instanceof this.obj_type;
        }
        toString() {
            const tp = this.obj_type;
            // NOTE: `__name__` is injected by a compiler transform
            const name = tp.__name__ ?? tp.toString();
            return `Ref(${name})`;
        }
    }
    Kinds.Ref = Ref;
    class AnyRef extends Kind {
        static __name__ = "AnyRef";
        valid(value) {
            return tp.isObject(value);
        }
        toString() {
            return "AnyRef";
        }
    }
    Kinds.AnyRef = AnyRef;
    class Number extends Kind {
        static __name__ = "Number";
        valid(value) {
            return tp.isNumber(value);
        }
        toString() {
            return "Number";
        }
    }
    Kinds.Number = Number;
    class Int extends Number {
        static __name__ = "Int";
        valid(value) {
            return super.valid(value) && tp.isInteger(value);
        }
        toString() {
            return "Int";
        }
    }
    Kinds.Int = Int;
    class Percent extends Number {
        static __name__ = "Percent";
        valid(value) {
            return super.valid(value) && 0 <= value && value <= 1;
        }
        toString() {
            return "Percent";
        }
    }
    Kinds.Percent = Percent;
    class Or extends Kind {
        types;
        static __name__ = "Or";
        constructor(types) {
            super();
            this.types = types;
            this.types = types;
        }
        valid(value) {
            return this.types.some((type) => type.valid(value));
        }
        toString() {
            return `Or(${this.types.map((type) => type.toString()).join(", ")})`;
        }
    }
    Kinds.Or = Or;
    class Tuple extends Kind {
        types;
        static __name__ = "Tuple";
        constructor(types) {
            super();
            this.types = types;
            this.types = types;
        }
        valid(value) {
            if (!tp.isArray(value))
                return false;
            for (let i = 0; i < this.types.length; i++) {
                const type = this.types[i];
                const item = value[i];
                if (!type.valid(item))
                    return false;
            }
            return true;
        }
        toString() {
            return `Tuple(${this.types.map((type) => type.toString()).join(", ")})`;
        }
    }
    Kinds.Tuple = Tuple;
    class Struct extends Kind {
        struct_type;
        static __name__ = "Struct";
        constructor(struct_type) {
            super();
            this.struct_type = struct_type;
        }
        valid(value) {
            if (!tp.isPlainObject(value))
                return false;
            const { struct_type } = this;
            for (const key of keys(value)) {
                if (!hasOwnProperty.call(struct_type, key))
                    return false;
            }
            for (const key in struct_type) {
                if (hasOwnProperty.call(struct_type, key)) {
                    const item_type = struct_type[key];
                    const item = value[key];
                    if (!item_type.valid(item))
                        return false;
                }
            }
            return true;
        }
        toString() {
            const items = entries(this.struct_type).map(([key, kind]) => `${key}: ${kind}`).join(", ");
            return `Struct({${items}})`;
        }
    }
    Kinds.Struct = Struct;
    class PartialStruct extends Kind {
        struct_type;
        static __name__ = "PartialStruct";
        constructor(struct_type) {
            super();
            this.struct_type = struct_type;
        }
        valid(value) {
            if (!tp.isPlainObject(value))
                return false;
            const { struct_type } = this;
            for (const key of keys(value)) {
                if (!hasOwnProperty.call(struct_type, key))
                    return false;
            }
            for (const key in struct_type) {
                if (!hasOwnProperty.call(value, key))
                    continue;
                if (hasOwnProperty.call(struct_type, key)) {
                    const item_type = struct_type[key];
                    const item = value[key];
                    if (!item_type.valid(item))
                        return false;
                }
            }
            return true;
        }
        toString() {
            const items = entries(this.struct_type).map(([key, kind]) => `${key}?: ${kind}`).join(", ");
            return `Struct({${items}})`;
        }
    }
    Kinds.PartialStruct = PartialStruct;
    class Arrayable extends Kind {
        item_type;
        static __name__ = "Arrayable";
        constructor(item_type) {
            super();
            this.item_type = item_type;
        }
        valid(value) {
            return tp.isArray(value) || tp.isTypedArray(value); // TODO: too specific
        }
        toString() {
            return `Arrayable(${this.item_type.toString()})`;
        }
    }
    Kinds.Arrayable = Arrayable;
    class Array extends Kind {
        item_type;
        static __name__ = "Array";
        constructor(item_type) {
            super();
            this.item_type = item_type;
        }
        valid(value) {
            return tp.isArray(value) && value.every((item) => this.item_type.valid(item));
        }
        toString() {
            return `Array(${this.item_type.toString()})`;
        }
    }
    Kinds.Array = Array;
    class Null extends Kind {
        static __name__ = "Null";
        valid(value) {
            return value === null;
        }
        toString() {
            return "Null";
        }
    }
    Kinds.Null = Null;
    class Nullable extends Kind {
        base_type;
        static __name__ = "Nullable";
        constructor(base_type) {
            super();
            this.base_type = base_type;
        }
        valid(value) {
            return value === null || this.base_type.valid(value);
        }
        toString() {
            return `Nullable(${this.base_type.toString()})`;
        }
    }
    Kinds.Nullable = Nullable;
    class Opt extends Kind {
        base_type;
        static __name__ = "Opt";
        constructor(base_type) {
            super();
            this.base_type = base_type;
        }
        valid(value) {
            return value === undefined || this.base_type.valid(value);
        }
        toString() {
            return `Opt(${this.base_type.toString()})`;
        }
    }
    Kinds.Opt = Opt;
    class Bytes extends Kind {
        static __name__ = "Bytes";
        valid(value) {
            return value instanceof ArrayBuffer;
        }
        toString() {
            return "Bytes";
        }
    }
    Kinds.Bytes = Bytes;
    class String extends Kind {
        static __name__ = "String";
        valid(value) {
            return tp.isString(value);
        }
        toString() {
            return "String";
        }
    }
    Kinds.String = String;
    class Regex extends String {
        regex;
        static __name__ = "Regex";
        constructor(regex) {
            super();
            this.regex = regex;
        }
        valid(value) {
            return super.valid(value) && this.regex.test(value);
        }
        toString() {
            return `Regex(${this.regex.toString()})`;
        }
    }
    Kinds.Regex = Regex;
    class Enum extends Kind {
        static __name__ = "Enum";
        values;
        constructor(values) {
            super();
            this.values = new ESSet(values);
        }
        valid(value) {
            return this.values.has(value);
        }
        *[Symbol.iterator]() {
            yield* this.values;
        }
        toString() {
            return `Enum(${[...this.values].map((v) => v.toString()).join(", ")})`;
        }
    }
    Kinds.Enum = Enum;
    class Dict extends Kind {
        item_type;
        static __name__ = "Dict";
        constructor(item_type) {
            super();
            this.item_type = item_type;
        }
        valid(value) {
            if (!tp.isPlainObject(value))
                return false;
            for (const key in value) {
                if (hasOwnProperty.call(value, key)) {
                    const item = value[key];
                    if (!this.item_type.valid(item))
                        return false;
                }
            }
            return true;
        }
        toString() {
            return `Dict(${this.item_type.toString()})`;
        }
    }
    Kinds.Dict = Dict;
    class Map extends Kind {
        key_type;
        item_type;
        static __name__ = "Map";
        constructor(key_type, item_type) {
            super();
            this.key_type = key_type;
            this.item_type = item_type;
        }
        valid(value) {
            if (!(value instanceof ESMap))
                return false;
            for (const [key, item] of value.entries()) {
                if (!(this.key_type.valid(key) && this.item_type.valid(item)))
                    return false;
            }
            return true;
        }
        toString() {
            return `Map(${this.key_type.toString()}, ${this.item_type.toString()})`;
        }
    }
    Kinds.Map = Map;
    class Set extends Kind {
        item_type;
        static __name__ = "Set";
        constructor(item_type) {
            super();
            this.item_type = item_type;
        }
        valid(value) {
            if (!(value instanceof ESSet))
                return false;
            for (const item of value) {
                if (!this.item_type.valid(item))
                    return false;
            }
            return true;
        }
        toString() {
            return `Set(${this.item_type.toString()})`;
        }
    }
    Kinds.Set = Set;
    class Color extends Kind {
        static __name__ = "Color";
        valid(value) {
            return is_Color(value);
        }
        toString() {
            return "Color";
        }
    }
    Kinds.Color = Color;
    class CSSLength extends String {
        static __name__ = "CSSLength";
        /*
        override valid(value: unknown): value is string {
          return super.valid(value) // TODO: && this._parse(value)
        }
        */
        toString() {
            return "CSSLength";
        }
    }
    Kinds.CSSLength = CSSLength;
    class Function extends Kind {
        static __name__ = "Function";
        valid(value) {
            return tp.isFunction(value);
        }
        toString() {
            return "Function(...)";
        }
    }
    Kinds.Function = Function;
    class NonNegative extends Kind {
        base_type;
        static __name__ = "NonNegative";
        constructor(base_type) {
            super();
            this.base_type = base_type;
        }
        valid(value) {
            return this.base_type.valid(value) && value >= 0;
        }
        toString() {
            return `NonNegative(${this.base_type.toString()})`;
        }
    }
    Kinds.NonNegative = NonNegative;
    class Positive extends Kind {
        base_type;
        static __name__ = "Positive";
        constructor(base_type) {
            super();
            this.base_type = base_type;
        }
        valid(value) {
            return this.base_type.valid(value) && value > 0;
        }
        toString() {
            return `Positive(${this.base_type.toString()})`;
        }
    }
    Kinds.Positive = Positive;
    class DOMNode extends Kind {
        static __name__ = "DOMNode";
        valid(value) {
            return value instanceof Node;
        }
        toString() {
            return "DOMNode";
        }
    }
    Kinds.DOMNode = DOMNode;
})(Kinds || (Kinds = {}));
export const Any = new Kinds.Any();
export const Unknown = new Kinds.Unknown();
export const Boolean = new Kinds.Boolean();
export const Number = new Kinds.Number();
export const Int = new Kinds.Int();
export const Bytes = new Kinds.Bytes();
export const String = new Kinds.String();
export const Regex = (regex) => new Kinds.Regex(regex);
export const Null = new Kinds.Null();
export const Nullable = (base_type) => new Kinds.Nullable(base_type);
export const Opt = (base_type) => new Kinds.Opt(base_type);
export const Or = (...types) => new Kinds.Or(types);
export const Tuple = (...types) => new Kinds.Tuple(types);
export const Struct = (struct_type) => new Kinds.Struct(struct_type);
export const PartialStruct = (struct_type) => new Kinds.PartialStruct(struct_type);
export const Arrayable = (item_type) => new Kinds.Arrayable(item_type);
export const Array = (item_type) => new Kinds.Array(item_type);
export const Dict = (item_type) => new Kinds.Dict(item_type);
export const Map = (key_type, item_type) => new Kinds.Map(key_type, item_type);
export const Set = (item_type) => new Kinds.Set(item_type);
export const Enum = (...values) => new Kinds.Enum(values);
export const Ref = (obj_type) => new Kinds.Ref(obj_type);
export const AnyRef = () => new Kinds.AnyRef();
export const Function = () => new Kinds.Function();
export const DOMNode = new Kinds.DOMNode();
export const NonNegative = (base_type) => new Kinds.NonNegative(base_type);
export const Positive = (base_type) => new Kinds.Positive(base_type);
export const Percent = new Kinds.Percent();
export const Alpha = Percent;
export const Color = new Kinds.Color();
export const Auto = Enum("auto");
export const CSSLength = new Kinds.CSSLength();
export const FontSize = String;
export const Font = String;
export const Angle = Number;
//# sourceMappingURL=kinds.js.map