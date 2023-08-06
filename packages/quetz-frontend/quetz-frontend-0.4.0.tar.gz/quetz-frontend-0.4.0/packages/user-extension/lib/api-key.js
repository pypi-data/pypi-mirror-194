import { Dialog, showDialog } from '@jupyterlab/apputils';
import { ServerConnection } from '@jupyterlab/services';
import { URLExt } from '@jupyterlab/coreutils';
import { InlineLoader, API_STATUSES, copyToClipboard, } from '@quetz-frontend/apputils';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTrash, faCopy } from '@fortawesome/free-solid-svg-icons';
import * as React from 'react';
import { RequestAPIKeyDialog, APIKeyDialog } from './apiKeyDialog';
import { Button } from '@jupyter-notebook/react-components';
class UserAPIKey extends React.PureComponent {
    constructor(props) {
        super(props);
        this._requestApiKey = async () => {
            const body = new RequestAPIKeyDialog();
            const value = await showDialog({ title: 'Keys', body });
            if (value.button.accept) {
                const data = body.info;
                if (!data.user && data.key.roles.length === 0) {
                    showDialog({
                        title: 'Format error',
                        body: 'Add roles',
                        buttons: [Dialog.okButton()],
                    });
                    return;
                }
                const settings = ServerConnection.makeSettings();
                const url = URLExt.join(settings.baseUrl, '/api/api-keys');
                const request = {
                    method: 'POST',
                    redirect: 'follow',
                    body: JSON.stringify(data.key),
                    headers: { 'Content-Type': 'application/json' },
                };
                const resp = await ServerConnection.makeRequest(url, request, settings);
                const response = await resp.json();
                if (response.detail) {
                    return console.error(response.detail);
                }
                const apiKeys = [...this.state.apiKeys, response];
                this.setState({ apiKeys });
            }
        };
        this._showRoles = async (roles) => {
            const body = new APIKeyDialog(roles);
            showDialog({
                title: 'Roles',
                body,
                buttons: [Dialog.okButton()],
            });
        };
        this._removeAPIKey = async (key) => {
            const body = (React.createElement("label", null,
                "Do you want to delete the API key:",
                ' ',
                React.createElement("label", { className: "qs-Label-Caption" }, key),
                "."));
            const value = await showDialog({
                title: 'Delete API key',
                body,
            });
            if (value.button.accept) {
                const settings = ServerConnection.makeSettings();
                const url = URLExt.join(settings.baseUrl, '/api/api-keys', key);
                const request = {
                    method: 'DELETE',
                    redirect: 'follow',
                };
                const resp = await ServerConnection.makeRequest(url, request, settings);
                if (!resp.ok) {
                    return console.error(resp.statusText);
                }
                const apiKeys = this.state.apiKeys.filter((api) => api.key !== key);
                this.setState({ apiKeys });
            }
        };
        this.state = {
            apiKeys: [],
            apiStatus: API_STATUSES.PENDING,
        };
    }
    async componentDidMount() {
        const settings = ServerConnection.makeSettings();
        const url = URLExt.join(settings.baseUrl, '/api/api-keys');
        const resp = await ServerConnection.makeRequest(url, {}, settings);
        const data = await resp.json();
        if (data.detail) {
            return console.error(data.detail);
        }
        this.setState({
            apiKeys: data,
            apiStatus: API_STATUSES.SUCCESS,
        });
    }
    render() {
        const { apiStatus, apiKeys } = this.state;
        const renderUserKey = () => {
            return apiKeys.map((item) => {
                if (item.roles === null) {
                    return (React.createElement("tr", { key: item.key },
                        React.createElement("td", null, item.key),
                        React.createElement("td", null,
                            React.createElement("label", { className: "qs-Label-Caption" }, item.description)),
                        React.createElement("td", null, item.time_created),
                        React.createElement("td", null, item.expire_at),
                        React.createElement("td", null,
                            React.createElement(Button, { "aria-label": "Copy API key", title: "Copy API key", appearance: "stealth", minimal: true, onClick: () => copyToClipboard(item.key, 'API key') },
                                React.createElement(FontAwesomeIcon, { icon: faCopy })),
                            React.createElement(Button, { "aria-label": "Delete API key", title: "Delete API key", appearance: "stealth", minimal: true, onClick: () => this._removeAPIKey(item.key) },
                                React.createElement(FontAwesomeIcon, { icon: faTrash })))));
                }
            });
        };
        const renderKeys = () => {
            return apiKeys.map((item) => {
                if (item.roles !== null) {
                    return (React.createElement("tr", { key: item.key, className: "qs-clickable-Row" },
                        React.createElement("td", { onClick: () => this._showRoles(item.roles) }, item.key),
                        React.createElement("td", { onClick: () => this._showRoles(item.roles) }, item.description),
                        React.createElement("td", null, item.time_created),
                        React.createElement("td", null, item.expire_at),
                        React.createElement("td", { onClick: () => copyToClipboard(item.key, 'API key') },
                            React.createElement(FontAwesomeIcon, { icon: faCopy })),
                        React.createElement("td", { onClick: () => this._removeAPIKey(item.key) },
                            React.createElement(FontAwesomeIcon, { icon: faTrash }))));
                }
            });
        };
        return (React.createElement("div", null,
            React.createElement("div", { className: "padding-bottom" },
                React.createElement(Button, { appearance: "neutral", onClick: this._requestApiKey }, "Request API key")),
            React.createElement("h3", { className: "heading3" }, "API keys"),
            apiStatus === API_STATUSES.PENDING && (React.createElement(InlineLoader, { text: "Fetching APIKeys" })),
            apiKeys.length !== 0 && (React.createElement("table", { className: "jp-table table-small" },
                React.createElement("thead", null,
                    React.createElement("tr", null,
                        React.createElement("th", null, "Key"),
                        React.createElement("th", null, "Description"),
                        React.createElement("th", null, "Created"),
                        React.createElement("th", null, "Expires"),
                        React.createElement("th", null, "Actions"))),
                React.createElement("tbody", null,
                    renderUserKey(),
                    renderKeys())))));
    }
}
export default UserAPIKey;
//# sourceMappingURL=api-key.js.map