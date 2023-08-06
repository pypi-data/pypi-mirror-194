import MySQLdb
import time
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Command For Populating Data into a remote DB'


    def handle(self, *args, **options):
        """

        :param args:
        :param options:
        :return:
        """
        start_time = time.time()
        conn = MySQLdb.connect(host="localhost", user="root", password="kuliza123", db="dump2")
        curr = conn.cursor()
        SQL = 'INSERT INTO database_dump_robochatview VALUES ({},"asas","ab","ab",1212,1212,12121,2121,12)'
        for i in range(100000):
            curr.execute(SQL.format(i+1))
        curr.close()
        conn.commit()
        conn.close()
        print(time.time()-start_time)