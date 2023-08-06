import { Breadcrumb, BreadcrumbItem, Button, } from '@jupyter-notebook/react-components';
import { IRouter } from '@jupyterlab/application';
import { DOMUtils, ReactWidget } from '@jupyterlab/apputils';
import { URLExt } from '@jupyterlab/coreutils';
import { ServerConnection } from '@jupyterlab/services';
import { Breadcrumbs, FetchHoc } from '@quetz-frontend/apputils';
import { Table } from '@quetz-frontend/table';
import * as React from 'react';
/**
 * The command ids used by the main plugin.
 */
export var CommandIDs;
(function (CommandIDs) {
    CommandIDs.open = '@quetz-frontend/search-extension:open';
})(CommandIDs || (CommandIDs = {}));
/**
 * The main menu plugin.
 */
const plugin = {
    id: '@quetz-frontend/search-extension:plugin',
    autoStart: true,
    requires: [IRouter],
    activate: (app, router) => {
        const { shell, commands } = app;
        commands.addCommand(CommandIDs.open, {
            execute: () => {
                shell.add(new SearchPage(router), 'main');
            },
        });
        router.register({
            pattern: /^\/search.*/,
            command: CommandIDs.open,
        });
    },
};
export default plugin;
class SearchPage extends ReactWidget {
    constructor(router) {
        super();
        this.id = DOMUtils.createDomID();
        this.title.label = 'Search page';
        this._router = router;
    }
    render() {
        const searchText = new URLSearchParams(window.location.search).get('q');
        const settings = ServerConnection.makeSettings();
        const url = URLExt.join(settings.baseUrl, `/api/packages/search/?q=${searchText}`);
        const breadcrumbItems = [
            {
                text: 'Home',
                onClick: () => {
                    this._route('/');
                },
            },
            {
                text: `Search for "${searchText}"`,
            },
        ];
        const columns = [
            {
                Header: 'Name',
                accessor: 'name',
                Cell: ({ row }) => (React.createElement(Breadcrumb, null,
                    React.createElement(BreadcrumbItem, null,
                        React.createElement(Button, { appearance: "lightweight", onClick: () => this._route(`/channels/${row.original.channel_name}`) }, row.original.channel_name)),
                    React.createElement(BreadcrumbItem, null,
                        React.createElement(Button, { appearance: "lightweight", onClick: () => this._route(`/channels/${row.original.channel_name}/packages/${row.values.name}`) }, row.values.name)))),
            },
            {
                Header: 'Summary',
                accessor: 'summary',
            },
            {
                Header: 'Version',
                accessor: 'current_version',
                Cell: ({ row }) => (row.values.current_version || React.createElement("i", null, "n/a")),
            },
        ];
        return (React.createElement("div", { className: "page-contents-width-limit" },
            React.createElement("h2", { className: "heading2" }, "Packages"),
            React.createElement("div", { className: "flex" },
                React.createElement(Breadcrumbs, { items: breadcrumbItems })),
            React.createElement("div", { className: "padding-side" },
                React.createElement(FetchHoc, { url: url, loadingMessage: "Searching for packages", genericErrorMessage: "Error fetching API keys" }, (data) => {
                    return React.createElement(Table, { columns: columns, data: data || [] });
                }))));
    }
    _route(route) {
        this._router.navigate(route);
    }
}
//# sourceMappingURL=index.js.map