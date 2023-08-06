import { ServerConnection } from '@jupyterlab/services';
import { URLExt } from '@jupyterlab/coreutils';
import { FetchHoc, formatSize } from '@quetz-frontend/apputils';
import { map } from 'lodash';
import fromNow from 'fromnow';
import * as React from 'react';
import { PaginatedTable } from '@quetz-frontend/table';
import CopyButton from '../components/copy-button';
class PackageVersions extends React.PureComponent {
    constructor() {
        super(...arguments);
        this._platforms = {
            linux: {
                faIconName: 'linux',
                operatingSystems: [],
            },
            osx: {
                faIconName: 'apple',
                operatingSystems: [],
            },
            win: {
                faIconName: 'windows',
                operatingSystems: [],
            },
            other: {
                operatingSystems: [],
            },
        };
        /**
         * Include the OS in the list of corresponding platforms.
         *
         * @param os - the os name as string.
         */
        this._fillPlatform = (os) => {
            const pf = os.split('-')[0];
            const pfKey = (pf in this._platforms ? pf : 'other');
            const newPlatform = this._platforms[pfKey].operatingSystems.length == 0;
            if (!this._platforms[pfKey].operatingSystems.includes(os)) {
                this._platforms[pfKey].operatingSystems.push(os);
            }
            return newPlatform;
        };
        /**
         * Format the platform icon and the list of OS.
         *
         * @param platform - the platform name as string.
         */
        this._formatPlatform = (platform) => {
            const pfKey = (platform in this._platforms ? platform : 'other');
            return (React.createElement("div", null,
                React.createElement("div", { className: "package-files-row" },
                    'faIconName' in this._platforms[pfKey] && (React.createElement("i", { className: `fa fa-${this._platforms[pfKey].faIconName} fa-3x` })),
                    React.createElement("span", { className: "package-platform-list" }, this._platforms[pfKey].operatingSystems.map((platform, index) => (React.createElement("p", { key: `${platform}_${index}` }, platform)))))));
        };
    }
    render() {
        const { channel, selectedPackage } = this.props;
        const settings = ServerConnection.makeSettings();
        const url = URLExt.join(settings.baseUrl, '/api/paginated/channels', channel, '/packages', selectedPackage, '/versions');
        return (React.createElement(FetchHoc, { url: url, loadingMessage: `Loading versions in ${selectedPackage}`, genericErrorMessage: "Error fetching package versions information" }, (versionData) => {
            if (versionData.result.length === 0) {
                return React.createElement("div", null, "No versions available for the package");
            }
            const lastVersionsData = [];
            versionData.result.forEach((version) => {
                const newPlatform = this._fillPlatform(version.platform);
                if (newPlatform) {
                    lastVersionsData.push(version);
                }
            });
            return (React.createElement(React.Fragment, null,
                React.createElement("div", { className: "package-row-flex" }, lastVersionsData.map((version) => {
                    const info = version.info;
                    return (React.createElement("div", { key: `${info.platform}_${info.version}`, className: "platform-item" },
                        this._formatPlatform(info.platform),
                        React.createElement("h4", { className: "section-heading" }, "Package Info"),
                        React.createElement("p", { className: "minor-paragraph" },
                            React.createElement("b", null, "Arch"),
                            ": ",
                            info.arch || 'n/a',
                            React.createElement("br", null),
                            React.createElement("b", null, "Build"),
                            ": ",
                            info.build || 'n/a',
                            React.createElement("br", null),
                            React.createElement("b", null, "MD5"),
                            ": ",
                            info.md5,
                            ' ',
                            React.createElement(CopyButton, { copyText: info.md5 }),
                            React.createElement("br", null),
                            React.createElement("b", null, "Platform"),
                            ": ",
                            version.platform,
                            React.createElement("br", null),
                            React.createElement("b", null, "Latest version"),
                            ": ",
                            info.version),
                        React.createElement("h4", { className: "section-heading" }, "Dependencies"),
                        React.createElement("p", { className: "minor-paragraph" }, map(info.depends, (dep, key) => {
                            return (React.createElement("span", { key: `${info.arch}_${key}`, className: "tag" }, dep));
                        }))));
                })),
                React.createElement("h4", { className: "section-heading" }, "Install"),
                React.createElement("div", { className: "minor-paragraph package-install-command" },
                    React.createElement("pre", null,
                        "mamba install -c ",
                        channel,
                        " ",
                        selectedPackage),
                    React.createElement(CopyButton, { copyText: `mamba install -c ${channel} ${selectedPackage}`, size: "lg" })),
                this.props.showVersionsList && (React.createElement(React.Fragment, null,
                    React.createElement("h4", { className: "section-heading" }, "History"),
                    React.createElement(PaginatedTable, { url: url, enableSearch: false, columns: getVersionTableColumns(settings.baseUrl) })))));
        }));
    }
}
export default PackageVersions;
export const getVersionTableColumns = (baseURL) => [
    {
        Header: 'Uploader',
        accessor: 'uploader.name',
        Cell: ({ row }) => row.values['uploader.name'],
    },
    {
        Header: 'Date',
        accessor: 'time_created',
        Cell: ({ row }) => fromNow(row.values.time_created, {
            max: 1,
            suffix: true,
        }),
    },
    {
        Header: 'Filename',
        accessor: 'filename',
        Cell: ({ row }) => {
            return (React.createElement("a", { href: URLExt.join(baseURL, `/get/${row.original.channel_name}/${row.original.info.subdir}/${row.values.filename}`), download: true }, row.values.filename));
        },
    },
    {
        Header: 'Platform',
        accessor: 'info.platform',
        Cell: ({ row }) => {
            const platform = row.values['info.platform'];
            return platform === 'linux' ? (React.createElement("i", { className: "fa fa-linux fa-2x" })) : platform === 'osx' ? (React.createElement("i", { className: "fa fa-apple fa-2x" })) : platform === 'win' ? (React.createElement("i", { className: "fa fa-windows fa-2x" })) : (React.createElement("div", { className: "package-platform-noarch" },
                React.createElement("i", { className: "fa fa-linux" }),
                React.createElement("i", { className: "fa fa-apple" }),
                React.createElement("i", { className: "fa fa-windows" })));
        },
    },
    {
        Header: 'Size',
        accessor: 'info.size',
        Cell: ({ row }) => formatSize(row.values['info.size']),
    },
    {
        Header: 'Version',
        accessor: 'version',
        Cell: ({ row }) => row.values.version,
    },
];
//# sourceMappingURL=versions.js.map