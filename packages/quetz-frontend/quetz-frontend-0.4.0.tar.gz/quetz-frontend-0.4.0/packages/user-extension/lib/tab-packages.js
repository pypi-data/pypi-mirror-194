import { ServerConnection } from '@jupyterlab/services';
import { URLExt } from '@jupyterlab/coreutils';
import { PaginatedTable } from '@quetz-frontend/table';
import * as React from 'react';
class UserPackages extends React.PureComponent {
    render() {
        const { username } = this.props;
        const settings = ServerConnection.makeSettings();
        const url = URLExt.join(settings.baseUrl, '/api/paginated/users', username, '/packages');
        return (React.createElement(React.Fragment, null,
            React.createElement("h3", { className: "heading3" }, "Packages"),
            React.createElement(PaginatedTable, { url: url, columns: getUserChannelsTableColumns(), to: (rowData) => `/${rowData.name}` })));
    }
}
export default UserPackages;
export const getUserChannelsTableColumns = () => [
    {
        Header: 'Name',
        accessor: 'name',
        Cell: ({ row }) => (React.createElement("a", { href: `/channels/${row.original.name}` }, row.original.name)),
    },
    {
        Header: 'Role',
        accessor: 'role',
    },
];
//# sourceMappingURL=tab-packages.js.map