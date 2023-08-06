import * as React from 'react';
/**
 * Search box properties
 */
export interface ISearchBoxProps {
    /**
     * Callback on search term submission
     */
    onSubmit: (input: string) => void;
    value: string;
}
export declare class SearchBox extends React.PureComponent<ISearchBoxProps> {
    constructor(props: ISearchBoxProps);
    render(): JSX.Element;
    private _searchRef;
}
