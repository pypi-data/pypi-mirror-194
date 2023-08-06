import { JupyterFrontEndContextMenu, JupyterLab, } from '@jupyterlab/application';
import { CommandLinker } from '@jupyterlab/apputils';
import { PageConfig } from '@jupyterlab/coreutils';
import { ContextMenuSvg } from '@jupyterlab/ui-components';
import { Application } from '@lumino/application';
import { Signal } from '@lumino/signaling';
import { QuetzServiceManager } from './servicemanager';
import { Shell } from './shell';
/**
 * App is the main application class. It is instantiated once and shared.
 */
export class App extends Application {
    /**
     * Construct a new App object.
     *
     * @param options The instantiation options for an application.
     */
    constructor(options = {}) {
        var _a;
        super(Object.assign(Object.assign({}, options), { shell: (_a = options.shell) !== null && _a !== void 0 ? _a : new Shell() }));
        /**
         * The name of the JupyterLab application.
         */
        this.name = PageConfig.getOption('appName') || 'Quetz';
        /**
         * A namespace/prefix plugins may use to denote their provenance.
         */
        this.namespace = PageConfig.getOption('appNamespace') || this.name;
        /**
         * A list of all errors encountered when registering plugins.
         */
        this.registerPluginErrors = [];
        /**
         * The version of the JupyterLab application.
         */
        this.version = PageConfig.getOption('appVersion') || 'unknown';
        this._formatChanged = new Signal(this);
        this.serviceManager = new QuetzServiceManager();
        // render context menu/submenus with inline svg icon tweaks
        this.contextMenu = new ContextMenuSvg({
            commands: this.commands,
            renderer: options.contextMenuRenderer,
            groupByTarget: false,
            sortBySelector: false,
        });
        // The default restored promise if one does not exist in the options.
        const restored = new Promise((resolve) => {
            requestAnimationFrame(() => {
                resolve();
            });
        });
        this.commandLinker =
            options.commandLinker || new CommandLinker({ commands: this.commands });
        this.restored =
            options.restored ||
                this.started.then(() => restored).catch(() => restored);
    }
    /**
     * The application form factor, e.g., `desktop` or `mobile`.
     */
    get format() {
        return this._format;
    }
    set format(format) {
        if (this._format !== format) {
            this._format = format;
            document.body.dataset['format'] = format;
            this._formatChanged.emit(format);
        }
    }
    /**
     * A signal that emits when the application form factor changes.
     */
    get formatChanged() {
        return this._formatChanged;
    }
    /**
     * The Quetz application paths dictionary.
     */
    get paths() {
        return JupyterLab.defaultPaths;
    }
    /**
     * Walks up the DOM hierarchy of the target of the active `contextmenu`
     * event, testing each HTMLElement ancestor for a user-supplied function. This can
     * be used to find an HTMLElement on which to operate, given a context menu click.
     *
     * @param fn - a function that takes an `HTMLElement` and returns a
     *   boolean for whether it is the element the requester is seeking.
     * @returns an HTMLElement or undefined, if none is found.
     */
    contextMenuHitTest(fn) {
        if (!this._contextMenuEvent ||
            !(this._contextMenuEvent.target instanceof Node)) {
            return undefined;
        }
        let node = this._contextMenuEvent.target;
        do {
            if (node instanceof HTMLElement && fn(node)) {
                return node;
            }
            node = node.parentNode;
        } while (node && node.parentNode && node !== node.parentNode);
        return undefined;
        // TODO: we should be able to use .composedPath() to simplify this function
        // down to something like the below, but it seems like composedPath is
        // sometimes returning an empty list.
        /*
        if (this._contextMenuEvent) {
          this._contextMenuEvent
            .composedPath()
            .filter(x => x instanceof HTMLElement)
            .find(test);
        }
        return undefined;
        */
    }
    /**
     * A method invoked on a document `'contextmenu'` event.
     *
     * @param event mouse event
     */
    evtContextMenu(event) {
        this._contextMenuEvent = event;
        if (event.shiftKey) {
            return;
        }
        const opened = this.contextMenu.open(event);
        if (opened) {
            const items = this.contextMenu.menu.items;
            // If only the context menu information will be shown,
            // with no real commands, close the context menu and
            // allow the native one to open.
            if (items.length === 1 &&
                items[0].command === JupyterFrontEndContextMenu.contextMenu) {
                this.contextMenu.menu.close();
                return;
            }
            // Stop propagation and allow the application context menu to show.
            event.preventDefault();
            event.stopPropagation();
        }
    }
    /**
     * Register plugins from a plugin module.
     *
     * @param mod - The plugin module to register.
     */
    registerPluginModule(mod) {
        let data = mod.default;
        // Handle commonjs exports.
        if (!Object.prototype.hasOwnProperty.call(mod, '__esModule')) {
            data = mod;
        }
        if (!Array.isArray(data)) {
            data = [data];
        }
        data.forEach((item) => {
            try {
                this.registerPlugin(item);
            }
            catch (error) {
                this.registerPluginErrors.push(error);
            }
        });
    }
    /**
     * Register the plugins from multiple plugin modules.
     *
     * @param mods - The plugin modules to register.
     */
    registerPluginModules(mods) {
        mods.forEach((mod) => {
            this.registerPluginModule(mod);
        });
    }
}
//# sourceMappingURL=app.js.map