import { ITranslator, TranslationManager } from '@jupyterlab/translation';
/**
 * A simplified Translator
 */
export const translator = {
    id: '@quetz-frontend/application-extension:translator',
    autoStart: true,
    provides: ITranslator,
    activate: (app) => {
        const translationManager = new TranslationManager();
        return translationManager;
    },
};
//# sourceMappingURL=translator.js.map