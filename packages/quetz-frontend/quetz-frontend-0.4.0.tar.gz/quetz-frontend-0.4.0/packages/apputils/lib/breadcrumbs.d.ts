import * as React from 'react';
export interface IBreadcrumbsProps {
    items: {
        /**
         * href
         */
        href?: string;
        /**
         * on click callback
         *
         * It will shadow href if defined
         */
        onClick?: (event: React.MouseEvent) => void;
        /**
         * Item content
         */
        text: string;
    }[];
}
export declare class Breadcrumbs extends React.PureComponent<IBreadcrumbsProps> {
    render(): JSX.Element;
}
