import { ServerConnection, SettingManager } from '@jupyterlab/services';
import { Signal } from '@lumino/signaling';
/**
 * A Quetz services manager
 */
export class QuetzServiceManager {
    /**
     * Construct a new services provider
     */
    constructor() {
        this._isDisposed = false;
        this._connectionFailure = new Signal(this);
        this.settings = new SettingManager({
            serverSettings: this.serverSettings,
        });
    }
    /**
     * A signal emitted when there is a connection failure with the kernel.
     */
    get connectionFailure() {
        return this._connectionFailure;
    }
    /**
     * Test whether the service manager is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * The server settings of the manager.
     */
    get serverSettings() {
        return ServerConnection.makeSettings();
    }
    /**
     * Test whether the manager is ready.
     */
    get isReady() {
        return true;
    }
    /**
     * A promise that fulfills when the manager is ready.
     */
    get ready() {
        return Promise.resolve();
    }
    /**
     * Dispose of the resources used by the manager.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        Signal.clearData(this);
    }
}
//# sourceMappingURL=servicemanager.js.map