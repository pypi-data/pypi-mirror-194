import { ServerConnection } from '@jupyterlab/services';
import { URLExt } from '@jupyterlab/coreutils';
import { FetchHoc, formatSize } from '@quetz-frontend/apputils';
import { faGlobeAmericas, faUnlockAlt, } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import * as React from 'react';
class ChannelDetailsInfo extends React.PureComponent {
    render() {
        const { channelId } = this.props;
        const settings = ServerConnection.makeSettings();
        const url = URLExt.join(settings.baseUrl, '/api/channels', channelId);
        return (React.createElement(FetchHoc, { url: url, loadingMessage: "Fetching channel information", genericErrorMessage: "Error fetching channel information" }, (channelInfo) => (React.createElement("div", { className: "padding" },
            React.createElement("p", { className: "paragraph" },
                React.createElement(FontAwesomeIcon, { icon: channelInfo.private ? faUnlockAlt : faGlobeAmericas }),
                "\u2003",
                channelInfo.private ? 'Private' : 'Public'),
            React.createElement("p", { className: "caption-inline" }, "Description"),
            React.createElement("p", { className: "paragraph" }, channelInfo.description || React.createElement("i", null, "No description available")),
            React.createElement("p", { className: "caption-inline" }, "Mirror mode"),
            React.createElement("p", { className: "paragraph" }, channelInfo.mirror_mode || React.createElement("i", null, "n/a")),
            React.createElement("p", { className: "caption-inline" }, "Mirror channel URL"),
            React.createElement("p", { className: "paragraph" }, channelInfo.mirror_channel_url || React.createElement("i", null, "n/a")),
            React.createElement("p", { className: "caption-inline" }, "Size limit"),
            React.createElement("p", { className: "paragraph" }, channelInfo.size_limit ? (formatSize(channelInfo.size_limit)) : (React.createElement("i", null, "No size limit")))))));
    }
}
export default ChannelDetailsInfo;
//# sourceMappingURL=tab-info.js.map