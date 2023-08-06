import { useExpanded, useTable } from 'react-table';
import * as React from 'react';
import 'regenerator-runtime/runtime';
const Table = ({ columns: userColumns, data, renderRowSubComponent, }) => {
    const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = useTable({
        columns: userColumns,
        data,
    }, useExpanded);
    return (React.createElement("table", Object.assign({}, getTableProps(), { className: "jp-table" }),
        React.createElement("thead", null, headerGroups.map((headerGroup) => (React.createElement("tr", Object.assign({}, headerGroup.getHeaderGroupProps(), { key: headerGroup.id }), headerGroup.headers.map((column) => (React.createElement("th", Object.assign({}, column.getHeaderProps(), { key: column.id }), column.render('Header')))))))),
        React.createElement("tbody", Object.assign({}, getTableBodyProps()), rows.map((row, i) => {
            prepareRow(row);
            return (React.createElement(React.Fragment, null,
                React.createElement("tr", Object.assign({}, row.getRowProps(), { key: row.id, "data-status": row.values.status }), row.cells.map((cell) => {
                    return (React.createElement("td", Object.assign({}, cell.getCellProps(), { key: row.id }), cell.render('Cell')));
                })),
                row.isExpanded ? (React.createElement("tr", null,
                    React.createElement("td", { colSpan: 5 }, renderRowSubComponent({ row })))) : null));
        }))));
};
export default Table;
//# sourceMappingURL=table.js.map