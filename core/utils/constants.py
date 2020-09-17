"""
Global constants used in the pseudo code.
"""


class STATUS(object):
    """
    List contains all the types of statuses used in the project.
    """
    # __slots__ = "SUCCESS", "FAILURE", "RUNNING", "INITIAL"

    SUCCESS = 0
    FAILURE = 1
    RUNNING = 2
    INITIAL = 3

    @classmethod
    def check_status(cls, status):
        """
        Check if it is a valid status.
        """
        if status in range(0, 4):
            return True
        raise RuntimeError('Invalid status code.')


known_port_list = {
    '21': 'FTP',
    '22': 'SSH',
    '23': 'Telnet',
    '25': 'SMTP',
    '43': 'Whois',
    '53': 'DNS',
    '68': 'DHCP',
    '80': 'HTTP',
    '110': 'POP3',
    '111': 'Portmapper',
    '115': 'SFTP',
    '119': 'NNTP',
    '123': 'NTP',
    '137': 'NetBIOS',
    '139': 'NetBIOS',
    '143': 'IMAP',
    '161': 'SNMP',
    '220': 'IMAP3',
    '389': 'LDAP',
    '443': 'SSL',
    '445': 'SAMBA',
    '513': 'Rlogin',
    '514': 'Rlogin',
    '691': 'Microsoft Exchange',
    '1433': 'MSSQL',
    '1521': 'Oracle SQL',
    '1701': 'L2TP',
    '1723': 'PPTP',
    '2049': 'NFS',
    '3306': 'mySQL',
    '3388': 'RDP',
    '3389': 'RDP',
    '3390': 'OWA',
    '4125': 'OWA',
    '5060': 'VNC',
    '5061': 'VNC',
    '5062': 'VNC',
    '5063': 'VNC',
    '5064': 'VNC',
    '5065': 'VNC',
    '5432': 'PostgreSQL',
    '5802': 'VNC',
    '5804': 'VNC',
    '5900': 'VNC',
    '5901': 'VNC',
    '5903': 'VNC',
    '5905': 'VNC',
    '5986': 'VNC',
    '6000': 'Xwindows',
    '6002': 'Xwindows',
    '6003': 'Xwindows',
    '6060': 'Xwindows',
    '6061': 'Xwindows',
    '6062': 'Xwindows',
    '6063': 'Xwindows',
    '6379': 'Redis',
    '7000': 'Cassandra Apache',
    '7001': 'Cassandra Apache',
    '7199': 'Cassandra Apache',
    '8000': 'HTTP',
    '8080': 'HTTP',
    '8090': 'HTTP',
    '8443': 'HTTPS',
    '8888': 'HTTP',
    '9001': 'HTTP',
    '9042': 'Cassandra Apache',
    '27017': 'MongoDB',
    '27018': 'MongoDB',
    '27019': 'MongoDB',
}