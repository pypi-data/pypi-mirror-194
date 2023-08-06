import { API_STATUSES } from '@quetz-frontend/apputils';
import * as React from 'react';
import { APIKey } from './types';
declare type APIKeyState = {
    apiKeys: APIKey[];
    apiStatus: API_STATUSES;
};
declare class UserAPIKey extends React.PureComponent<any, APIKeyState> {
    constructor(props: any);
    componentDidMount(): Promise<void>;
    private _requestApiKey;
    private _showRoles;
    private _removeAPIKey;
    render(): JSX.Element;
}
export default UserAPIKey;
