import * as React from 'react';
import ApiKeyPage from '../components/api-key-page';
class PackageDetailsApiKeys extends React.PureComponent {
    render() {
        const { channelId, packageId } = this.props;
        return (React.createElement("div", { className: "padding" },
            React.createElement(ApiKeyPage, { filters: { channel: channelId, package: packageId } })));
    }
}
export default PackageDetailsApiKeys;
//# sourceMappingURL=tab-api-keys.js.map