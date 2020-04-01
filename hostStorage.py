from hostingInfo import HostInfo
import sqlite3

class HostStorage:
    def __init__(self, name):
        """
        :param name: Name of the db or path
        """
        self._conn = sqlite3.connect(name)
        self._conn.execute("CREATE table if not EXISTS hosts (domain text PRIMARY KEY, datacenter text)")
        self._conn.commit()

    def getHostInfo(self, domain):
        """
        Obtains the datacener of a given domain

        :param domain: Domain to fetch
        :return: Datacenter
        """
        rows = self._conn.execute("SELECT * FROM hosts WHERE domain=?", (domain,))

        for (domain, datacenter) in rows.fetchall():
            return HostInfo(domain=domain, datacenter=datacenter)

        return None

    def cache(self, hostsInfo):
        """
        Cache the given data

        :param hostInfo: A list of HostInfo to store
        """

        rows = []
        for h in hostsInfo:
            rows.append((h.domain, h.datacenter))

        self._conn.executemany("INSERT INTO hosts (domain, datacenter) VALUES (?,?)", rows)
        self._conn.commit()
