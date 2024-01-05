"""
[TODO]
The database should be backed up from time to time.
Introduce operations to support backing up and restoring the database state based on timestamps.
When restoring, ttl expiration times should be recalculated accordingly.

BACKUP <timestamp> — should save the database state at the specified timestamp, including the remaining ttl for all records and fields.
Remaining ttl is the difference between their initial ttl and their current lifespan (the duration between the timestamp of this operation and their initial timestamp).
Returns a string representing the number of non-empty non-expired records in the database.

RESTORE <timestamp> <timestampToRestore> — should restore the database from the latest backup before or at timestampToRestore.
It's guaranteed that a backup before or at timestampToRestore will exist.
Expiration times for restored records and fields should be recalculated according to the timestamp of this operation - since the database timeline always flows forward, restored records and fields should expire after the timestamp of this operation, depending on their remaining ttls at backup. This operation should return an empty string.
"""
import math
from typing import Optional


class MemDb:
    """Simple memory db class"""

    OP_SET = "SET"
    OP_SET_AT = "SET_AT"
    OP_SET_AT_TTL = "SET_AT_WITH_TTL"
    OP_GET = "GET"
    OP_GET_AT = "GET_AT"
    OP_DEL = "DELETE"
    OP_DEL_AT = "DELETE_AT"
    OP_SCAN = "SCAN"
    OP_SCAN_AT = "SCAN_AT"
    OP_SCAN_FILTER = "SCAN_BY_PREFIX"
    OP_SCAN_FILTER_AT = "SCAN_BY_PREFIX_AT"
    OP_BACKUP = "BACKUP"
    OP_RESTORE = "RESTORE"
    FIELD_TIMESTAMP = "timestamp"
    FIELD_TTL = "ttl"
    FIELD_VALUE = "value"
    TOKEN_EMPTY = ""
    TOKEN_DEL_SUCCESS = "true"
    TOKEN_DEL_FAILURE = "false"

    # key -> {field: {value, timestamp, ttl}}
    __data: "dict[str, dict[str, dict[str, str]]]" = {}

    def query(self, *args: "str") -> "str":
        """
        Handle all queries the db supports
        args: op, key, field/prefix, value, timestamp, ttl
        """
        op, key, *rest = args
        if op == MemDb.OP_SET or op == MemDb.OP_SET_AT or op == MemDb.OP_SET_AT_TTL:
            return self.insert(key, *rest)
        elif op == MemDb.OP_GET or op == MemDb.OP_GET_AT:
            return self.retrieve(key, *rest)
        elif op == MemDb.OP_DEL or op == MemDb.OP_DEL_AT:
            return self.delete(key, *rest)
        elif (
            op == MemDb.OP_SCAN
            or op == MemDb.OP_SCAN_FILTER
            or op == MemDb.OP_SCAN_FILTER_AT
        ):
            return self.scan(key, *rest)
        elif op == MemDb.OP_SCAN_AT:
            return self.scan(key, None, rest[0])
        else:
            raise NotImplementedError(f"Unsupported operation: {args}")

    def insert(
        self,
        key: "str",
        field: "str",
        value: "str",
        timestamp: "Optional[str]" = None,
        ttl: "Optional[str]" = None,
    ) -> "str":
        """Add or create a record with the field and value set"""
        if key not in self.__data:
            self.__data[key] = {}

        self.__data[key][field] = {MemDb.FIELD_VALUE: value}

        if timestamp:
            self.__data[key][field][MemDb.FIELD_TIMESTAMP] = int(timestamp)
            if ttl:
                self.__data[key][field][MemDb.FIELD_TTL] = int(ttl)

        return MemDb.TOKEN_EMPTY

    def get_existing_fields_at(
        self,
        key: "str",
        timestamp: "Optional[str]" = None,
    ) -> "Optional[set[str]]":
        """Get the existing fields for a record at a given timestamp"""
        if key not in self.__data:
            return None

        existing_record = self.__data.get(key, {})
        op_timestamp = int(timestamp) if timestamp else 0
        existing_fields = set()
        for field, value in existing_record.items():
            # fallback to op timestamp in order to always return value when record has no timestamp
            record_timestamp = value.get(MemDb.FIELD_TIMESTAMP, op_timestamp)
            # field lives forever if no TTL has been specified
            record_ttl = value.get(MemDb.FIELD_TTL, math.inf)
            # check if the record timestamp and ttl contain the op timestamp, end exclusive
            if (
                op_timestamp >= record_timestamp
                and op_timestamp < record_timestamp + record_ttl
            ):
                existing_fields.add(field)

        return existing_fields

    def exists(
        self,
        key: "str",
        field: "Optional[str]" = None,
        timestamp: "Optional[str]" = None,
    ) -> "bool":
        """Check if field exists in record at given timestamp"""
        existing_fields = self.get_existing_fields_at(key, timestamp)
        # key does not exist in db
        if existing_fields is None:
            return False
        # no field specified so return if any fields found
        if field is None:
            return bool(existing_fields)
        # check if field exists at the specified timestamp
        return field in existing_fields

    def retrieve(
        self, key: "str", field: "str", timestamp: "Optional[str]" = None
    ) -> "str":
        """Get value from record entry with a fallback when not found"""
        if self.exists(key, field, timestamp):
            return (
                self.__data.get(key, {})
                .get(field, {})
                .get(MemDb.FIELD_VALUE, MemDb.TOKEN_EMPTY)
            )

        return MemDb.TOKEN_EMPTY

    def delete(
        self, key: "str", field: "str", timestamp: "Optional[str]" = None
    ) -> "bool":
        """Remove field value from record if it exists"""
        if not self.exists(key, field, timestamp):
            return MemDb.TOKEN_DEL_FAILURE

        del self.__data[key][field]
        return MemDb.TOKEN_DEL_SUCCESS

    def scan(
        self,
        key: "str",
        prefix: "Optional[str]" = None,
        timestamp: "Optional[str]" = None,
    ) -> "str":
        """Retrieve entire record formatted if it exists with fields filtered"""
        fields = self.get_existing_fields_at(key, timestamp)

        if fields is None:
            return MemDb.TOKEN_EMPTY

        record = self.__data[key]
        return ", ".join(
            f"{f}({record.get(f).get(MemDb.FIELD_VALUE)})"
            for f in sorted(fields)
            if prefix is None or f.startswith(prefix)
        )


def solution(queries: "list[list[str]]") -> "list[str]":
    """For each query perform the operation on the same db instance"""
    db = MemDb()
    return [db.query(*q) for q in queries]
