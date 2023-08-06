import { IRouter } from '@jupyterlab/application';
import { DOMUtils, ReactWidget } from '@jupyterlab/apputils';
import { fileIcon } from '@jupyterlab/ui-components';
import { IMenu } from '@quetz-frontend/menu';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import * as React from 'react';
import ChannelsList from './channels/list';
import ChannelDetails from './channels/details';
import PackageDetails from './package';
/**
 * The command ids used by the channel plugin.
 */
export var CommandIDs;
(function (CommandIDs) {
    /**
     * Open channels page
     */
    CommandIDs.open = '@quetz-frontend/channels-extension:open';
    /**
     * Go to channels page
     */
    CommandIDs.gotoChannels = '@quetz-frontend/channels-extension:navigate-to-channels';
})(CommandIDs || (CommandIDs = {}));
/**
 * The main plugin.
 */
const plugin = {
    id: '@quetz-frontend/channels-extension:plugin',
    autoStart: true,
    requires: [IRouter, IMenu],
    activate: (app, router, menu) => {
        const { commands, shell } = app;
        commands.addCommand(CommandIDs.open, {
            label: 'Open Channels Panel',
            execute: () => {
                shell.add(new RouterWidget(router), 'main');
            },
        });
        commands.addCommand(CommandIDs.gotoChannels, {
            label: 'Channels',
            isVisible: () => menu.profile !== null,
            execute: () => {
                router.navigate('/channels');
            },
        });
        router.register({
            pattern: /^\/channels.*/,
            command: CommandIDs.open,
        });
        menu.addItem({
            command: CommandIDs.gotoChannels,
            rank: 200,
        });
    },
};
export default plugin;
class RouterWidget extends ReactWidget {
    constructor(_router) {
        super();
        this._router = _router;
        this.id = DOMUtils.createDomID();
        this.title.label = 'Channels main page';
        this.title.icon = fileIcon;
        this.addClass('jp-ReactWidget');
    }
    render() {
        return (React.createElement("div", { className: "page-contents-width-limit" },
            React.createElement(Router, { basename: "/channels" },
                React.createElement(Switch, null,
                    React.createElement(Route, { path: "/:channelId/packages/:packageId" },
                        React.createElement(PackageDetails, { router: this._router })),
                    React.createElement(Route, { path: "/:channelId" },
                        React.createElement(ChannelDetails, { router: this._router })),
                    React.createElement(Route, { path: "", exact: true },
                        React.createElement(ChannelsList, { router: this._router }))))));
    }
}
//# sourceMappingURL=index.js.map