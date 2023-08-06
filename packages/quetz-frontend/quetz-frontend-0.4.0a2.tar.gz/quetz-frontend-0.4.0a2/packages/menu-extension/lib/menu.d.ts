import { ReactWidget } from '@jupyterlab/apputils';
import { IRankedMenu, RankedMenu } from '@jupyterlab/ui-components';
import { ISignal } from '@lumino/signaling';
import { QuetzFrontEndPlugin } from '@quetz-frontend/application';
import { IMenu, Profile } from '@quetz-frontend/menu';
import * as React from 'react';
/**
 * The menu plugin.
 */
export declare const menu: QuetzFrontEndPlugin<IMenu>;
/**
 * Main menu
 */
declare class MainMenu extends RankedMenu implements IMenu {
    constructor(options: IRankedMenu.IOptions);
    /**
     * Logged user profile.
     */
    get profile(): Profile | null;
    /**
     * User profile changed signal.
     */
    get profileChanged(): ISignal<IMenu, Profile | null>;
    protected setProfile(v: Profile | null): void;
    private _messageNode;
    private _profile;
    private _profileChanged;
}
/**
 * A concrete implementation of a help menu.
 */
export declare class MenuButton extends ReactWidget {
    private _menu;
    constructor(_menu: MainMenu);
    private _onClick;
    render(): React.ReactElement;
}
export {};
