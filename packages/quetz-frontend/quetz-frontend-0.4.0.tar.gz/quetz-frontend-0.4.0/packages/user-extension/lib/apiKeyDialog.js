import { ServerConnection } from '@jupyterlab/services';
import { URLExt } from '@jupyterlab/coreutils';
import { ReactWidget } from '@jupyterlab/apputils';
import { Button, Checkbox, TextField, } from '@jupyter-notebook/react-components';
import { InlineLoader, API_STATUSES } from '@quetz-frontend/apputils';
import moment from 'moment';
import * as React from 'react';
/**
 * A ReactWidget to edit the dashboard notebook metadata.
 */
export class RequestAPIKeyDialog extends ReactWidget {
    /**
     * Construct a `DashboardMetadataEditor`.
     *
     */
    constructor() {
        super();
        /**
         * Handler for description input changes
         *
         * @param event
         */
        this._handleDescription = (event) => {
            this._api_key_info.description = event.target.value;
            this.update();
        };
        this._handleExpire = (event) => {
            this._api_key_info.expire_at = event.target.value;
            this.update();
        };
        this._handleUserCheck = (event) => {
            this._user_api_key = event.target.checked;
            this.update();
        };
        this._handleChannel = (event) => {
            this._role.channel = event.target.value;
            const channel = this._channels.find((channel) => channel.name === this._role.channel);
            if (channel) {
                switch (channel.role) {
                    case 'owner':
                        this._roles = ['member', 'maintainer', 'owner'];
                        break;
                    case 'maintainer':
                        this._roles = ['member', 'maintainer'];
                        break;
                    case 'member':
                        this._roles = ['member'];
                        break;
                    default:
                        this._roles = [];
                        break;
                }
            }
            else {
                this._roles = [];
            }
            this._packages_channel = this._packages.filter((value) => value.channel_name === this._role.channel);
            this.update();
        };
        this._handlePackage = (event) => {
            this._role.package = event.target.value;
            const pkg = this._packages.find((pkg) => pkg.name === this._role.package);
            if (pkg) {
                switch (pkg.role) {
                    case 'owner':
                        this._roles = ['member', 'maintainer', 'owner'];
                        break;
                    case 'maintainer':
                        this._roles = ['member', 'maintainer'];
                        break;
                    case 'member':
                        this._roles = ['member'];
                        break;
                }
            }
            this.update();
        };
        this._handleRole = (event) => {
            this._role.role = event.target.value;
            this.update();
        };
        /**
         * Handler for adding role to list of roles
         */
        this._addRole = () => {
            this._api_key_info.roles.push(this._role);
            this._role = {
                channel: '',
                package: '',
                role: 'member',
            };
            this._packages_channel = [];
            this.update();
        };
        /**
         * Handler for removing role from list of roles
         *
         * @param index
         */
        this._removeRole = (index) => {
            this._api_key_info.roles.splice(index, 1);
            this.update();
        };
        const expire_at = moment().add(1, 'months').format(moment.HTML5_FMT.DATE);
        this._api_key_info = {
            description: '',
            expire_at,
            roles: [],
        };
        this._username = '';
        this._apiStatus = API_STATUSES.PENDING;
        this._user_api_key = true;
        this._role = {
            channel: '',
            package: '',
            role: 'member',
        };
        this._channels = [];
        this._packages = [];
        this._roles = [];
        this._packages_channel = [];
    }
    get info() {
        if (this._user_api_key) {
            return {
                user: true,
                key: {
                    description: this._api_key_info.description,
                    expire_at: this._api_key_info.expire_at,
                    roles: [],
                },
            };
        }
        else {
            return { user: false, key: this._api_key_info };
        }
    }
    onAfterAttach(message) {
        const settings = ServerConnection.makeSettings();
        const url = URLExt.join(settings.baseUrl, '/api/me');
        ServerConnection.makeRequest(url, {}, settings)
            .then((resp) => {
            return resp.json();
        })
            .then(async (data) => {
            if (data.detail) {
                return console.error(data.detail);
            }
            this._username = data.user.username;
            const urlChannels = URLExt.join(settings.baseUrl, `/api/users/${this._username}/channels`);
            const respChannels = await ServerConnection.makeRequest(urlChannels, {}, settings);
            const channels = await respChannels.json();
            if (channels.detail) {
                console.error(channels.detail);
                this._channels = [];
            }
            else {
                this._channels = channels;
            }
            const urlPackages = URLExt.join(settings.baseUrl, `/api/users/${this._username}/packages`);
            const respPackage = await ServerConnection.makeRequest(urlPackages, {}, settings);
            const packages = await respPackage.json();
            if (packages.detail) {
                console.error(packages.detail);
                this._packages = [];
            }
            else {
                this._packages = packages;
            }
            this._apiStatus = API_STATUSES.SUCCESS;
            this.update();
        });
    }
    render() {
        const renderChannels = () => {
            return (React.createElement("div", { className: "qs-Form-Section" },
                React.createElement("label", { className: "qs-Input-Label" }, "Channel:"),
                React.createElement("input", { name: "channels", type: "search", className: "jp-mod-styled", list: "channels", value: this._role.channel, onChange: this._handleChannel, placeholder: "Select a channel" }),
                React.createElement("datalist", { id: "channels" }, this._channels.map((channel, i) => (React.createElement("option", { key: i, value: channel.name }, channel.name))))));
        };
        const renderPackages = () => {
            return (React.createElement("div", { className: "qs-Form-Section" },
                React.createElement("label", { className: "qs-Input-Label" }, "Package"),
                React.createElement("input", { name: "package", type: "search", className: "jp-mod-styled", list: "packages", value: this._role.package, onChange: this._handlePackage, placeholder: "Leave blank for all packages", disabled: this._role.channel.length === 0 }),
                React.createElement("datalist", { id: "packages" }, this._packages_channel.map((value, i) => (React.createElement("option", { key: i, value: value.name }, value.name))))));
        };
        const renderRoles = () => {
            return (React.createElement("div", { className: "qs-Form-Section" },
                React.createElement("label", { className: "qs-Input-Label" }, "Role"),
                React.createElement("select", { name: "role", className: "jp-mod-styled", value: this._role.role, onChange: this._handleRole }, this._roles.map((role, i) => (React.createElement("option", { key: i, value: role }, role))))));
        };
        const renderTable = () => {
            return (React.createElement("div", { className: "qs-Form-Section" },
                React.createElement("table", { className: "jp-table table-small" },
                    React.createElement("thead", null,
                        React.createElement("tr", null,
                            React.createElement("th", null, "Channel"),
                            React.createElement("th", null, "Package"),
                            React.createElement("th", null, "Role"))),
                    React.createElement("tbody", null, this._api_key_info.roles.map((role, i) => {
                        return (React.createElement("tr", { key: i, className: "qs-clickable-Row", onClick: () => this._removeRole(i) },
                            React.createElement("td", null, role.channel.length !== 0 ? role.channel : '*'),
                            React.createElement("td", null, role.package.length !== 0 ? role.package : '*'),
                            React.createElement("td", null, role.role)));
                    })))));
        };
        return (React.createElement("form", { className: "jp-Input-Dialog" },
            React.createElement("div", { className: "qs-Form-Section" },
                React.createElement("label", { className: "qs-Form-Section-Label" }, "Description"),
                React.createElement(TextField, { name: "description", value: this._api_key_info.description, onChange: this._handleDescription })),
            React.createElement("div", { className: "qs-Form-Section" },
                React.createElement("label", { className: "qs-Form-Section-Label" }, "Expiration date"),
                React.createElement("input", { type: "date", name: "expire_at", className: "jp-mod-styled", min: moment().format(moment.HTML5_FMT.DATE), value: this._api_key_info.expire_at, onChange: this._handleExpire })),
            React.createElement("div", { className: "qs-Form-Section-Row" },
                React.createElement(Checkbox, { id: "user-apiKey", name: "user-apiKey", checked: this._user_api_key, onChange: this._handleUserCheck },
                    "API key with same roles as",
                    ' ',
                    React.createElement("span", { className: "qs-Label-Caption" }, this._username))),
            !this._user_api_key && (React.createElement(React.Fragment, null,
                this._apiStatus === API_STATUSES.PENDING && (React.createElement(InlineLoader, { text: "Fetching user channels and packages" })),
                this._channels.length !== 0 ? (React.createElement(React.Fragment, null,
                    renderChannels(),
                    this._role.channel.length !== 0 ? (React.createElement(React.Fragment, null,
                        this._packages_channel.length !== 0 && renderPackages(),
                        renderRoles(),
                        React.createElement("div", { className: "qs-Form-Section" },
                            React.createElement(Button, { onClick: this._addRole, minimal: true }, "Add role")))) : (React.createElement("label", null, "No packages available")))) : (React.createElement("label", null, "No channels available")),
                this._api_key_info.roles.length !== 0 && renderTable()))));
    }
}
/**
 * A ReactWidget to render a table for APIKeys' roles.
 */
export class APIKeyDialog extends ReactWidget {
    /**
     * Construct a `APIKeyDialog`.
     *
     * @param roles
     */
    constructor(roles) {
        super();
        this._roles = roles;
    }
    render() {
        return (React.createElement("table", { className: "jp-table table-small" },
            React.createElement("thead", null,
                React.createElement("tr", null,
                    React.createElement("th", null, "Channel"),
                    React.createElement("th", null, "Package"),
                    React.createElement("th", null, "Role"))),
            React.createElement("tbody", { className: "qs-scrollable-Table" }, this._roles.map((role, i) => {
                return (React.createElement("tr", { key: i },
                    React.createElement("td", null, role.channel ? role.channel : '*'),
                    React.createElement("td", null, role.package ? role.package : '*'),
                    React.createElement("td", null, role.role ? role.role : '*')));
            }))));
    }
}
//# sourceMappingURL=apiKeyDialog.js.map