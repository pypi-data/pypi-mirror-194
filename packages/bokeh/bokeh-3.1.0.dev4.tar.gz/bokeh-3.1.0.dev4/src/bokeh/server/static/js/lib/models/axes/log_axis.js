import { ContinuousAxis, ContinuousAxisView } from "./continuous_axis";
import { LogTickFormatter } from "../formatters/log_tick_formatter";
import { LogTicker } from "../tickers/log_ticker";
export class LogAxisView extends ContinuousAxisView {
    static __name__ = "LogAxisView";
}
export class LogAxis extends ContinuousAxis {
    static __name__ = "LogAxis";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = LogAxisView;
        this.override({
            ticker: () => new LogTicker(),
            formatter: () => new LogTickFormatter(),
        });
    }
}
//# sourceMappingURL=log_axis.js.map