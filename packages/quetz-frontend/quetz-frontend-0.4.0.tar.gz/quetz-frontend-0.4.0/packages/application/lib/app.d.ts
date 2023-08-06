import { JupyterFrontEnd } from '@jupyterlab/application';
import { CommandLinker } from '@jupyterlab/apputils';
import { ServiceManager } from '@jupyterlab/services';
import { ContextMenuSvg } from '@jupyterlab/ui-components';
import { Application, IPlugin } from '@lumino/application';
import { ISignal } from '@lumino/signaling';
import { IShell, Shell } from './shell';
export declare type QuetzFrontEnd = Application<JupyterFrontEnd.IShell>;
/**
 * The type for all QuetzFrontEnd application plugins.
 *
 * @typeparam T - The type that the plugin `provides` upon being activated.
 */
export declare type QuetzFrontEndPlugin<T> = IPlugin<QuetzFrontEnd, T>;
/**
 * App is the main application class. It is instantiated once and shared.
 */
export declare class App extends Application<Shell> {
    /**
     * Construct a new App object.
     *
     * @param options The instantiation options for an application.
     */
    constructor(options?: App.IOptions);
    /**
     * The name of the JupyterLab application.
     */
    readonly name: string;
    /**
     * A namespace/prefix plugins may use to denote their provenance.
     */
    readonly namespace: string;
    /**
     * A list of all errors encountered when registering plugins.
     */
    readonly registerPluginErrors: Array<Error>;
    /**
     * The version of the JupyterLab application.
     */
    readonly version: string;
    /**
     * The command linker used by the application.
     */
    readonly commandLinker: CommandLinker;
    /**
     * The application context menu.
     */
    readonly contextMenu: ContextMenuSvg;
    /**
     * Promise that resolves when state is first restored.
     */
    readonly restored: Promise<void>;
    /**
     * The service manager used by the application.
     */
    readonly serviceManager: ServiceManager.IManager;
    /**
     * The application form factor, e.g., `desktop` or `mobile`.
     */
    get format(): 'desktop' | 'mobile';
    set format(format: 'desktop' | 'mobile');
    /**
     * A signal that emits when the application form factor changes.
     */
    get formatChanged(): ISignal<this, 'desktop' | 'mobile'>;
    /**
     * The Quetz application paths dictionary.
     */
    get paths(): JupyterFrontEnd.IPaths;
    /**
     * Walks up the DOM hierarchy of the target of the active `contextmenu`
     * event, testing each HTMLElement ancestor for a user-supplied function. This can
     * be used to find an HTMLElement on which to operate, given a context menu click.
     *
     * @param fn - a function that takes an `HTMLElement` and returns a
     *   boolean for whether it is the element the requester is seeking.
     * @returns an HTMLElement or undefined, if none is found.
     */
    contextMenuHitTest(fn: (node: HTMLElement) => boolean): HTMLElement | undefined;
    /**
     * A method invoked on a document `'contextmenu'` event.
     *
     * @param event mouse event
     */
    protected evtContextMenu(event: MouseEvent): void;
    /**
     * Register plugins from a plugin module.
     *
     * @param mod - The plugin module to register.
     */
    registerPluginModule(mod: App.IPluginModule): void;
    /**
     * Register the plugins from multiple plugin modules.
     *
     * @param mods - The plugin modules to register.
     */
    registerPluginModules(mods: App.IPluginModule[]): void;
    private _contextMenuEvent;
    private _format;
    private _formatChanged;
}
/**
 * A namespace for App statics.
 */
export declare namespace App {
    /**
     * The instantiation options for an App application.
     */
    type IOptions = Partial<JupyterFrontEnd.IOptions<IShell>>;
    /**
     * The interface for a module that exports a plugin or plugins as
     * the default value.
     */
    interface IPluginModule {
        /**
         * The default export.
         */
        default: QuetzFrontEndPlugin<any> | QuetzFrontEndPlugin<any>[];
    }
}
