import { JupyterFrontEnd } from '@jupyterlab/application';
/**
 * The default paths.
 */
export const paths = {
    id: '@quetz-frontend/application-extension:paths',
    autoStart: true,
    provides: JupyterFrontEnd.IPaths,
    activate: (app) => {
        return app.paths;
    },
};
//# sourceMappingURL=paths.js.map