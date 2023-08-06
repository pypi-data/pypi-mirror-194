import { faCopy } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import * as React from 'react';
/**
 * A button to copy a text to clipboard.
 *
 * @param props - The properties of the button, CopyButtonProps type.
 */
const CopyButton = (props) => {
    const [shake, setShake] = React.useState(false);
    /**
     * Animation of the icon when clicked.
     */
    const animate = () => {
        setShake(true);
        setTimeout(() => setShake(false), 1000);
    };
    return (React.createElement(FontAwesomeIcon, { className: 'copy-button' +
            (props.size ? ` fa-${props.size}` : '') +
            (shake ? ' shake' : ''), icon: faCopy, onClick: () => {
            animate();
            navigator.clipboard.writeText(props.copyText);
        } }));
};
export default CopyButton;
//# sourceMappingURL=copy-button.js.map