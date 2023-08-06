export class VisualProperties {
    obj;
    prefix;
    static __name__ = "VisualProperties";
    _props;
    *[Symbol.iterator]() {
        yield* this._props;
    }
    constructor(obj, prefix = "") {
        this.obj = obj;
        this.prefix = prefix;
        const self = this;
        this._props = [];
        for (const attr of this.attrs) {
            const prop = obj.model.properties[prefix + attr];
            prop.change.connect(() => this.update());
            self[attr] = prop;
            this._props.push(prop);
        }
    }
    update() { }
}
export class VisualUniforms {
    obj;
    prefix;
    static __name__ = "VisualUniforms";
    *[Symbol.iterator]() {
        for (const attr of this.attrs) {
            yield this.obj.model.properties[this.prefix + attr];
        }
    }
    constructor(obj, prefix = "") {
        this.obj = obj;
        this.prefix = prefix;
        for (const attr of this.attrs) {
            Object.defineProperty(this, attr, {
                get() {
                    return obj[prefix + attr];
                },
            });
        }
    }
    update() { }
}
//# sourceMappingURL=visual.js.map