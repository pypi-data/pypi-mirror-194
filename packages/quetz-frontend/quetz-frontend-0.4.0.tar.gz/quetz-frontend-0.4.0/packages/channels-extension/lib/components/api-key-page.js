import { ServerConnection } from '@jupyterlab/services';
import { URLExt } from '@jupyterlab/coreutils';
import { FetchHoc } from '@quetz-frontend/apputils';
import { Table } from '@quetz-frontend/table';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTrash, faCopy } from '@fortawesome/free-solid-svg-icons';
import { some, filter } from 'lodash';
import * as React from 'react';
import { Button } from '@jupyter-notebook/react-components';
class ApiKeyComponent extends React.PureComponent {
    constructor() {
        super(...arguments);
        this.onCopy = (key) => {
            // TODO
            console.log('Copied key: ', key);
        };
        this.onDelete = (key) => {
            // TODO
            console.log('Deleted key: ', key);
        };
    }
    render() {
        const { apiKeyList, filters } = this.props;
        // Filter the list if matches in roles
        const filteredList = filters
            ? filter(apiKeyList, (key) => some(key.roles, filters))
            : apiKeyList;
        return (React.createElement(Table, { columns: getApikeysTableColumns({
                onCopy: this.onCopy,
                onDelete: this.onDelete,
            }), data: filteredList || [] }));
    }
}
class ApiKeyPage extends React.PureComponent {
    render() {
        const { filters } = this.props;
        const settings = ServerConnection.makeSettings();
        const url = URLExt.join(settings.baseUrl, 'api/api-keys');
        return (React.createElement(React.Fragment, null,
            React.createElement(FetchHoc, { url: url, loadingMessage: "Fetching list of API keys", genericErrorMessage: "Error fetching API keys" }, (apiKeyList) => (React.createElement(ApiKeyComponent, { apiKeyList: apiKeyList, filters: filters })))));
    }
}
export default ApiKeyPage;
const getApikeysTableColumns = ({ onCopy, onDelete }) => [
    {
        Header: 'API key',
        accessor: 'key',
    },
    {
        Header: 'Description',
        accessor: 'description',
    },
    {
        Header: 'Role',
        accessor: 'roles[0].role',
    },
    {
        Header: 'Actions',
        accessor: 'actions',
        Cell: ({ row }) => (React.createElement(React.Fragment, null,
            React.createElement(Button, { "aria-label": "Copy API key", title: "Copy API key", appearance: "stealth", onClick: () => onCopy(row.original.key) },
                React.createElement(FontAwesomeIcon, { icon: faCopy })),
            React.createElement(Button, { "aria-label": "Delete API key", title: "Delete API key", appearance: "stealth", onClick: () => onDelete(row.original.key) },
                React.createElement(FontAwesomeIcon, { icon: faTrash })))),
    },
];
//# sourceMappingURL=api-key-page.js.map