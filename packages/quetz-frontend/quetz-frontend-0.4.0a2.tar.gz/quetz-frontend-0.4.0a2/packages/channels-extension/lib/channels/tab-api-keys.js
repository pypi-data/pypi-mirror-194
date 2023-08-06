import * as React from 'react';
import ApiKeyPage from '../components/api-key-page';
class ChannelDetailsApiKeys extends React.PureComponent {
    render() {
        const { channelId } = this.props;
        return (React.createElement("div", { className: "padding" },
            React.createElement(ApiKeyPage, { filters: { channel: channelId } })));
    }
}
export default ChannelDetailsApiKeys;
//# sourceMappingURL=tab-api-keys.js.map