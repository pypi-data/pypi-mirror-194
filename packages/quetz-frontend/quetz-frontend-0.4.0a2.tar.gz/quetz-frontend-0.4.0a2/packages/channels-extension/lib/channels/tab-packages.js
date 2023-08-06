import { ServerConnection } from '@jupyterlab/services';
import { URLExt } from '@jupyterlab/coreutils';
import { PaginatedTable } from '@quetz-frontend/table';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faAngleDown, faAngleRight } from '@fortawesome/free-solid-svg-icons';
import { Link } from 'react-router-dom';
import * as React from 'react';
import PackageVersions from '../package/versions';
class ChannelDetailsPackages extends React.PureComponent {
    constructor() {
        super(...arguments);
        this.renderRowSubComponent = ({ row }) => {
            const { channelId } = this.props;
            const packageName = row.values.name;
            return (React.createElement(PackageVersions, { selectedPackage: packageName, channel: channelId }));
        };
    }
    render() {
        const { channelId } = this.props;
        const settings = ServerConnection.makeSettings();
        const url = URLExt.join(settings.baseUrl, '/api/paginated/channels', channelId, '/packages');
        return (React.createElement(PaginatedTable, { url: url, enableSearch: true, columns: getPackageTableColumns(channelId), renderRowSubComponent: this.renderRowSubComponent }));
    }
}
export default ChannelDetailsPackages;
export const getPackageTableColumns = (channelId) => [
    {
        id: 'expander',
        Header: () => null,
        Cell: ({ row }) => (React.createElement("span", Object.assign({}, row.getToggleRowExpandedProps({
            style: {
                paddingLeft: `${row.depth * 2}rem`,
            },
        })),
            React.createElement(FontAwesomeIcon, { icon: row.isExpanded ? faAngleDown : faAngleRight }))),
    },
    {
        Header: 'Name',
        accessor: 'name',
        Cell: ({ row }) => (React.createElement(Link, { to: `${channelId}/packages/${row.values.name}` }, row.values.name)),
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
//# sourceMappingURL=tab-packages.js.map