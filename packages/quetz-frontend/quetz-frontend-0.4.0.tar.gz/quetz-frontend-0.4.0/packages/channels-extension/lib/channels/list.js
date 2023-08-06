import { faGlobeAmericas, faUnlockAlt, } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Search, Tooltip } from '@jupyter-notebook/react-components';
import { URLExt } from '@jupyterlab/coreutils';
import { ServerConnection } from '@jupyterlab/services';
import { Breadcrumbs, formatPlural } from '@quetz-frontend/apputils';
import { PaginatedList } from '@quetz-frontend/table';
import * as React from 'react';
class ChannelsList extends React.PureComponent {
    constructor(props) {
        super(props);
        this.onSearch = (searchText) => {
            this.setState({ searchText });
        };
        this.state = {
            channels: null,
            searchText: '',
        };
    }
    render() {
        const { searchText } = this.state;
        const breadcrumbItems = [
            {
                text: 'Home',
                onClick: () => {
                    this.props.router.navigate('/');
                },
            },
            {
                text: 'Channels',
            },
        ];
        const settings = ServerConnection.makeSettings();
        const url = URLExt.join(settings.baseUrl, '/api/paginated/channels');
        return (React.createElement(React.Fragment, null,
            React.createElement(Breadcrumbs, { items: breadcrumbItems }),
            React.createElement("h2", { className: "heading2" }, "Channels"),
            React.createElement(Search, { className: "channels-search", onInput: (event) => {
                    this.onSearch(event.target.value);
                }, placeholder: "Search" }),
            React.createElement(PaginatedList, { url: url, params: { q: searchText }, columns: getChannelsListColumns(), to: (rowData) => {
                    this.props.router.navigate(`/channels/${rowData.name}`);
                } })));
    }
}
export default ChannelsList;
const getChannelsListColumns = () => [
    {
        Header: '',
        accessor: 'name',
        Cell: ({ row }) => {
            const [anchor, setAnchor] = React.useState(null);
            return (React.createElement(React.Fragment, null,
                React.createElement("span", { ref: (element) => {
                        setAnchor(element);
                    } },
                    React.createElement(FontAwesomeIcon, { icon: row.original.private ? faUnlockAlt : faGlobeAmericas })),
                React.createElement(Tooltip, { anchorElement: anchor, position: "right" }, row.original.private ? 'Private' : 'Public')));
        },
        width: 5,
    },
    {
        Header: '',
        accessor: 'user.profile.name',
        Cell: ({ row }) => (React.createElement("div", null,
            React.createElement("p", { className: "text" }, row.original.name),
            React.createElement("p", { className: "minor-paragraph channel-list-description" }, row.original.description))),
        width: 45,
    },
    {
        Header: '',
        accessor: 'user.username',
        Cell: ({ row }) => formatPlural(row.original.packages_count, 'package'),
        width: 35,
    },
    {
        Header: '',
        accessor: 'role',
        Cell: ({ row }) => formatPlural(row.original.members_count, 'member'),
        width: 20,
    },
];
//# sourceMappingURL=list.js.map