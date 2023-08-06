import { ServerConnection } from '@jupyterlab/services';
import type { ServiceManager, Session, KernelSpec, Setting, Builder, Contents, Terminal, Workspace, NbConvert } from '@jupyterlab/services';
import { ISignal } from '@lumino/signaling';
/**
 * A Quetz services manager
 */
export declare class QuetzServiceManager implements ServiceManager.IManager {
    /**
     * Construct a new services provider
     */
    constructor();
    /**
     * A signal emitted when there is a connection failure with the kernel.
     */
    get connectionFailure(): ISignal<this, Error>;
    /**
     * Test whether the service manager is disposed.
     */
    get isDisposed(): boolean;
    /**
     * The server settings of the manager.
     */
    get serverSettings(): ServerConnection.ISettings;
    /**
     * Get the session manager instance.
     */
    readonly sessions: Session.IManager;
    /**
     * Get the session manager instance.
     */
    readonly kernelspecs: KernelSpec.IManager;
    /**
     * Get the setting manager instance.
     */
    readonly settings: Setting.IManager;
    /**
     * The builder for the manager.
     */
    readonly builder: Builder.IManager;
    /**
     * Get the contents manager instance.
     */
    readonly contents: Contents.IManager;
    /**
     * Get the terminal manager instance.
     */
    readonly terminals: Terminal.IManager;
    /**
     * Get the workspace manager instance.
     */
    readonly workspaces: Workspace.IManager;
    /**
     * Get the nbconvert manager instance.
     */
    readonly nbconvert: NbConvert.IManager;
    /**
     * Test whether the manager is ready.
     */
    get isReady(): boolean;
    /**
     * A promise that fulfills when the manager is ready.
     */
    get ready(): Promise<void>;
    /**
     * Dispose of the resources used by the manager.
     */
    dispose(): void;
    private _isDisposed;
    private _connectionFailure;
}
