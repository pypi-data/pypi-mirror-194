import { classes, LabIcon } from '@jupyterlab/ui-components';
import { ArrayExt, iter } from '@lumino/algorithm';
import { Panel, Widget, BoxLayout } from '@lumino/widgets';
import { MessageLoop } from '@lumino/messaging';
/**
 * The default rank for ranked panels.
 */
const DEFAULT_RANK = 900;
/**
 * The application shell.
 */
export class Shell extends Widget {
    constructor() {
        super();
        this.id = 'main';
        const rootLayout = new BoxLayout();
        this._top = new Private.PanelHandler();
        this._bottom = new Private.PanelHandler();
        this._main = new Panel();
        this._bottom.panel.id = 'bottom-panel';
        this._top.panel.id = 'top-panel';
        this._main.id = 'main-panel';
        BoxLayout.setStretch(this._top.panel, 0);
        BoxLayout.setStretch(this._bottom.panel, 0);
        BoxLayout.setStretch(this._main, 1);
        // this._main.spacing = 5;
        rootLayout.spacing = 0;
        rootLayout.addWidget(this._top.panel);
        rootLayout.addWidget(this._main);
        rootLayout.addWidget(this._bottom.panel);
        this.layout = rootLayout;
    }
    activateById(id) {
        // no-op
    }
    /**
     * Add a widget to the application shell.
     *
     * @param widget - The widget being added.
     * @param area - Optional region in the shell into which the widget should
     * be added.
     * @param options
     */
    add(widget, area, options) {
        var _a;
        const rank = (_a = options === null || options === void 0 ? void 0 : options.rank) !== null && _a !== void 0 ? _a : DEFAULT_RANK;
        if (area === 'top') {
            return this._top.addWidget(widget, rank);
        }
        if (area === 'bottom') {
            return this._bottom.addWidget(widget, rank);
        }
        if (area === 'main' || area === undefined) {
            // if (this._main.widgets.length > 0) {
            //   // do not add the widget if there is already one
            //   return;
            // }
            this._addToMainArea(widget);
        }
        return;
    }
    /**
     * The current widget in the shell's main area.
     */
    get currentWidget() {
        // TODO: use a focus tracker to return the current widget
        return this._main.widgets[0];
    }
    /**
     * Get the top area wrapper panel
     */
    get top() {
        return this._topWrapper;
    }
    /**
     * Get the bottom area wrapper panel
     */
    get bottom() {
        return this._bottomWrapper;
    }
    widgets(area) {
        if (area === 'top') {
            return iter(this._top.panel.widgets);
        }
        return iter(this._main.widgets);
    }
    /**
     * Add a widget to the main content area.
     *
     * @param widget The widget to add.
     */
    _addToMainArea(widget) {
        if (!widget.id) {
            console.error('Widgets added to the app shell must have unique id property.');
            return;
        }
        const dock = this._main;
        const { title } = widget;
        title.dataset = Object.assign(Object.assign({}, title.dataset), { id: widget.id });
        if (title.icon instanceof LabIcon) {
            // bind an appropriate style to the icon
            title.icon = title.icon.bindprops({
                stylesheet: 'mainAreaTab',
            });
        }
        else if (typeof title.icon === 'string' || !title.icon) {
            // add some classes to help with displaying css background imgs
            title.iconClass = classes(title.iconClass, 'jp-Icon');
        }
        if (dock.widgets.length) {
            dock.widgets[0].dispose();
        }
        dock.addWidget(widget);
    }
}
var Private;
(function (Private) {
    /**
     * A less-than comparison function for side bar rank items.
     *
     * @param first
     * @param second
     */
    function itemCmp(first, second) {
        return first.rank - second.rank;
    }
    Private.itemCmp = itemCmp;
    /**
     * A class which manages a panel and sorts its widgets by rank.
     */
    class PanelHandler {
        constructor() {
            /**
             * A message hook for child add/remove messages on the main area dock panel.
             *
             * @param handler
             * @param msg
             */
            this._panelChildHook = (handler, msg) => {
                switch (msg.type) {
                    case 'child-added':
                        {
                            const widget = msg.child;
                            // If we already know about this widget, we're done
                            if (this._items.find((v) => v.widget === widget)) {
                                break;
                            }
                            // Otherwise, add to the end by default
                            const rank = this._items[this._items.length - 1].rank;
                            this._items.push({ widget, rank });
                        }
                        break;
                    case 'child-removed':
                        {
                            const widget = msg.child;
                            ArrayExt.removeFirstWhere(this._items, (v) => v.widget === widget);
                        }
                        break;
                    default:
                        break;
                }
                return true;
            };
            this._items = new Array();
            this._panel = new Panel();
            MessageLoop.installMessageHook(this._panel, this._panelChildHook);
        }
        /**
         * Get the panel managed by the handler.
         */
        get panel() {
            return this._panel;
        }
        /**
         * Add a widget to the panel.
         *
         * If the widget is already added, it will be moved.
         *
         * @param widget
         * @param rank
         */
        addWidget(widget, rank) {
            widget.parent = null;
            const item = { widget, rank };
            const index = ArrayExt.upperBound(this._items, item, Private.itemCmp);
            ArrayExt.insert(this._items, index, item);
            this._panel.insertWidget(index, widget);
        }
    }
    Private.PanelHandler = PanelHandler;
})(Private || (Private = {}));
//# sourceMappingURL=shell.js.map