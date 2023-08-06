var _a;
import { div } from "@bokehjs/core/dom";
import { HTMLBox, HTMLBoxView } from "./layout";
export class EChartsView extends HTMLBoxView {
    connect_signals() {
        super.connect_signals();
        this.connect(this.model.properties.data.change, () => this._plot());
        const { width, height, renderer, theme } = this.model.properties;
        this.on_change([width, height], () => this._resize());
        this.on_change([theme, renderer], () => this.render());
    }
    render() {
        if (this._chart != null)
            window.echarts.dispose(this._chart);
        super.render();
        this.container = div({ style: "height: 100%; width: 100%;" });
        const config = { width: this.model.width, height: this.model.height, renderer: this.model.renderer };
        this._chart = window.echarts.init(this.container, this.model.theme, config);
        this._plot();
        this.shadow_el.append(this.container);
        this._chart.resize();
    }
    remove() {
        super.remove();
        if (this._chart != null)
            window.echarts.dispose(this._chart);
    }
    after_layout() {
        super.after_layout();
        this._chart.resize();
    }
    _plot() {
        if (window.echarts == null)
            return;
        this._chart.setOption(this.model.data);
    }
    _resize() {
        this._chart.resize({ width: this.model.width, height: this.model.height });
    }
}
EChartsView.__name__ = "EChartsView";
export class ECharts extends HTMLBox {
    constructor(attrs) {
        super(attrs);
    }
}
_a = ECharts;
ECharts.__name__ = "ECharts";
ECharts.__module__ = "panel.models.echarts";
(() => {
    _a.prototype.default_view = EChartsView;
    _a.define(({ Any, String }) => ({
        data: [Any, {}],
        theme: [String, "default"],
        renderer: [String, "canvas"]
    }));
})();
//# sourceMappingURL=echarts.js.map