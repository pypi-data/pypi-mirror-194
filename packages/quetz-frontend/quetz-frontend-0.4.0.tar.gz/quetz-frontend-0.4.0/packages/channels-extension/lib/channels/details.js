import { Tab, TabPanel, Tabs } from '@jupyter-notebook/react-components';
import { Breadcrumbs } from '@quetz-frontend/apputils';
import * as React from 'react';
import { withRouter } from 'react-router-dom';
import ChannelDetailsApiKeys from './tab-api-keys';
import TabInfo from './tab-info';
import ChannelDetailsMembers from './tab-members';
import ChannelDetailsPackages from './tab-packages';
export var ChannelTabs;
(function (ChannelTabs) {
    ChannelTabs["Info"] = "info";
    ChannelTabs["Packages"] = "packages";
    ChannelTabs["Members"] = "members";
    ChannelTabs["ApiKeys"] = "api-keys";
})(ChannelTabs || (ChannelTabs = {}));
class ChannelDetails extends React.PureComponent {
    constructor(props) {
        var _a;
        super(props);
        this.setTabId = (selectedTabId) => {
            this.setState({
                selectedTabId,
            });
            const urlParams = new URLSearchParams(window.location.search);
            urlParams.delete('tab');
            // delete things from pagination
            urlParams.delete('index');
            urlParams.delete('query');
            urlParams.delete('size');
            urlParams.append('tab', selectedTabId);
            history.pushState(null, '', '?' + urlParams.toString());
        };
        const urlParams = new URLSearchParams(window.location.search);
        const currentTab = (_a = urlParams.get('tab')) !== null && _a !== void 0 ? _a : 'info';
        this.state = {
            selectedTabId: currentTab !== null && currentTab !== void 0 ? currentTab : ChannelTabs.Info,
        };
    }
    render() {
        const { selectedTabId: selectedTabIndex } = this.state;
        const { match: { params }, } = this.props;
        const { channelId } = params;
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
            },
        ];
        return (React.createElement(React.Fragment, null,
            React.createElement(Breadcrumbs, { items: breadcrumbItems }),
            React.createElement("h2", { className: "heading2" }, channelId),
            React.createElement(Tabs, { activeid: `channel-${selectedTabIndex}`, onChange: (event) => {
                    const activeID = event.target.activeid;
                    if (typeof activeID === 'string') {
                        this.setTabId(
                        // Remove head `channel-`
                        activeID.slice(8));
                    }
                } },
                React.createElement(Tab, { id: `channel-${ChannelTabs.Info}` }, "Info"),
                React.createElement(Tab, { id: `channel-${ChannelTabs.Packages}` }, "Packages"),
                React.createElement(Tab, { id: `channel-${ChannelTabs.Members}` }, "Members"),
                React.createElement(Tab, { id: `channel-${ChannelTabs.ApiKeys}` }, "API keys"),
                React.createElement(TabPanel, null,
                    React.createElement(TabInfo, { channelId: channelId })),
                React.createElement(TabPanel, null,
                    React.createElement(ChannelDetailsPackages, { channelId: channelId })),
                React.createElement(TabPanel, null,
                    React.createElement(ChannelDetailsMembers, { channelId: channelId })),
                React.createElement(TabPanel, null,
                    React.createElement(ChannelDetailsApiKeys, { channelId: channelId })))));
    }
}
export default withRouter(ChannelDetails);
//# sourceMappingURL=details.js.map