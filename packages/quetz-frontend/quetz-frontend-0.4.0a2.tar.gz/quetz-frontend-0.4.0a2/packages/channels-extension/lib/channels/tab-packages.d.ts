import { API_STATUSES } from '@quetz-frontend/apputils';
import * as React from 'react';
declare type PackagesState = {
    packages: null | Date;
    apiStatus: API_STATUSES;
};
declare class ChannelDetailsPackages extends React.PureComponent<any, PackagesState> {
    renderRowSubComponent: ({ row }: any) => JSX.Element;
    render(): JSX.Element;
}
export default ChannelDetailsPackages;
export declare const getPackageTableColumns: (channelId: string) => ({
    id: string;
    Header: () => null;
    Cell: ({ row }: any) => any;
    accessor?: undefined;
} | {
    Header: string;
    accessor: string;
    Cell: ({ row }: any) => any;
    id?: undefined;
} | {
    Header: string;
    accessor: string;
    id?: undefined;
    Cell?: undefined;
})[];
