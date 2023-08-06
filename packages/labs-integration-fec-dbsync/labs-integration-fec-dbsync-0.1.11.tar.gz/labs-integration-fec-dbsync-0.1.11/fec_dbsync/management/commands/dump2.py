import time

import cx_Oracle
from fec_dbsync.constants import MODELS_DICT, batch_size
from django.core.management.base import BaseCommand
from django.db import connections


class Command(BaseCommand):
    help = 'Take Database dump from oracle database and store in to integration broker database'

    def make_connection(self):
        database_id = "dump2"  # just something unique
        newDatabase = {}
        newDatabase["id"] = database_id
        newDatabase['ENGINE'] = 'django.db.backends.mysql'
        newDatabase['NAME'] = '/path/to/db_%s.sql' % database_id
        newDatabase['USER'] = ''
        newDatabase['PASSWORD'] = ''
        newDatabase['HOST'] = ''
        newDatabase['PORT'] = ''
        connections.databases[database_id] = newDatabase

    # x = GeneralAccount.objects.using('dump2').all()
    # print(x)

    def take_dump(self, curr, offset, limit, model):
        """

        :param offset:
        :param limit:
        :return:
        """
        SQL = 'SELECT ' + ",".join(MODELS_DICT[model]['row_dict'].keys()) + ' from ' + MODELS_DICT[model][
            'table_name'] + ' OFFSET {} ROWS FETCH NEXT {} ROWS ONLY'  # FOR ORACLE
        # SQL = 'SELECT * from '+ MODELS_DICT[model]['table_name'] +' limit {},{}'  # FOR MYSQL


        curr.execute(SQL.format(offset, limit))
        obj = []
        for row in curr:
            new_object = model()
            for attribute in MODELS_DICT[model]['row_dict'].keys():
                setattr(new_object, attribute, eval(MODELS_DICT[model]['row_dict'][attribute]))
            obj.append(new_object)
        print ('===============SYNCING DATA FROM TABLE================')
        print (MODELS_DICT[model]['table_name'])
        print('=======================================================')
        model.objects.bulk_create(obj)

    def handle(self, *args, **options):
        """

        :param args:
        :param options:
        :return:
        """
        self.make_connection()
        start_time = time.time()
        conn = cx_Oracle.connect('ROBO_MOBILE/robo1qa3ws@newfin-pro-scan:1521/LMSPROD')  # FOR ORACLE
        # conn = MySQLdb.connect(host="localhost", user="root", password="kuliza123", db="dump2")  # FOR MYSQL
        for model in MODELS_DICT:
            curr = conn.cursor()
            SQL = 'SELECT count(*) from ' + MODELS_DICT[model]['table_name']
            curr.execute(SQL)
            for row in curr:
                row_count = row[0]
            if not row_count:
                row_count = 0
            offset = 0
            model.objects.all().delete()
            while row_count > 0:
                limit = row_count
                if row_count > batch_size:
                    limit = batch_size
                row_count -= limit
                self.take_dump(curr, offset, limit, model)
                offset += batch_size
            curr.close()
        conn.close()
        print(time.time() - start_time)
