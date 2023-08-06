import { QuetzFrontEndPlugin } from '@quetz-frontend/application';
/**
 * The command ids used by the channel plugin.
 */
export declare namespace CommandIDs {
    /**
     * Open channels page
     */
    const open = "@quetz-frontend/channels-extension:open";
    /**
     * Go to channels page
     */
    const gotoChannels = "@quetz-frontend/channels-extension:navigate-to-channels";
}
/**
 * The main plugin.
 */
declare const plugin: QuetzFrontEndPlugin<void>;
export default plugin;
