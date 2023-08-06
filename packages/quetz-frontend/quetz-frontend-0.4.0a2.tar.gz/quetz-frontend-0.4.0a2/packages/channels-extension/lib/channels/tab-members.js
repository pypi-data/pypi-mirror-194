import { ServerConnection } from '@jupyterlab/services';
import { URLExt } from '@jupyterlab/coreutils';
import { FetchHoc } from '@quetz-frontend/apputils';
import { List } from '@quetz-frontend/table';
import * as React from 'react';
class ChannelDetailsMembers extends React.PureComponent {
    render() {
        const { channelId } = this.props;
        const settings = ServerConnection.makeSettings();
        const url = URLExt.join(settings.baseUrl, '/api/channels', channelId, '/members');
        return (React.createElement(FetchHoc, { url: url, loadingMessage: "Fetching list of members", genericErrorMessage: "Error fetching members" }, (channelMembers) => (React.createElement("div", { className: "padding" },
            React.createElement(List, { columns: getMembersListColumns(), data: channelMembers || [] })))));
    }
}
export default ChannelDetailsMembers;
export const getMembersListColumns = () => [
    {
        Header: '',
        accessor: 'name',
        Cell: ({ row }) => (React.createElement("img", { src: row.original.user.profile.avatar_url, className: "profile-icon", alt: "" })),
        width: 10,
    },
    {
        Header: '',
        accessor: 'user.profile.name',
        width: 40,
    },
    {
        Header: '',
        accessor: 'user.username',
        width: 30,
    },
    {
        Header: '',
        accessor: 'role',
        width: 20,
    },
];
//# sourceMappingURL=tab-members.js.map