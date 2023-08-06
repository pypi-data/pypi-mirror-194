import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import * as React from 'react';
import { Button, Search } from '@jupyter-notebook/react-components';
export class SearchBox extends React.PureComponent {
    constructor(props) {
        super(props);
        this._searchRef = React.createRef();
    }
    render() {
        return (React.createElement("form", { onSubmit: (event) => {
                var _a;
                event.preventDefault();
                const value = (_a = this._searchRef.current) === null || _a === void 0 ? void 0 : _a.value;
                if (value) {
                    this.props.onSubmit(value);
                }
            } },
            React.createElement("div", { className: "btn-group quetz-search-box" },
                React.createElement(Search, { ref: this._searchRef, value: this.props.value, placeholder: "Search" }),
                React.createElement(Button, { appearance: "neutral", type: "submit" },
                    React.createElement(FontAwesomeIcon, { icon: faSearch })))));
    }
}
//# sourceMappingURL=search.js.map