"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.BuildError = void 0;
class BuildError extends Error {
    component;
    static __name__ = "BuildError";
    constructor(component, message) {
        super(message);
        this.component = component;
    }
}
exports.BuildError = BuildError;
//# sourceMappingURL=error.js.map