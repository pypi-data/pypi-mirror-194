import { ServerConnection } from '@jupyterlab/services';
import { URLExt } from '@jupyterlab/coreutils';
import { FetchHoc } from '@quetz-frontend/apputils';
import { withRouter } from 'react-router-dom';
import * as React from 'react';
import PackageVersions from './versions';
class PackageMainContent extends React.PureComponent {
    render() {
        const { match: { params: { packageId, channelId }, }, } = this.props;
        const settings = ServerConnection.makeSettings();
        const url = URLExt.join(settings.baseUrl, '/api/channels', channelId, '/packages', packageId);
        return (React.createElement("div", { className: "padding jp-table" },
            React.createElement(FetchHoc, { url: url, loadingMessage: "Fetching package information", genericErrorMessage: "Error fetching package information" }, (packageData) => (React.createElement(React.Fragment, null,
                React.createElement("h4", { className: "section-heading" }, "Summary"),
                React.createElement("p", { className: "minor-paragraph" }, packageData.summary || React.createElement("i", null, "n/a")),
                React.createElement("h4", { className: "section-heading" }, "Description"),
                React.createElement("p", { className: "minor-paragraph" }, packageData.description || React.createElement("i", null, "n/a")),
                React.createElement(PackageVersions, { selectedPackage: packageId, channel: channelId, showVersionsList: true }))))));
    }
}
export default withRouter(PackageMainContent);
//# sourceMappingURL=tab-info.js.map