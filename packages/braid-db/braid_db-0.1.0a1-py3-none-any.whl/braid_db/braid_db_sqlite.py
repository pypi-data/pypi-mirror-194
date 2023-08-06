# Keeping this in the codebase for now for historical purposes
class BraidDBSQLite:
    def __init__(self, db_file, log=False, debug=False, mpi=False):
        self.db_file = db_file
        self.logger = logging.getLogger("BraidDB")
        level = logging.WARN
        if log:
            level = logging.INFO
        if debug:
            level = logging.DEBUG
        self.logger.setLevel(level)
        self.mpi = mpi

        if not self.mpi:
            self.sql = BraidSQL(db_file, log, debug)
        else:
            from db_tools_mpi import BraidSQL_MPI

            self.sql = BraidSQL_MPI(db_file, log, debug)
        self.sql.connect()

    def create(self):
        """Set up the tables defined in the SQL file"""
        if self.mpi:
            if self.sql.rank != 0:
                return
        BRAID_HOME = os.getenv("BRAID_HOME")
        if BRAID_HOME is None:
            braid_sql = DEFAULT_SCHEMA_FILE_PATH
        else:
            braid_sql = f"{BRAID_HOME}/src/braid_db/braid-db.sql"
        print(f"creating DB tables: '{self.db_file}'")
        with open(braid_sql) as fp:
            sqlcode = fp.read()
            try:
                self.sql.executescript(sqlcode)
                self.sql.commit()
            except OperationalError as oe:
                self.logger.info(f"Got error creating DB: {str(oe)}")

    def insert(self, record):
        pass

    def print(self):
        self.sql.select("records", "*")
        records = {}
        while True:
            row = self.sql.cursor.fetchone()
            if row is None:
                break
            (record_id, name, time) = row[0:3]
            text = "%5s : %-16s %s" % ("[%i]" % record_id, name, time)
            records[record_id] = text
        for record_id in list(records.keys()):
            deps = self.get_dependencies(record_id)
            text = records[record_id] + " <- " + str(deps)
            records[record_id] = text
        for record_id in list(records.keys()):
            uris = self.get_uris(record_id)
            text = records[record_id]
            for uri in uris:
                text += "\n\t\t\t URI: "
                text += uri
            records[record_id] = text
        self.extract_tags(records)
        for record_id in list(records.keys()):
            print(records[record_id])

    def extract_tags(self, records):
        """Append tags data to records"""
        tags = {}  # In case there are no records
        for record_id in list(records.keys()):
            tags = self.get_tags(record_id)
            text = records[record_id]
        for key in tags.keys():
            text += "\n\t\t\t TAG: "
            if (
                tags[key].type_ == BraidTagType.INTEGER
                or tags[key].type_ == BraidTagType.FLOAT
            ):
                text += "%s = %s" % (key, tags[key].value)
            else:
                text += "%s = '%s'" % (key, tags[key].value)
            records[record_id] = text

    def get_dependencies(self, record_id):
        """
        return list of integers
        """
        self.trace("DB.get_dependencies(%i) ..." % record_id)
        self.sql.select(
            "dependencies", "dependency", "record_id=%i" % record_id
        )
        deps = []
        while True:
            row = self.sql.cursor.fetchone()
            if row is None:
                break
            deps.append(row[0])
        return deps

    def get_uris(self, record_id):
        """
        return list of string URIs
        """
        self.trace("DB.get_uris(%i) ..." % record_id)
        self.sql.select("uris", "uri", "record_id=%i" % record_id)
        uris = []
        while True:
            row = self.sql.cursor.fetchone()
            if row is None:
                break
            uris.append(row[0])
        return uris

    def get_tags(self, record_id):
        """
        return dict of string->BraidTagValue key->value pairs
        """
        self.trace(f"DB.get_tags({record_id}) ...")
        self.sql.select("tags", "key, value, type", f"record_id={record_id}")
        tags = {}
        while True:
            row = self.sql.cursor.fetchone()
            if row is None:
                break
            (key, v, t) = row[0:3]
            type_ = BraidTagType(t)
            value = BraidTagValue(v, type_)
            tags[key] = value
        return tags

    def debug(self, msg):
        self.logger.debug(msg)

    def trace(self, msg):
        self.logger.log(level=logging.DEBUG - 5, msg=msg)
        print(f"DEBUG {(msg)=}")

    def size(self):
        """
        For performance measurements, etc.
        Just the sum of the table sizes
        """
        result = 0
        tables = ["records", "dependencies", "uris", "tags"]
        for table in tables:
            self.sql.select(table, "count(record_id)")
            row = self.sql.cursor.fetchone()
            assert row is not None
            count = int(row[0])
            print("count: %s = %i" % (table, count))
            result += count

        return result
