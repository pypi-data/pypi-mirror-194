/// <reference types="react" />
import { Dialog, ReactWidget } from '@jupyterlab/apputils';
import { Message } from '@lumino/messaging';
import { APIKeyInfo, Role } from './types';
/**
 * A ReactWidget to edit the dashboard notebook metadata.
 */
export declare class RequestAPIKeyDialog extends ReactWidget implements Dialog.IBodyWidget<ReactWidget> {
    /**
     * Construct a `DashboardMetadataEditor`.
     *
     */
    constructor();
    get info(): {
        user: boolean;
        key: APIKeyInfo;
    };
    onAfterAttach(message: Message): void;
    /**
     * Handler for description input changes
     *
     * @param event
     */
    private _handleDescription;
    private _handleExpire;
    private _handleUserCheck;
    private _handleChannel;
    private _handlePackage;
    private _handleRole;
    /**
     * Handler for adding role to list of roles
     */
    private _addRole;
    /**
     * Handler for removing role from list of roles
     *
     * @param index
     */
    private _removeRole;
    render(): JSX.Element;
    private _api_key_info;
    private _username;
    private _apiStatus;
    private _user_api_key;
    private _role;
    private _channels;
    private _packages;
    private _packages_channel;
    private _roles;
}
/**
 * A ReactWidget to render a table for APIKeys' roles.
 */
export declare class APIKeyDialog extends ReactWidget implements Dialog.IBodyWidget<ReactWidget> {
    /**
     * Construct a `APIKeyDialog`.
     *
     * @param roles
     */
    constructor(roles: Role[]);
    render(): JSX.Element;
    private _roles;
}
