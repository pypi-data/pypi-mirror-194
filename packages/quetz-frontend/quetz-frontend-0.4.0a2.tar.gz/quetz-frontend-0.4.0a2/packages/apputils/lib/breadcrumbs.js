import { Breadcrumb, BreadcrumbItem } from '@jupyter-notebook/react-components';
import * as React from 'react';
export class Breadcrumbs extends React.PureComponent {
    render() {
        const { items } = this.props;
        return (React.createElement(Breadcrumb, null, items.map((item) => item.onClick ? (React.createElement(BreadcrumbItem, { key: item.text },
            React.createElement("a", { onClick: item.onClick }, item.text))) : (React.createElement(BreadcrumbItem, { key: item.text, href: item.href }, item.text)))));
    }
}
//# sourceMappingURL=breadcrumbs.js.map