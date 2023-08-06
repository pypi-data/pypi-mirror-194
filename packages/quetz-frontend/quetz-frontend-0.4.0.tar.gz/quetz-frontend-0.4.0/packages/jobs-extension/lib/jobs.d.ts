/// <reference types="react" />
import { ReactWidget } from '@jupyterlab/apputils';
import { IRouter } from '@jupyterlab/application';
/**
 *
 */
export declare class Jobs extends ReactWidget {
    private _router;
    constructor(_router: IRouter);
    _loadData(): void;
    render(): JSX.Element;
    private _data;
    private _status;
}
