import ts from "typescript";
import { Path } from "./sys";
export type CompileConfig = {
    bokehjs_dir?: Path;
    inputs?(files: Path[]): Inputs;
};
export type Inputs = Map<Path, string>;
export type Outputs = Map<Path, string>;
export type Diagnostics = readonly ts.Diagnostic[];
export type Failed = {
    diagnostics: Diagnostics;
};
export declare function is_failed<T>(obj: T | Partial<Failed>): obj is Failed;
export type TSConfig = {
    files: Path[];
    options: ts.CompilerOptions;
    diagnostics?: undefined;
};
export interface TSOutput {
    diagnostics?: Diagnostics;
}
export declare function report_diagnostics(diagnostics: Diagnostics): {
    count: number;
    text: string;
};
export declare function compiler_host(inputs: Inputs, options: ts.CompilerOptions, bokehjs_dir?: Path): ts.CompilerHost;
export declare function default_transformers(options: ts.CompilerOptions): ts.CustomTransformers;
export declare function compile_files(inputs: Path[], options: ts.CompilerOptions, transformers?: ts.CustomTransformers, host?: ts.CompilerHost): TSOutput;
export type OutDir = Path | {
    js: Path;
    dts: Path;
};
export declare function parse_tsconfig(tsconfig_json: object, base_dir: Path, preconfigure?: ts.CompilerOptions): TSConfig | Failed;
export declare function read_tsconfig(tsconfig_path: Path, preconfigure?: ts.CompilerOptions): TSConfig | Failed;
export declare function compile_typescript(tsconfig_path: Path, config?: CompileConfig): void;
//# sourceMappingURL=compiler.d.ts.map