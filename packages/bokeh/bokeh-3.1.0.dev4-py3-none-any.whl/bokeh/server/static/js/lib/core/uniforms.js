import { equals } from "./util/eq";
export class Uniform {
    static __name__ = "Uniform";
    is_Scalar() { return this.is_scalar; }
    is_Vector() { return !this.is_scalar; }
}
export class UniformScalar extends Uniform {
    value;
    length;
    static __name__ = "UniformScalar";
    is_scalar = true;
    constructor(value, length) {
        super();
        this.value = value;
        this.length = length;
    }
    get(_i) {
        return this.value;
    }
    *[Symbol.iterator]() {
        const { length, value } = this;
        for (let i = 0; i < length; i++) {
            yield value;
        }
    }
    select(indices) {
        return new UniformScalar(this.value, indices.count);
    }
    [equals](that, cmp) {
        return cmp.eq(this.length, that.length) && cmp.eq(this.value, that.value);
    }
}
export class UniformVector extends Uniform {
    array;
    static __name__ = "UniformVector";
    is_scalar = false;
    length;
    constructor(array) {
        super();
        this.array = array;
        this.length = this.array.length;
    }
    get(i) {
        return this.array[i];
    }
    *[Symbol.iterator]() {
        yield* this.array;
    }
    select(indices) {
        const array = indices.select(this.array);
        return new this.constructor(array);
    }
    [equals](that, cmp) {
        return cmp.eq(this.length, that.length) && cmp.eq(this.array, that.array);
    }
}
export class ColorUniformVector extends UniformVector {
    array;
    static __name__ = "ColorUniformVector";
    _view;
    constructor(array) {
        super(array);
        this.array = array;
        this._view = new DataView(array.buffer);
    }
    get(i) {
        return this._view.getUint32(4 * i);
    }
    *[Symbol.iterator]() {
        const n = this.length;
        for (let i = 0; i < n; i++)
            yield this.get(i);
    }
}
//# sourceMappingURL=uniforms.js.map