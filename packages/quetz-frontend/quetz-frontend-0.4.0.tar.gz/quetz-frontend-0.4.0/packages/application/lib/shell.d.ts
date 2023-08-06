import { JupyterFrontEnd } from '@jupyterlab/application';
import type { DocumentRegistry } from '@jupyterlab/docregistry';
import { IIterator } from '@lumino/algorithm';
import { Widget } from '@lumino/widgets';
export declare type IShell = Shell;
/**
 * A namespace for Shell statics
 */
export declare namespace IShell {
    /**
     * The areas of the application shell where widgets can reside.
     */
    type Area = 'main' | 'top' | 'bottom';
}
/**
 * The application shell.
 */
export declare class Shell extends Widget implements JupyterFrontEnd.IShell {
    constructor();
    activateById(id: string): void;
    /**
     * Add a widget to the application shell.
     *
     * @param widget - The widget being added.
     * @param area - Optional region in the shell into which the widget should
     * be added.
     * @param options
     */
    add(widget: Widget, area?: IShell.Area, options?: DocumentRegistry.IOpenOptions): void;
    /**
     * The current widget in the shell's main area.
     */
    get currentWidget(): Widget;
    /**
     * Get the top area wrapper panel
     */
    get top(): Widget;
    /**
     * Get the bottom area wrapper panel
     */
    get bottom(): Widget;
    widgets(area: IShell.Area): IIterator<Widget>;
    /**
     * Add a widget to the main content area.
     *
     * @param widget The widget to add.
     */
    private _addToMainArea;
    private _main;
    private _top;
    private _topWrapper;
    private _bottom;
    private _bottomWrapper;
}
