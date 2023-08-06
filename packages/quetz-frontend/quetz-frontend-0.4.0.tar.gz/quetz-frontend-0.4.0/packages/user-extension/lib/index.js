import { Tabs, Tab, TabPanel } from '@jupyter-notebook/react-components';
import { IRouter } from '@jupyterlab/application';
import { DOMUtils, ReactWidget } from '@jupyterlab/apputils';
import { ServerConnection } from '@jupyterlab/services';
import { URLExt } from '@jupyterlab/coreutils';
import { FetchHoc, Breadcrumbs } from '@quetz-frontend/apputils';
import { IMenu } from '@quetz-frontend/menu';
import * as React from 'react';
import UserAPIKey from './api-key';
import UserProfile from './tab-profile';
import UserPackages from './tab-packages';
import UserChannels from './tab-channels';
/**
 * The command ids used by the user plugin.
 */
export var CommandIDs;
(function (CommandIDs) {
    /**
     * Open user page
     */
    CommandIDs.open = '@quetz-frontend/user-extension:open';
    /**
     * Go to user page
     */
    CommandIDs.gotoUser = '@quetz-frontend/user-extension:navigate-to-user';
})(CommandIDs || (CommandIDs = {}));
/**
 * The user plugin.
 */
const plugin = {
    id: '@quetz-frontend/user-extension:plugin',
    autoStart: true,
    requires: [IRouter, IMenu],
    activate: (app, router, menu) => {
        const { shell, commands } = app;
        const connectionSettings = ServerConnection.makeSettings();
        const url = URLExt.join(connectionSettings.baseUrl, '/api/me');
        commands.addCommand(CommandIDs.open, {
            label: 'Open User Panel',
            execute: () => {
                const userWidget = ReactWidget.create(React.createElement(FetchHoc, { url: url, loadingMessage: "Fetching user information", genericErrorMessage: "Error fetching user information" }, (userData) => (React.createElement(UserDetails, { router: router, userData: userData }))));
                userWidget.id = DOMUtils.createDomID();
                userWidget.title.label = 'User main page';
                shell.add(userWidget, 'main');
            },
        });
        commands.addCommand(CommandIDs.gotoUser, {
            label: 'Profile',
            isVisible: () => menu.profile !== null,
            execute: () => {
                router.navigate('/user');
            },
        });
        router.register({
            pattern: /^\/user.*/,
            command: CommandIDs.open,
        });
        menu.addItem({
            command: CommandIDs.gotoUser,
            rank: 501,
        });
    },
};
export default plugin;
var UserTabs;
(function (UserTabs) {
    UserTabs["Profile"] = "profile";
    UserTabs["Channels"] = "channels";
    UserTabs["Packages"] = "packages";
    UserTabs["ApiKeys"] = "api-keys";
})(UserTabs || (UserTabs = {}));
class UserDetails extends React.PureComponent {
    constructor(props) {
        super(props);
        this.setTabId = (selectedTabId) => {
            this.setState({
                selectedTabId,
            });
            const pathFragments = window.location.pathname.split('/');
            if (!Object.values(UserTabs).includes(pathFragments[pathFragments.length - 1])) {
                pathFragments.push(selectedTabId);
            }
            else {
                pathFragments[pathFragments.length - 1] = selectedTabId;
            }
            history.pushState(null, '', pathFragments.join('/'));
        };
        const pathFragments = window.location.pathname.split('/');
        const target = pathFragments.length > 0
            ? pathFragments[pathFragments.length - 1]
            : UserTabs.Profile;
        this.state = {
            selectedTabId: target !== null && target !== void 0 ? target : UserTabs.Profile,
        };
    }
    render() {
        const { selectedTabId } = this.state;
        const { userData } = this.props;
        const breadcrumbItems = [
            {
                text: 'Home',
                onClick: () => {
                    this.props.router.navigate('/');
                },
            },
            {
                text: 'User details',
                onClick: () => {
                    this.props.router.navigate('/user');
                },
            },
            {
                text: selectedTabId,
            },
        ];
        return (React.createElement("div", { className: "page-contents-width-limit" },
            React.createElement(Breadcrumbs, { items: breadcrumbItems }),
            React.createElement("h2", { className: "heading2" }, "User Details"),
            React.createElement(Tabs, { orientation: "vertical", activeid: `user-${selectedTabId}`, onChange: (event) => {
                    this.setTabId(
                    // Remove head `user-`
                    event.target.activeid.slice(5));
                } },
                React.createElement(Tab, { id: "user-profile" }, "Profile"),
                React.createElement(Tab, { id: "user-api-keys" }, "API keys"),
                React.createElement(Tab, { id: "user-channels" }, "Channels"),
                React.createElement(Tab, { id: "user-packages" }, "Packages"),
                React.createElement(TabPanel, null,
                    React.createElement(UserProfile, { userData: userData })),
                React.createElement(TabPanel, null,
                    React.createElement(UserAPIKey, null)),
                React.createElement(TabPanel, null,
                    React.createElement(UserChannels, { username: userData.user.username })),
                React.createElement(TabPanel, null,
                    React.createElement(UserPackages, { username: userData.user.username })))));
    }
}
//# sourceMappingURL=index.js.map