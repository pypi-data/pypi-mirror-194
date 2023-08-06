import base64
import datetime
import logging
import os

import MySQLdb
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Command For Generating User Journey by quering flowable DB.'

    def handle(self, *args, **options):
        """
        :param args:
        :param options:
        :return:
        """
        try:
            host = os.environ.get('IB_DATABASE_HOST', 'localhost')
            username = os.environ.get('IB_DATABASE_USER', 'username')
            password = base64.b64decode(os.environ.get('IB_DATABASE_PASSWORD', 'cGFzc3dvcmQ=')).decode("utf-8")
            database = os.environ.get('FLOWABLE_DATABASE_NAME', 'flowableDB')
            mobile_mapping_database = os.environ.get('MOBILE_MAPPING_DATABASE_NAME', 'mobile_mapping')

            db = MySQLdb.connect(host, username, password, database)
        except Exception as e:
            logger.debug("Unable to connect to database: " + repr(e))

        cursor = db.cursor()
        cursor_insert = db.cursor()

        try:
            table_create_query = """create table if not exists """ + mobile_mapping_database + """.campaign_journey 
                                        (id bigint(20) NOT NULL, created datetime, modified datetime, 
                                        contact_number varchar(255), campaign_id int, device_type varchar(255), 
                                        application_date varchar(255), application_stage varchar(255), 
                                        PROC_INST_ID_ varchar(64), application_status varchar(255));"""
            logger.info("Running Query: " + table_create_query)
            cursor.execute(table_create_query)
            db.commit()

            table_truncate_query = "truncate " + mobile_mapping_database + ".campaign_journey;"
            logger.info("Running Query: " + table_truncate_query)
            cursor.execute(table_truncate_query)
            db.commit()

            user_journey_query = """
                SELECT  a.id, a.created "User Creation", a.modified "User Modified", a.contact_number "Mobile Number", a.device_type "Customer Device",

                        b.application_date, b.application_stage,
                
                        c.PROC_INST_ID_,
                
                        CASE WHEN (c.TASK_DEF_KEY_ = 'emiCalculator' OR c.TASK_DEF_KEY_ = 'enterYourDetails' OR c.TASK_DEF_KEY_ = 'statusScreen-1' OR c.TASK_DEF_KEY_ = 'enterYourDetailsClone' OR c.TASK_DEF_KEY_ = 'emiCalculator-clone1' OR c.TASK_DEF_KEY_ = 'statusScreen-11' OR c.TASK_DEF_KEY_ = 'emiCalculator-clone2' OR c.TASK_DEF_KEY_ = 'statusScreen-12' OR c.TASK_DEF_KEY_ = 'enterYourDetailsClone_2' OR c.TASK_DEF_KEY_ ='emiCalculatorClone') THEN 'REGISTRATION'
                
                             WHEN (c.TASK_DEF_KEY_ = 'identityVerification' OR c.TASK_DEF_KEY_ = 'statusScreen-2' OR c.TASK_DEF_KEY_ = 'statusScreen-rejectMessageBlacklist' OR c.TASK_DEF_KEY_ = 'statusScreen-rejectMessageRetry') THEN 'IDENTITY VERIFICATION'
                
                             WHEN (c.TASK_DEF_KEY_ = 'uploadSurrogateDocuments') THEN 'INCOME VERIFICATION'
                
                             WHEN (c.TASK_DEF_KEY_ = 'statusScreen-3' OR c.TASK_DEF_KEY_ = 'applicationReview' OR c.TASK_DEF_KEY_ = 'statusScreen-4' OR c.TASK_DEF_KEY_ = 'applicationReviewSelfEmployed') THEN 'APPLICATION REVIEW'
                
                             WHEN (c.TASK_DEF_KEY_ ='loanoffer' OR c.TASK_DEF_KEY_ = 'modeofdisbursement') THEN 'APPROVAL'
                
                             WHEN (c.TASK_DEF_KEY_ = 'loanAgree' OR c.TASK_DEF_KEY_ = 'statusScreen-csApproval') THEN 'ESIGN'
                
                             WHEN (c.TASK_DEF_KEY_ = 'congratsScreen-collectionModeVnpost' OR c.TASK_DEF_KEY_ = 'congratsScreen-transfertoexistingaccount' OR c.TASK_DEF_KEY_ = 'congratsScreen-transfertovpbankaccount') THEN 'DISBURSEMENT'
                
                             WHEN (c.TASK_DEF_KEY_ = 'congratulationScreen-last') THEN 'DISBURSED'
                
                             WHEN (c.TASK_DEF_KEY_ = 'statusScreen-cancelMessage') THEN 'CANCELLATION'
                
                             WHEN (c.TASK_DEF_KEY_ = 'statusScreen-rejectionMessage' OR c.TASK_DEF_KEY_ = 'rejectMessageRetry' OR c.TASK_DEF_KEY_ = 'rejectMessageBlacklist' OR c.TASK_DEF_KEY_ = 'rejectionMessage') THEN 'REJECTION'
                
                             ELSE 'TBD'
                
                         END as application_status      
                
                FROM los_user AS a INNER JOIN los_user_loan_data AS b ON a.id = b.user_id INNER JOIN ACT_RU_TASK AS c ON b.process_instance_id = c.PROC_INST_ID_ INNER JOIN """ + mobile_mapping_database + """.Crosssell_mobile_mapping as d on a.contact_number = d.phone
                
                UNION ALL
                
                SELECT a.id, a.created "User Creation", a.modified "User Modified", a.contact_number "Mobile Number", a.device_type "Customer Device", NULL application_date, NULL application_stage, NULL PROC_INST_ID_, 'LOGIN' application_status
                
                FROM los_user AS a LEFT OUTER JOIN los_user_loan_data AS b ON a.id = b.user_id INNER JOIN """ + mobile_mapping_database + """.Crosssell_mobile_mapping as c on a.contact_number = c.phone
                
                WHERE 1=1
                
                AND b.user_id is NULL;
            """
            logger.info("Running Query: " + user_journey_query)
            cursor.execute(user_journey_query)

            for row in cursor:
                values = []
                for i in range(len(row)):
                    if row[i] == None:
                        values.append("NULL")
                    else:
                        values.append(row[i])

                application_date = values[5]
                try:
                    application_date = datetime.datetime.fromtimestamp(int(application_date) // 1000).replace(
                        tzinfo=datetime.timezone.utc).strftime(
                        '%a %b %d %H:%M:%S %Z %Y')
                except:
                    application_date = values[5]

                insert_query = "insert into " + mobile_mapping_database + ".campaign_journey VALUES (" + str(
                    values[0]) + ",CAST('" + values[1].strftime("%Y-%m-%d %H:%M:%S") + "' AS datetime),CAST('" + values[
                                   2].strftime("%Y-%m-%d %H:%M:%S") + "' AS datetime),'" + values[3] + "',1,'" + \
                               values[4] + "','" + application_date + "','" + values[6] + "','" + values[7] + "','" + \
                               values[8] + "');"
                logger.info("Running Query: " + insert_query)
                cursor_insert.execute(insert_query)
            db.commit()

        except Exception as e:
            logger.debug("Unable to query database: " + repr(e))
            db.rollback()

        db.close()
