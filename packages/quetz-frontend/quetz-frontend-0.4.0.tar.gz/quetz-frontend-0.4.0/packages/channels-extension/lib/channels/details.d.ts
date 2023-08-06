import { IRouter } from '@jupyterlab/application';
import * as React from 'react';
import { RouteComponentProps } from 'react-router-dom';
export declare enum ChannelTabs {
    Info = "info",
    Packages = "packages",
    Members = "members",
    ApiKeys = "api-keys"
}
export interface IChannelDetailsState {
    selectedTabId: string;
}
export interface IChannelDetailProps extends RouteComponentProps {
    router: IRouter;
}
declare class ChannelDetails extends React.PureComponent<IChannelDetailProps, IChannelDetailsState> {
    constructor(props: IChannelDetailProps);
    setTabId: (selectedTabId: string) => void;
    render(): JSX.Element;
}
declare const _default: React.ComponentClass<Pick<IChannelDetailProps, "router"> & {
    wrappedComponentRef?: ((instance: ChannelDetails | null) => void) | React.RefObject<ChannelDetails> | null | undefined;
}, any> & import("react-router").WithRouterStatics<typeof ChannelDetails>;
export default _default;
