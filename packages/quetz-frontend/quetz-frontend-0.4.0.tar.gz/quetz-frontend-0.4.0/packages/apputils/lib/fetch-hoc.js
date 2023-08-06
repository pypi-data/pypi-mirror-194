import { Button } from '@jupyter-notebook/react-components';
import { ServerConnection } from '@jupyterlab/services';
import * as React from 'react';
import { API_STATUSES } from './constants';
import { InlineLoader } from './loader';
export class FetchHoc extends React.PureComponent {
    constructor(props) {
        super(props);
        this.componentDidMount = () => {
            this.tryFetch();
        };
        this.tryFetch = async () => {
            const { url } = this.props;
            this.setState({
                apiStatus: API_STATUSES.PENDING,
            });
            const settings = ServerConnection.makeSettings();
            const resp = await ServerConnection.makeRequest(url, {}, settings);
            if (!resp.ok) {
                this.setState({
                    error: resp.statusText,
                    apiStatus: API_STATUSES.FAILED,
                });
            }
            else {
                this.setState({
                    data: await resp.json(),
                    apiStatus: API_STATUSES.SUCCESS,
                });
            }
        };
        this.state = {
            data: null,
            apiStatus: API_STATUSES.PENDING,
            error: '',
        };
    }
    render() {
        const { apiStatus, data, error } = this.state;
        const { children, loadingMessage, genericErrorMessage } = this.props;
        if (apiStatus === API_STATUSES.PENDING) {
            return React.createElement(InlineLoader, { text: loadingMessage });
        }
        if (apiStatus === API_STATUSES.FAILED) {
            return (React.createElement("p", { className: "paragraph padding error-message" },
                error || genericErrorMessage || 'Error occurred while fetching data',
                "\u2003",
                React.createElement(Button, { appearance: "lightweight", onClick: this.tryFetch }, "Try again")));
        }
        return React.createElement(React.Fragment, null, children(data));
    }
}
//# sourceMappingURL=fetch-hoc.js.map