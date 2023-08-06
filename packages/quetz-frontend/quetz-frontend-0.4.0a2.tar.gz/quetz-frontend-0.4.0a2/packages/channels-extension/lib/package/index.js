import { Tab, TabPanel, Tabs } from '@jupyter-notebook/react-components';
import { Breadcrumbs } from '@quetz-frontend/apputils';
import * as React from 'react';
import { withRouter } from 'react-router-dom';
import PackageDetailsApiKeys from './tab-api-keys';
import PackageInfo from './tab-info';
import PackageMembers from './tab-members';
export var PackageTabs;
(function (PackageTabs) {
    PackageTabs["Info"] = "info";
    PackageTabs["Members"] = "members";
    PackageTabs["ApiKeys"] = "api-keys";
})(PackageTabs || (PackageTabs = {}));
class PackageDetails extends React.PureComponent {
    constructor(props) {
        super(props);
        this.setTabId = (selectedTabId) => {
            this.setState({
                selectedTabId,
            });
            history.pushState(null, '', `#${selectedTabId}`);
        };
        const locationHash = (window.location.hash || `#${PackageTabs.Info}`).substring(1);
        this.state = {
            selectedTabId: locationHash !== null && locationHash !== void 0 ? locationHash : PackageTabs.Info,
        };
    }
    render() {
        const { selectedTabId } = this.state;
        const { match: { params }, } = this.props;
        const { channelId, packageId } = params;
        const breadcrumbItems = [
            {
                text: 'Home',
                onClick: () => {
                    this.props.router.navigate('/');
                },
            },
            {
                text: 'Channels',
                onClick: () => {
                    this.props.router.navigate('/channels');
                },
            },
            {
                text: channelId,
                onClick: () => {
                    this.props.router.navigate(`/channels/${channelId}`);
                },
            },
            {
                text: 'packages',
                onClick: () => {
                    this.props.router.navigate(`/channels/${channelId}?tab=packages`);
                },
            },
            {
                text: packageId,
            },
        ];
        return (React.createElement("div", null,
            React.createElement(Breadcrumbs, { items: breadcrumbItems }),
            React.createElement("h2", { className: "heading2" },
                channelId,
                "/",
                packageId),
            React.createElement(Tabs, { activeid: `package-${selectedTabId}`, onChange: (event) => {
                    this.setTabId(
                    // Remove head `package-`
                    event.target.activeid.slice(8));
                } },
                React.createElement(Tab, { id: `package-${PackageTabs.Info}` }, "Info"),
                React.createElement(Tab, { id: `package-${PackageTabs.Members}` }, "Members"),
                React.createElement(Tab, { id: `package-${PackageTabs.ApiKeys}` }, "API keys"),
                React.createElement(TabPanel, null,
                    React.createElement(PackageInfo, null)),
                React.createElement(TabPanel, null,
                    React.createElement(PackageMembers, { channelId: channelId, packageId: packageId })),
                React.createElement(TabPanel, null,
                    React.createElement(PackageDetailsApiKeys, { channelId: channelId, packageId: packageId })))));
    }
}
export default withRouter(PackageDetails);
//# sourceMappingURL=index.js.map