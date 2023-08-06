import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTimes, faCheckCircle, faTimesCircle, faInfoCircle, faExclamationCircle, } from '@fortawesome/free-solid-svg-icons';
import clsx from 'clsx';
import { Store } from 'react-notifications-component';
import * as React from 'react';
export const NOTIFICATION_TYPES = {
    SUCCESS: 'success',
    DANGER: 'danger',
    INFO: 'info',
    DEFAULT: 'default',
    WARNING: 'warning',
};
const NOTIFICATION_ICONS = {
    [NOTIFICATION_TYPES.SUCCESS]: faCheckCircle,
    [NOTIFICATION_TYPES.DANGER]: faTimesCircle,
    [NOTIFICATION_TYPES.INFO]: faInfoCircle,
    [NOTIFICATION_TYPES.DEFAULT]: faInfoCircle,
    [NOTIFICATION_TYPES.WARNING]: faExclamationCircle,
};
class NotificationComponent extends React.PureComponent {
    render() {
        const { id, type, title, message } = this.props;
        return (React.createElement("div", { className: "notification-item" },
            React.createElement("p", { className: clsx('notification-icon', type) },
                React.createElement(FontAwesomeIcon, { icon: NOTIFICATION_ICONS[type] })),
            React.createElement("div", { className: "notification-content" },
                title && React.createElement("p", { className: clsx('notification-title', type) }, title),
                message && React.createElement("p", { className: "notification-message" }, message)),
            React.createElement("button", { className: "notification-close" },
                React.createElement(FontAwesomeIcon, { icon: faTimes, onClick: () => Store.removeNotification(id) }))));
    }
}
export const sendNotification = ({ type = NOTIFICATION_TYPES.DEFAULT, title, message, duration, }) => {
    const notifId = Store.addNotification({
        content: ({ id }) => (React.createElement(NotificationComponent, { id: id, title: title, type: type, message: message })),
        insert: 'top',
        container: 'top-right',
        animationIn: ['animate__animated', 'animate__fadeIn'],
        animationOut: ['animate__animated', 'animate__fadeOut'],
        dismiss: {
            duration,
        },
    });
    // TODO: Find out why the notifiaction is not automatically disappearing
    if (duration) {
        setTimeout(() => {
            Store.removeNotification(notifId);
        }, duration);
    }
};
//# sourceMappingURL=notification.js.map