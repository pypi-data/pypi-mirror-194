import * as React from 'react';
import 'regenerator-runtime/runtime';
interface ITableFcProps {
    columns: any;
    data: any;
    dataSize?: any;
    fetchData?: any;
    renderRowSubComponent?: any;
    loading?: any;
    paginated?: undefined | boolean;
    pageIndex?: number;
    pageSize?: number;
    pageCount?: any;
    enableSearch?: boolean;
    query?: string;
}
export declare const Table: React.FC<ITableFcProps>;
export declare const PaginatedTable: ({ url, columns, renderRowSubComponent, enableSearch, }: any) => JSX.Element;
export {};
