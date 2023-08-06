import { Avatar, Button } from '@jupyter-notebook/react-components';
import { IRouter } from '@jupyterlab/application';
import { ReactWidget, UseSignal } from '@jupyterlab/apputils';
import { MenuSvg, RankedMenu } from '@jupyterlab/ui-components';
import { JSONExt } from '@lumino/coreutils';
import { Signal } from '@lumino/signaling';
import { IMenu } from '@quetz-frontend/menu';
import * as React from 'react';
import { avatarIcon, hamburgerIcon } from './icons';
var CommandIDs;
(function (CommandIDs) {
    /**
     * Logout the current user
     */
    CommandIDs.logout = '@quetz-frontend/menu-extension:logout';
})(CommandIDs || (CommandIDs = {}));
/**
 * The menu plugin.
 */
export const menu = {
    id: '@quetz-frontend/menu-extension:menu',
    autoStart: true,
    requires: [IRouter],
    provides: IMenu,
    activate: activateMenu,
};
/**
 * Main menu
 */
class MainMenu extends RankedMenu {
    constructor(options) {
        super(options);
        this._profile = null;
        this._profileChanged = new Signal(this);
        // Insert fake separator after sign in message
        this.node.insertAdjacentHTML('afterbegin', '<div class="lm-Menu-item" data-type="separator" style="display: inline;"><div></div></div>');
        this._messageNode = document.createElement('span');
        this._messageNode.textContent = 'Not signed in';
        this.node.insertAdjacentElement('afterbegin', this._messageNode);
        (async () => {
            const config_data = document.getElementById('jupyter-config-data');
            if (config_data) {
                try {
                    const data = JSON.parse(config_data.innerHTML);
                    if (data.detail) {
                        console.error(data.detail);
                        return;
                    }
                    if (data.logged_in_user_profile) {
                        this.setProfile(JSON.parse(data.logged_in_user_profile));
                    }
                    else {
                        try {
                            const response = await fetch('/api/me');
                            const payload = await response.json();
                            if (payload.detail) {
                                console.error(payload.detail);
                            }
                            else {
                                this.setProfile(payload);
                            }
                        }
                        catch (reason) {
                            console.error('Fail to get user profile.', reason);
                        }
                    }
                }
                catch (e) {
                    console.log("Couldn't parse configuration object.", e);
                }
            }
        })();
    }
    /**
     * Logged user profile.
     */
    get profile() {
        return this._profile;
    }
    /**
     * User profile changed signal.
     */
    get profileChanged() {
        return this._profileChanged;
    }
    setProfile(v) {
        if (!JSONExt.deepEqual(this.profile, v)) {
            this._profile = v;
            this._messageNode.textContent = this.profile
                ? `Signed in as ${this.profile.user.username}`
                : 'Not signed in';
            this._profileChanged.emit(this.profile);
        }
    }
}
/**
 * A concrete implementation of a help menu.
 */
export class MenuButton extends ReactWidget {
    constructor(_menu) {
        super();
        this._menu = _menu;
        this._onClick = () => {
            const { left, bottom } = this.node.getBoundingClientRect();
            this._menu.open(left, bottom, { forceY: true });
        };
        this.id = 'login-menu';
        this.addClass('topbar-item');
    }
    render() {
        return (React.createElement(UseSignal, { signal: this._menu.profileChanged }, () => {
            var _a;
            const isAnonymous = !this._menu.profile;
            const profile = (_a = this._menu.profile) !== null && _a !== void 0 ? _a : {
                name: 'Anonymous',
                avatar_url: '',
            };
            // block default avatar from showing invalid image for dummy users
            if (profile.avatar_url == '/avatar.jpg') {
                profile.avatar_url = '';
            }
            return (React.createElement("div", null,
                React.createElement(Button
                // appearance="stealth"
                , { "aria-label": `User Menu: ${profile.name}`, onClick: this._onClick, className: "hamburger-menu-button" }, isAnonymous ? (React.createElement("div", { style: { display: 'flex', alignItems: 'center' } },
                    React.createElement(avatarIcon.react, { className: "anonymous-icon", tag: "span", width: "28px", height: "28px" }),
                    React.createElement("span", { className: "hamburger-menu-text" }, "Login"),
                    React.createElement(hamburgerIcon.react, { className: "hamburger-icon", tag: "span" }))) : (React.createElement("div", { style: { display: 'flex', alignItems: 'center' } },
                    React.createElement(Avatar, { src: profile.avatar_url, shape: "circle", alt: `${profile.name.slice(0, 2).toLocaleUpperCase()}`, style: { width: '28px', height: '28px' } }),
                    React.createElement("span", { className: "hamburger-menu-text" }, "Menu"),
                    React.createElement(hamburgerIcon.react, { className: "hamburger-icon", tag: "span" }))))));
        }));
    }
}
/**
 * @param app Application object
 * @returns The application menu object
 */
function activateMenu(app) {
    // Add menu
    const menu = new MainMenu({
        commands: app.commands,
        renderer: MenuSvg.defaultRenderer,
    });
    menu.addClass('quetz-main-menu');
    const menuButton = new MenuButton(menu);
    app.commands.addCommand(CommandIDs.logout, {
        label: 'Sign out',
        isVisible: () => menu.profile !== null,
        execute: () => {
            window.location.href = '/auth/logout';
        },
    });
    app.shell.add(menuButton, 'top', { rank: 100 });
    menu.addItem({ type: 'separator', rank: 500 });
    menu.addItem({ type: 'separator', rank: 1000 });
    menu.addItem({
        command: CommandIDs.logout,
        rank: 1001,
    });
    return menu;
}
//# sourceMappingURL=menu.js.map