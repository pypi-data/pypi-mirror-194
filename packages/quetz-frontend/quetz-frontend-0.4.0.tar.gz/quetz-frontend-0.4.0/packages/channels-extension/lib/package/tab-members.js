import { ServerConnection } from '@jupyterlab/services';
import { URLExt } from '@jupyterlab/coreutils';
import { FetchHoc } from '@quetz-frontend/apputils';
import * as React from 'react';
class PackageMembers extends React.PureComponent {
    render() {
        const { channelId, packageId } = this.props;
        const settings = ServerConnection.makeSettings();
        const url = URLExt.join(settings.baseUrl, '/api/channels', channelId, '/packages', packageId, '/members');
        // TODO use a proper table
        return (React.createElement(FetchHoc, { url: url, loadingMessage: "Fetching list of members", genericErrorMessage: "Error fetching members list" }, (packageMembers) => (React.createElement("div", { className: "package-files-wrapper padding" }, (packageMembers || []).map((member) => (React.createElement("div", { className: "list-row", key: member.user.id },
            React.createElement("div", { className: "member-icon-column" },
                React.createElement("img", { src: member.user.profile.avatar_url, className: "profile-icon", alt: "" })),
            React.createElement("div", { className: "member-name-column" }, member.user.profile.name),
            React.createElement("div", { className: "member-username-column" }, member.user.username),
            React.createElement("div", { className: "member-role-column" }, member.role))))))));
    }
}
export default PackageMembers;
//# sourceMappingURL=tab-members.js.map