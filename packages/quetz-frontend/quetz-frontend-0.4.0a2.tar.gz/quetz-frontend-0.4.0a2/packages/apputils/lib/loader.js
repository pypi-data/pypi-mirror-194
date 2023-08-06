import { ProgressRing } from '@jupyter-notebook/react-components';
import * as React from 'react';
export class InlineLoader extends React.PureComponent {
    render() {
        const { text } = this.props;
        return (React.createElement("div", { className: "loader-wrapper padding" },
            React.createElement(ProgressRing, null),
            text && React.createElement("p", { className: "text loader-text" }, text)));
    }
}
//# sourceMappingURL=loader.js.map