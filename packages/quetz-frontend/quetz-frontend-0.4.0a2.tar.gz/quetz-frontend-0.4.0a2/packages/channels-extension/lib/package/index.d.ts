import { IRouter } from '@jupyterlab/application';
import * as React from 'react';
import { RouteComponentProps } from 'react-router-dom';
export declare enum PackageTabs {
    Info = "info",
    Members = "members",
    ApiKeys = "api-keys"
}
export interface IPackageDetailsState {
    selectedTabId: string;
}
export interface IPackageDetailsProps extends RouteComponentProps {
    router: IRouter;
}
declare class PackageDetails extends React.PureComponent<IPackageDetailsProps, IPackageDetailsState> {
    constructor(props: IPackageDetailsProps);
    setTabId: (selectedTabId: any) => void;
    render(): JSX.Element;
}
declare const _default: React.ComponentClass<Pick<IPackageDetailsProps, "router"> & {
    wrappedComponentRef?: ((instance: PackageDetails | null) => void) | React.RefObject<PackageDetails> | null | undefined;
}, any> & import("react-router").WithRouterStatics<typeof PackageDetails>;
export default _default;
