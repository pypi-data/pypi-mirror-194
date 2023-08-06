import tz from "timezone";
import * as Numbro from "@bokeh/numbro";
import { _ } from "underscore.template";
import { div, i } from "../../../core/dom";
import { FontStyle, TextAlign, RoundingFunction } from "../../../core/enums";
import { isNumber, isString } from "../../../core/util/types";
import { to_fixed } from "../../../core/util/string";
import { color2css } from "../../../core/util/color";
import { Model } from "../../../model";
export class CellFormatter extends Model {
    static __name__ = "CellFormatter";
    constructor(attrs) {
        super(attrs);
    }
    doFormat(_row, _cell, value, _columnDef, _dataContext) {
        if (value == null)
            return "";
        else
            return `${value}`.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }
}
export class StringFormatter extends CellFormatter {
    static __name__ = "StringFormatter";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ Color, Nullable, String }) => ({
            font_style: [FontStyle, "normal"],
            text_align: [TextAlign, "left"],
            text_color: [Nullable(Color), null],
            nan_format: [String, "-"],
        }));
    }
    doFormat(_row, _cell, value, _columnDef, _dataContext) {
        const { font_style, text_align, text_color } = this;
        const text = div(value == null ? "" : `${value}`);
        switch (font_style) {
            case "normal":
                break;
            case "bold":
                text.style.fontWeight = "bold";
                break;
            case "italic":
                text.style.fontStyle = "italic";
                break;
            case "bold italic":
                text.style.fontWeight = "bold";
                text.style.fontStyle = "italic";
                break;
        }
        text.style.textAlign = text_align;
        if (text_color != null)
            text.style.color = color2css(text_color);
        return text.outerHTML;
    }
}
export class ScientificFormatter extends StringFormatter {
    static __name__ = "ScientificFormatter";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ Number }) => ({
            precision: [Number, 10],
            power_limit_high: [Number, 5],
            power_limit_low: [Number, -3],
        }));
    }
    get scientific_limit_low() {
        return 10.0 ** this.power_limit_low;
    }
    get scientific_limit_high() {
        return 10.0 ** this.power_limit_high;
    }
    doFormat(row, cell, value, columnDef, dataContext) {
        const need_sci = Math.abs(value) <= this.scientific_limit_low || Math.abs(value) >= this.scientific_limit_high;
        let precision = this.precision;
        // toExponential does not handle precision values < 0 correctly
        if (precision < 1) {
            precision = 1;
        }
        if (value == null || isNaN(value))
            value = this.nan_format;
        else if (value == 0)
            value = to_fixed(value, 1);
        else if (need_sci)
            value = value.toExponential(precision);
        else
            value = to_fixed(value, precision);
        // add StringFormatter formatting
        return super.doFormat(row, cell, value, columnDef, dataContext);
    }
}
export class NumberFormatter extends StringFormatter {
    static __name__ = "NumberFormatter";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ String }) => ({
            format: [String, "0,0"],
            language: [String, "en"],
            rounding: [RoundingFunction, "round"],
        }));
    }
    doFormat(row, cell, value, columnDef, dataContext) {
        const { format, language, nan_format } = this;
        const rounding = (() => {
            switch (this.rounding) {
                case "round":
                case "nearest": return Math.round;
                case "floor":
                case "rounddown": return Math.floor;
                case "ceil":
                case "roundup": return Math.ceil;
            }
        })();
        if (value == null || isNaN(value))
            value = nan_format;
        else
            value = Numbro.format(value, format, language, rounding);
        return super.doFormat(row, cell, value, columnDef, dataContext);
    }
}
export class BooleanFormatter extends CellFormatter {
    static __name__ = "BooleanFormatter";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ String }) => ({
            icon: [String, "check"],
        }));
    }
    doFormat(_row, _cell, value, _columnDef, _dataContext) {
        return !!value ? i({ class: this.icon }).outerHTML : "";
    }
}
export class DateFormatter extends StringFormatter {
    static __name__ = "DateFormatter";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ String }) => ({
            format: [String, "ISO-8601"],
        }));
    }
    getFormat() {
        // using definitions provided here: https://api.jqueryui.com/datepicker/
        // except not implementing TICKS
        switch (this.format) {
            case "ATOM":
            case "W3C":
            case "RFC-3339":
            case "ISO-8601":
                return "%Y-%m-%d";
            case "COOKIE":
                return "%a, %d %b %Y";
            case "RFC-850":
                return "%A, %d-%b-%y";
            case "RFC-1123":
            case "RFC-2822":
                return "%a, %e %b %Y";
            case "RSS":
            case "RFC-822":
            case "RFC-1036":
                return "%a, %e %b %y";
            case "TIMESTAMP":
                return undefined;
            default:
                return this.format;
        }
    }
    doFormat(row, cell, value, columnDef, dataContext) {
        function parse(date) {
            /* Parse bare dates as UTC. */
            const has_tz = /Z$|[+-]\d\d((:?)\d\d)?$/.test(date); // ISO 8601 TZ designation or offset
            const iso_date = has_tz ? date : `${date}Z`;
            return new Date(iso_date).getTime();
        }
        const epoch = (() => {
            if (value == null || isNumber(value)) {
                return value;
            }
            else if (isString(value)) {
                const epoch = Number(value);
                return isNaN(epoch) ? parse(value) : epoch;
            }
            else if (value instanceof Date) {
                return value.valueOf();
            }
            else {
                return Number(value);
            }
        })();
        const NaT = -9223372036854776.0;
        const date = (() => {
            if (epoch == null || isNaN(epoch) || epoch == NaT)
                return this.nan_format;
            else
                return tz(epoch, this.getFormat());
        })();
        return super.doFormat(row, cell, date, columnDef, dataContext);
    }
}
export class HTMLTemplateFormatter extends CellFormatter {
    static __name__ = "HTMLTemplateFormatter";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ String }) => ({
            template: [String, "<%= value %>"],
        }));
    }
    doFormat(_row, _cell, value, _columnDef, dataContext) {
        const { template } = this;
        if (value == null)
            return "";
        else {
            const compiled_template = _.template(template);
            const context = { ...dataContext, value };
            return compiled_template(context);
        }
    }
}
//# sourceMappingURL=cell_formatters.js.map