import { SizeProp } from '@fortawesome/fontawesome-svg-core';
import * as React from 'react';
declare type CopyButtonProps = {
    /**
     * Text to copy when clicking the button.
     */
    copyText: string;
    /**
     * Size of the icon as fontawesome SizeProp.
     */
    size?: SizeProp;
};
/**
 * A button to copy a text to clipboard.
 *
 * @param props - The properties of the button, CopyButtonProps type.
 */
declare const CopyButton: (props: CopyButtonProps) => React.ReactElement;
export default CopyButton;
