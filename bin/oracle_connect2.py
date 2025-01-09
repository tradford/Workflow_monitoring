import cx_Oracle
import pandas as pd
import json

from keepass_connect import get_keepass_entry


###conf = json.loads(open('conf.json').read())
#password_key=list(conf['dict'].keys())[0]
#password=conf['dict'][password_key]
username = get_keepass_entry('Local ORCL ENSYNC', 'username')
password = get_keepass_entry('Local ORCL ENSYNC', 'password')
class Oracle():
    def __init__(self):
        print('Database Connection')
        
    def connect_node(self, username=username, password=password, hostname="EnviroOrCL112.ENVIROTECH.envirotechservices.com", port="1521", servicename="orcl"):
        """ Connect to the ORCL database. """
        try:
            self.db = cx_Oracle.connect(username, password
                                , hostname + ':' + port + '/' + servicename)
        except cx_Oracle.DatabaseError as e:
            # Log error as appropriate
            raise
        # If the database connection succeeded create the cursor
        # we-re going to use.
        self.cursor = self.db.cursor()

    def disconnect_node(self):
        """
        Disconnect from the database. If this fails, for instance
        if the connection instance doesn't exist, ignore the exception.
        """
        try:
            self.cursor.close()
            self.db.close()
        except cx_Oracle.DatabaseError:
            pass

    def execute_node(self, sql, commit=False):
        """
Execute whatever SQL procedure are passed to the method;
        commit if specified.

        """
        try:
            self.cursor.execute(sql)
        except cx_Oracle.DatabaseError as e:
            # Log error as appropriate
            raise
        # Only commit if it-s necessary.
        if commit:
            self.db.commit()

    def execute_proc_node(self, sql, commit=False):
        """
        Execute whatever SQL procedure are passed to the method;
        commit if specified.
        """
        try:
            self.cursor.callproc(sql)
        except cx_Oracle.DatabaseError as e:
            # Log error as appropriate
            raise
        # Only commit if it-s necessary.
        if commit:
            self.db.commit()
