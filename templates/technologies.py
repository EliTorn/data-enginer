TECHNOLOGY_TEMPLATES = {
    "database": [
        "Database {db_name} on {server} is experiencing slow query performance",
        "{server} PostgreSQL connection pool exhausted",
        "MySQL replication lag on {server} exceeds 10 seconds",
        "Oracle backup failed on {server} - tablespace full",
        "{server} MongoDB replica set member unreachable"
    ],
    "networking": [
        "Network connectivity issues between {server} and {server2}",
        "{server} experiencing packet loss to gateway",
        "VPN tunnel down affecting {server}",
        "Firewall blocking port 443 on {server}",
        "{server} DNS resolution failures"
    ],
    "authentication": [
        "LDAP authentication failing on {server}",
        "Users unable to login to {server} - Active Directory timeout",
        "{server} Kerberos ticket expiration issues",
        "SSO integration broken on {server}",
        "Failed login attempts from {server} exceed threshold"
    ],
    "api": [
        "{server} REST API returning 500 errors",
        "API rate limiting triggered on {server}",
        "{server} GraphQL endpoint timeout",
        "Webhook delivery failures from {server}",
        "{server} API gateway health check failing"
    ],
    "storage": [
        "Disk space critically low on {server} - 95% full",
        "{server} NFS mount unresponsive",
        "S3 bucket access denied from {server}",
        "{server} RAID array degraded - drive failure",
        "Backup volume on {server} out of space"
    ]
}



TECHNOLOGIES_DESCRIPTIONS = {
    "database": (
        "Issues related to database systems and data persistence, including performance degradation, "
        "replication problems, connection limits, backups, storage capacity, and database availability "
        "across relational and non-relational databases"
    ),

    "networking": (
        "Problems involving network communication and connectivity between systems, such as packet loss, "
        "routing failures, firewall restrictions, VPN tunnels, DNS resolution, and general network reachability"
    ),

    "authentication": (
        "Failures related to user identity, authentication, and access control mechanisms, including login "
        "issues, directory services, single sign-on integrations, credential validation, and authorization flows"
    ),

    "api": (
        "Issues concerning service-to-service communication and application interfaces, including API "
        "endpoints, request handling, integrations, timeouts, error responses, gateways, and rate limiting"
    ),

    "storage": (
        "Problems related to data storage systems and disk resources, including capacity exhaustion, "
        "filesystem availability, network-attached storage, object storage access, backups, and hardware failures"
    )
}
