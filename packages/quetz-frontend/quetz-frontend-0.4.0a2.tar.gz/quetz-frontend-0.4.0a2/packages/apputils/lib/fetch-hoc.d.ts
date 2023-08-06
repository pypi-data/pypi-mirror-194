import * as React from 'react';
import { API_STATUSES } from './constants';
export interface IFetchHocProps<T> {
    url: string;
    children: (data: T) => React.ReactNode;
    loadingMessage: string;
    genericErrorMessage: string;
}
export interface IFetchHocState {
    data: any | null;
    apiStatus: API_STATUSES;
    error: string;
}
export declare class FetchHoc<T> extends React.PureComponent<IFetchHocProps<T>, IFetchHocState> {
    constructor(props: IFetchHocProps<T>);
    componentDidMount: () => void;
    tryFetch: () => Promise<void>;
    render(): JSX.Element;
}
