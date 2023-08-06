import { API_STATUSES } from '@quetz-frontend/apputils';
import * as React from 'react';
import { Column } from 'react-table';
declare type PackageVersionProps = {
    channel: string;
    selectedPackage: string;
    showVersionsList?: boolean;
};
declare type PackageVersionsState = {
    versionData: null | any;
    apiStatus: API_STATUSES;
};
declare class PackageVersions extends React.PureComponent<PackageVersionProps, PackageVersionsState> {
    private _platforms;
    /**
     * Include the OS in the list of corresponding platforms.
     *
     * @param os - the os name as string.
     */
    private _fillPlatform;
    /**
     * Format the platform icon and the list of OS.
     *
     * @param platform - the platform name as string.
     */
    private _formatPlatform;
    render(): React.ReactElement;
}
export default PackageVersions;
export declare const getVersionTableColumns: (baseURL: string) => ReadonlyArray<Column>;
