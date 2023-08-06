import { ServerConnection } from '@jupyterlab/services';
import { useTable, useFlexLayout, usePagination } from 'react-table';
import clsx from 'clsx';
import * as React from 'react';
import { Pagination } from './pagination';
const headerProps = (props, { column }) => getStyles(props, column.align);
const cellProps = (props, { cell }) => getStyles(props, cell.column.align);
const getStyles = (props, align = 'left') => [
    props,
    {
        style: {
            justifyContent: align === 'right' ? 'flex-end' : 'flex-start',
            alignItems: 'flex-start',
            display: 'flex',
        },
    },
];
export const List = ({ columns: userColumns, data, to, paginated, fetchData, loading, pageCount: controlledPageCount, dataSize, }) => {
    const defaultColumn = {
        width: 150,
    };
    const { getTableProps, headerGroups, prepareRow, 
    // Non-paginated table
    rows, 
    // Paginated table
    page, canPreviousPage, canNextPage, pageOptions, pageCount, gotoPage, nextPage, previousPage, setPageSize, state: { pageIndex, pageSize }, } = useTable({
        columns: userColumns,
        data,
        defaultColumn,
        initialState: { pageIndex: 0 },
        manualPagination: paginated,
        pageCount: controlledPageCount,
    }, useFlexLayout, (hooks) => {
        hooks.allColumns.push((columns) => [...columns]);
    }, ...(paginated ? [usePagination] : []));
    if (paginated) {
        React.useEffect(() => {
            fetchData({ pageIndex, pageSize });
        }, [fetchData, pageIndex, pageSize]);
    }
    // Only show the "Showing 1 to x of y results and arrows if there's more than one page"
    const showPaginationInformation = dataSize > pageSize;
    return (React.createElement(React.Fragment, null,
        React.createElement("div", Object.assign({}, getTableProps(), { className: "table" }),
            React.createElement("div", null, headerGroups.map((headerGroup, key) => (React.createElement("div", Object.assign({}, headerGroup.getHeaderGroupProps({
            // style: { paddingRight: '15px' },
            }), { className: "tr", key: key }), headerGroup.headers.map((column) => (React.createElement("div", Object.assign({}, column.getHeaderProps(headerProps), { className: "th", key: column.id }), column.render('Header')))))))),
            React.createElement("div", { className: "tbody" },
                ((paginated ? page : rows) || []).map((row) => {
                    prepareRow(row);
                    return (React.createElement("div", Object.assign({}, row.getRowProps(), { key: row.id, className: clsx('tr', 'list-row', {
                            clickable: !!to,
                        }), onClick: () => {
                            if (to) {
                                to(row.original);
                            }
                        } }), row.cells.map((cell) => {
                        return (React.createElement("div", Object.assign({}, cell.getCellProps(cellProps), { className: "td", key: cell.column.id }), cell.render('Cell')));
                    })));
                }),
                React.createElement("div", { className: "tr" }, !loading && data.length === 0 && (React.createElement("div", { className: "padding-bottom padding-top" }, "No data available"))))),
        paginated && (React.createElement(Pagination, { pageSize: pageSize, pageCount: pageCount, gotoPage: gotoPage, canPreviousPage: canPreviousPage, previousPage: previousPage, nextPage: nextPage, canNextPage: canNextPage, pageIndex: pageIndex, pageOptions: pageOptions, setPageSize: setPageSize, loading: loading, showPagination: showPaginationInformation }))));
};
export const PaginatedList = ({ url, columns, to, q }) => {
    const [data, setData] = React.useState([]);
    const [loading, setLoading] = React.useState(false);
    const [pageCount, setPageCount] = React.useState(0);
    const [dataSize, setDataSize] = React.useState(0);
    const fetchIdRef = React.useRef(0);
    const fetchData = React.useCallback(async ({ pageSize, pageIndex }) => {
        const fetchId = ++fetchIdRef.current;
        setLoading(true);
        const params = JSON.stringify(Object.assign(Object.assign({}, q), { skip: pageIndex * pageSize, limit: pageSize }));
        const settings = ServerConnection.makeSettings();
        const resp = await ServerConnection.makeRequest(`${url}?${params}`, {}, settings);
        const data = await resp.json();
        if (data && fetchId === fetchIdRef.current) {
            setData(data.result);
            setDataSize(data.pagination.all_records_count);
            setPageCount(Math.ceil(data.pagination.all_records_count / pageSize));
            setLoading(false);
        }
    }, []);
    return (React.createElement(List, { columns: columns, data: data, to: to, paginated: true, fetchData: fetchData, loading: loading, pageCount: pageCount, dataSize: dataSize }));
};
//# sourceMappingURL=list.js.map