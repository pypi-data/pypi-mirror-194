import { Router, IRouter } from '@jupyterlab/application';
export const router = {
    id: '@quetz-frontend/application-extension:router',
    autoStart: true,
    provides: IRouter,
    activate: (app) => {
        const { commands } = app;
        const router = new Router({ base: '/', commands });
        void app.started.then(() => {
            void router.route();
            // Route all pop state events.
            window.addEventListener('popstate', () => {
                void router.route();
            });
        });
        return router;
    },
};
//# sourceMappingURL=router.js.map