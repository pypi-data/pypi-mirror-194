import { InputWidget, InputWidgetView } from "./input_widget";
import { input } from "../../core/dom";
import { isString } from "../../core/util/types";
import * as p from "../../core/properties";
import * as inputs from "../../styles/widgets/inputs.css";
import buttons_css from "../../styles/buttons.css";
export class FileInputView extends InputWidgetView {
    static __name__ = "FileInputView";
    styles() {
        return [...super.styles(), buttons_css];
    }
    render() {
        super.render();
        const { multiple, disabled } = this.model;
        const accept = (() => {
            const { accept } = this.model;
            return isString(accept) ? accept : accept.join(",");
        })();
        this.input_el = input({ type: "file", class: inputs.input, multiple, accept, disabled });
        this.group_el.appendChild(this.input_el);
        this.input_el.addEventListener("change", () => {
            const { files } = this.input_el;
            if (files != null) {
                this.load_files(files);
            }
        });
    }
    async load_files(files) {
        const values = [];
        const filenames = [];
        const mime_types = [];
        for (const file of files) {
            const data_url = await this._read_file(file);
            const [, mime_type = "", , value = ""] = data_url.split(/[:;,]/, 4);
            values.push(value);
            filenames.push(file.name);
            mime_types.push(mime_type);
        }
        const [value, filename, mime_type] = (() => {
            if (this.model.multiple)
                return [values, filenames, mime_types];
            else if (files.length != 0)
                return [values[0], filenames[0], mime_types[0]];
            else
                return ["", "", ""];
        })();
        this.model.setv({ value, filename, mime_type });
    }
    _read_file(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => {
                const { result } = reader;
                if (result != null) {
                    resolve(result);
                }
                else {
                    reject(reader.error ?? new Error(`unable to read '${file.name}'`));
                }
            };
            reader.readAsDataURL(file);
        });
    }
}
export class FileInput extends InputWidget {
    static __name__ = "FileInput";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = FileInputView;
        this.define(({ Boolean, String, Array, Or }) => ({
            value: [Or(String, Array(String)), p.unset, { readonly: true }],
            mime_type: [Or(String, Array(String)), p.unset, { readonly: true }],
            filename: [Or(String, Array(String)), p.unset, { readonly: true }],
            accept: [Or(String, Array(String)), ""],
            multiple: [Boolean, false],
        }));
    }
}
//# sourceMappingURL=file_input.js.map