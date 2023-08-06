var _a;
import { div } from "@bokehjs/core/dom";
import { ModelEvent } from "@bokehjs/core/bokeh_events";
import { isArray } from "@bokehjs/core/util/types";
import { HTMLBox, HTMLBoxView, set_size } from "./layout";
import { debounce } from "debounce";
export class VegaEvent extends ModelEvent {
    constructor(data) {
        super();
        this.data = data;
        this.event_name = "vega_event";
        this.publish = true;
    }
    get event_values() {
        return { model: this.origin, data: this.data };
    }
}
VegaEvent.__name__ = "VegaEvent";
export class VegaPlotView extends HTMLBoxView {
    connect_signals() {
        super.connect_signals();
        const { data, show_actions, theme } = this.model.properties;
        this.on_change([data, show_actions, theme], () => {
            this._plot();
        });
        this.connect(this.model.properties.data_sources.change, () => this._connect_sources());
        this.connect(this.model.properties.events.change, () => {
            for (const event of this.model.events) {
                if (this._callbacks.indexOf(event) > -1)
                    continue;
                this._callbacks.push(event);
                const callback = (name, value) => this._dispatch_event(name, value);
                const timeout = this.model.throttle[event] || 20;
                this.vega_view.addSignalListener(event, debounce(callback, timeout, false));
            }
        });
        this._connected = [];
        this._connect_sources();
    }
    _connect_sources() {
        for (const ds in this.model.data_sources) {
            const cds = this.model.data_sources[ds];
            if (this._connected.indexOf(ds) < 0) {
                this.connect(cds.properties.data.change, this._plot);
                this._connected.push(ds);
            }
        }
    }
    _dispatch_event(name, value) {
        if ('vlPoint' in value && value.vlPoint.or != null) {
            const indexes = [];
            for (const index of value.vlPoint.or)
                indexes.push(index._vgsid_);
            value = indexes;
        }
        this.model.trigger_event(new VegaEvent({ type: name, value: value }));
    }
    _fetch_datasets() {
        const datasets = {};
        for (const ds in this.model.data_sources) {
            const cds = this.model.data_sources[ds];
            const data = [];
            const columns = cds.columns();
            for (let i = 0; i < cds.get_length(); i++) {
                const item = {};
                for (const column of columns) {
                    item[column] = cds.data[column][i];
                }
                data.push(item);
            }
            datasets[ds] = data;
        }
        return datasets;
    }
    render() {
        super.render();
        this.container = div();
        set_size(this.container, this.model);
        this._callbacks = [];
        this._plot();
        this.shadow_el.append(this.container);
    }
    _plot() {
        const data = this.model.data;
        if ((data == null) || !window.vegaEmbed)
            return;
        if (this.model.data_sources && (Object.keys(this.model.data_sources).length > 0)) {
            const datasets = this._fetch_datasets();
            if ('data' in datasets) {
                data.data['values'] = datasets['data'];
                delete datasets['data'];
            }
            if (data.data != null) {
                const data_objs = isArray(data.data) ? data.data : [data.data];
                for (const d of data_objs) {
                    if (d.name in datasets) {
                        d['values'] = datasets[d.name];
                        delete datasets[d.name];
                    }
                }
            }
            this.model.data['datasets'] = datasets;
        }
        const config = { actions: this.model.show_actions, theme: this.model.theme };
        window.vegaEmbed(this.container, this.model.data, config).then((result) => {
            this.vega_view = result.view;
            result.view.addResizeListener(() => {
                this.resize_view(result.view);
            });
            this.resize_view(result.view);
            const callback = (name, value) => this._dispatch_event(name, value);
            for (const event of this.model.events) {
                this._callbacks.push(event);
                const timeout = this.model.throttle[event] || 20;
                this.vega_view.addSignalListener(event, debounce(callback, timeout, false));
            }
        });
    }
    resize_view(view) {
        let rect = this.container.getBoundingClientRect();
        console.log(rect.width, rect.height);
        view._el.children[0].style.width = `${rect.width}px`;
        view._el.children[0].style.height = `${rect.height}px`;
        view.resize().runAsync();
    }
}
VegaPlotView.__name__ = "VegaPlotView";
export class VegaPlot extends HTMLBox {
    constructor(attrs) {
        super(attrs);
    }
}
_a = VegaPlot;
VegaPlot.__name__ = "VegaPlot";
VegaPlot.__module__ = "panel.models.vega";
(() => {
    _a.prototype.default_view = VegaPlotView;
    _a.define(({ Any, Array, Boolean, Nullable, String }) => ({
        data: [Any, {}],
        data_sources: [Any, {}],
        events: [Array(String), []],
        show_actions: [Boolean, false],
        theme: [Nullable(String), null],
        throttle: [Any, {}]
    }));
})();
//# sourceMappingURL=vega.js.map