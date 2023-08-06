import { IRouter } from '@jupyterlab/application';
import { API_STATUSES } from '@quetz-frontend/apputils';
import * as React from 'react';
import { RouteComponentProps } from 'react-router-dom';
interface IOwner {
    id: string;
    username: string;
    profile: {
        name: string;
        avatar_url: string;
    };
}
interface IJob {
    id: number;
    items_spec: string;
    owner: IOwner;
    created: Date;
    status: string;
    manifest: string;
}
declare type JobState = {
    id: number;
    job: IJob;
    apiStatus: API_STATUSES;
};
export interface IJobProps extends RouteComponentProps {
    router: IRouter;
}
/**
 *
 */
declare class Job extends React.Component<IJobProps, JobState> {
    constructor(props: IJobProps);
    componentDidMount(): Promise<void>;
    render(): JSX.Element;
}
export default Job;
