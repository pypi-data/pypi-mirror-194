import { QuetzFrontEndPlugin } from '@quetz-frontend/application';
/**
 * The command ids used by the user plugin.
 */
export declare namespace CommandIDs {
    /**
     * Open user page
     */
    const open = "@quetz-frontend/user-extension:open";
    /**
     * Go to user page
     */
    const gotoUser = "@quetz-frontend/user-extension:navigate-to-user";
}
/**
 * The user plugin.
 */
declare const plugin: QuetzFrontEndPlugin<void>;
export default plugin;
