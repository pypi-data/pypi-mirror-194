import * as React from 'react';
class UserProfile extends React.PureComponent {
    render() {
        const { userData } = this.props;
        return (React.createElement(React.Fragment, null,
            React.createElement("h3", { className: "heading3" }, "Profile"),
            React.createElement("p", { className: "caption-inline" }, "Name"),
            React.createElement("p", { className: "paragraph" }, userData.name),
            React.createElement("p", { className: "caption-inline" }, "Username"),
            React.createElement("p", { className: "paragraph" }, userData.user.username),
            React.createElement("p", { className: "caption-inline" }, "Avatar"),
            React.createElement("img", { className: "user-avatar", src: userData.avatar_url, alt: "" })));
    }
}
export default UserProfile;
//# sourceMappingURL=tab-profile.js.map