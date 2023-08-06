import * as p from "@bokehjs/core/properties";
import { HTMLBox, HTMLBoxView } from "./layout";
export declare class EChartsView extends HTMLBoxView {
    model: ECharts;
    _chart: any;
    container: Element;
    connect_signals(): void;
    render(): void;
    remove(): void;
    after_layout(): void;
    _plot(): void;
    _resize(): void;
}
export declare namespace ECharts {
    type Attrs = p.AttrsOf<Props>;
    type Props = HTMLBox.Props & {
        data: p.Property<any>;
        renderer: p.Property<string>;
        theme: p.Property<string>;
    };
}
export interface ECharts extends ECharts.Attrs {
}
export declare class ECharts extends HTMLBox {
    properties: ECharts.Props;
    constructor(attrs?: Partial<ECharts.Attrs>);
    static __module__: string;
}
