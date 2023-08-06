/// <reference types="react" />
export interface IPaginationOptions {
    /**
     * Number of items to show.
     */
    pageSize: number;
    /**
     * total number of pages.
     */
    pageCount: number;
    /**
     * Current page index.
     */
    pageIndex: number;
    /**
     * List of available page number.
     */
    pageOptions: number[];
    /**
     * Whether a previous page is available or not.
     */
    canPreviousPage: boolean;
    /**
     * Whether a next page is available or not.
     */
    canNextPage: boolean;
    /**
     * Function that will change the current page index.
     */
    gotoPage: (updater: ((pageIndex: number) => number) | number) => void;
    /**
     * Function to go to previous page;
     */
    previousPage: () => void;
    /**
     * Function to go to next page.
     */
    nextPage: () => void;
    /**
     * Function to change the number of items to show.
     */
    setPageSize: (pageSize: number) => void;
    /**
     * Whether the index is loading.
     */
    loading: boolean;
    /**
     * Whether to show the entire pagination bar.
     */
    showPagination: boolean;
}
export declare const Pagination: ({ pageSize, pageCount, gotoPage, canPreviousPage, previousPage, nextPage, canNextPage, pageIndex, pageOptions, setPageSize, loading, showPagination, }: IPaginationOptions) => JSX.Element;
