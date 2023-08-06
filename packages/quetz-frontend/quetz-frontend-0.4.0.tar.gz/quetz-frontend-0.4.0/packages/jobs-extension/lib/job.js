import { URLExt } from '@jupyterlab/coreutils';
import { ServerConnection } from '@jupyterlab/services';
import { API_STATUSES, Breadcrumbs, InlineLoader, } from '@quetz-frontend/apputils';
import * as React from 'react';
import Table from './table';
/**
 *
 */
class Job extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            id: props.match.params.jobId,
            job: {
                id: 0,
                created: new Date(),
                manifest: '',
                owner: { id: '', profile: { name: '', avatar_url: '' }, username: '' },
                items_spec: '',
                status: '',
            },
            apiStatus: API_STATUSES.PENDING,
        };
    }
    async componentDidMount() {
        const settings = ServerConnection.makeSettings();
        const url = URLExt.join(settings.baseUrl, '/api/jobs', this.state.id.toString());
        const resp = await ServerConnection.makeRequest(url, {}, settings);
        const job = await resp.json();
        this.setState({
            job,
            apiStatus: API_STATUSES.SUCCESS,
        });
    }
    render() {
        const { apiStatus, job } = this.state;
        const breadcrumbItems = [
            {
                text: 'Home',
                onClick: () => {
                    this.props.router.navigate('/');
                },
            },
            {
                text: 'Jobs',
                onClick: () => {
                    this.props.router.navigate('/jobs');
                },
            },
            {
                text: 'Job ID',
            },
        ];
        const jobColumns = [
            {
                Header: 'Manifest',
                accessor: 'manifest',
            },
            {
                Header: 'Created',
                accessor: 'created',
            },
            {
                Header: 'Status',
                accessor: 'status',
            },
            {
                Header: 'Owner',
                accessor: 'owner.username',
            },
        ];
        return (React.createElement("div", { className: "page-contents-width-limit" },
            React.createElement(Breadcrumbs, { items: breadcrumbItems }),
            React.createElement("h2", { className: "heading2" }, "Jobs"),
            apiStatus === API_STATUSES.PENDING && (React.createElement(InlineLoader, { text: "Fetching tasks" })),
            React.createElement(Table, { columns: jobColumns, data: job })));
    }
}
export default Job;
//# sourceMappingURL=job.js.map