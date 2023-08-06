import { IRouter } from '@jupyterlab/application';
import * as React from 'react';
interface IChannelsApiItem {
    name: string;
    description: string;
    private: boolean;
    size_limit: null | number;
    mirror_channel_url: null | string;
    mirror_mode: null | string;
    members_count: number;
    packages_count: number;
}
export interface IChannelsListProps {
    router: IRouter;
}
declare type ChannelsAppState = {
    channels: null | IChannelsApiItem[];
    searchText: string;
};
declare class ChannelsList extends React.PureComponent<IChannelsListProps, ChannelsAppState> {
    constructor(props: IChannelsListProps);
    onSearch: (searchText: string) => void;
    render(): JSX.Element;
}
export default ChannelsList;
