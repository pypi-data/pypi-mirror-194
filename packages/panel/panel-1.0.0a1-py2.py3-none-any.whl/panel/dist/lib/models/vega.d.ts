import * as p from "@bokehjs/core/properties";
import { ModelEvent } from "@bokehjs/core/bokeh_events";
import { HTMLBox, HTMLBoxView } from "./layout";
import { Attrs } from "@bokehjs/core/types";
export declare class VegaEvent extends ModelEvent {
    readonly data: any;
    event_name: string;
    publish: boolean;
    constructor(data: any);
    protected get event_values(): Attrs;
}
export declare class VegaPlotView extends HTMLBoxView {
    model: VegaPlot;
    vega_view: any;
    container: HTMLDivElement;
    _callbacks: string[];
    _connected: string[];
    connect_signals(): void;
    _connect_sources(): void;
    _dispatch_event(name: string, value: any): void;
    _fetch_datasets(): any;
    render(): void;
    _plot(): void;
    resize_view(view: any): void;
}
export declare namespace VegaPlot {
    type Attrs = p.AttrsOf<Props>;
    type Props = HTMLBox.Props & {
        data: p.Property<any>;
        data_sources: p.Property<any>;
        events: p.Property<string[]>;
        show_actions: p.Property<boolean>;
        theme: p.Property<string | null>;
        throttle: p.Property<any>;
    };
}
export interface VegaPlot extends VegaPlot.Attrs {
}
export declare class VegaPlot extends HTMLBox {
    properties: VegaPlot.Props;
    constructor(attrs?: Partial<VegaPlot.Attrs>);
    static __module__: string;
}
