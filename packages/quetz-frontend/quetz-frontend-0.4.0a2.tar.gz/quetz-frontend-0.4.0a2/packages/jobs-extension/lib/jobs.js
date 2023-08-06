import { DOMUtils, ReactWidget } from '@jupyterlab/apputils';
import { ServerConnection } from '@jupyterlab/services';
import { URLExt } from '@jupyterlab/coreutils';
import { InlineLoader, Breadcrumbs, API_STATUSES, } from '@quetz-frontend/apputils';
import { Table } from '@quetz-frontend/table';
import * as React from 'react';
/**
 *
 */
export class Jobs extends ReactWidget {
    constructor(_router) {
        super();
        this._router = _router;
        this.id = DOMUtils.createDomID();
        this.title.label = 'Jobs main page';
        this._data = new Array();
        this._status = API_STATUSES.PENDING;
        this._loadData();
    }
    _loadData() {
        const settings = ServerConnection.makeSettings();
        const url = URLExt.join(settings.baseUrl, '/api/jobs');
        ServerConnection.makeRequest(url, {}, settings).then(async (resp) => {
            resp.json().then((data) => {
                /* TODO: Support pagination */
                this._data = data.result;
                this._status = API_STATUSES.SUCCESS;
                this.update();
            });
        });
    }
    render() {
        const breadcrumbItems = [
            {
                text: 'Home',
                onClick: () => {
                    this._router.navigate('/home');
                },
            },
            {
                text: 'Jobs',
            },
        ];
        return (React.createElement("div", { className: "page-contents-width-limit" },
            React.createElement(Breadcrumbs, { items: breadcrumbItems }),
            React.createElement("h2", { className: "heading2" }, "Jobs"),
            this._status === API_STATUSES.PENDING ? (React.createElement(InlineLoader, { text: "Fetching jobs" })) : (React.createElement(Table, { data: this._data, columns: getColumns(), enableSearch: true }))));
    }
}
const getColumns = () => [
    {
        Header: 'Manifest',
        accessor: 'manifest',
        disableFilters: true,
        Cell: ({ row }) => (
        //@ts-ignore
        React.createElement("div", { onClick: () => window.route.navigate(`/jobs/:${row.original.id}`) }, row.values.manifest)),
    },
    {
        Header: 'Created',
        accessor: 'created',
        Cell: ({ row }) => row.values.created,
    },
    {
        Header: 'Status',
        accessor: 'status',
        Cell: ({ row }) => row.values.status,
    },
    {
        Header: 'Owner',
        accessor: 'owner',
        Cell: ({ row }) => row.values.owner.username,
    },
];
//# sourceMappingURL=jobs.js.map