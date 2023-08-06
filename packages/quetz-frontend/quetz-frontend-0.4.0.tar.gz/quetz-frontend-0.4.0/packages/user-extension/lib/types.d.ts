export declare type APIKeyInfo = {
    description: string;
    expire_at: string;
    roles: Role[];
};
export declare type Role = {
    channel: string;
    package: string;
    role: string;
};
export declare type APIKey = {
    description: string;
    time_created: string;
    expire_at: string;
    roles: Role[];
    key: string;
};
export declare type Channel = {
    name: string;
    role: string;
};
export declare type Package = {
    name: string;
    channel_name: string;
    role: string;
};
