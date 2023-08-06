import { QuetzFrontEndPlugin } from '@quetz-frontend/application';
/**
 * The command ids used by the main plugin.
 */
export declare namespace CommandIDs {
    /**
     * Open jobs widget
     */
    const jobs = "@quetz-frontend/jobs-extensions:open";
    /**
     * Go to jobs page
     */
    const goToJobs = "@quetz-frontend/jobs-extensions:navigate-to-jobs";
}
/**
 * The main menu plugin.
 */
declare const plugin: QuetzFrontEndPlugin<void>;
export default plugin;
