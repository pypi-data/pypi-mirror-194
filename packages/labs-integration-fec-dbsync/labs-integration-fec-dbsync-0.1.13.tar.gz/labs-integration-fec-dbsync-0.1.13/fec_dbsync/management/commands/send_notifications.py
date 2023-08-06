import requests
import json
from datetime import date, timedelta, datetime

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection
import logging
from fec_dbsync.models import GeneralAccount

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Command for sending the notifications for users'

    def handle(self, *args, **options):
        """

        :param args:
        :param options:
        :return:
        """

        verbosity = int(options['verbosity'])
        root_logger = logging.getLogger('')

        if verbosity > 1:
            root_logger.setLevel(logging.DEBUG)

        response = requests.get(settings.WORKFLOW_BASE_URL + "/config?name=feCreditBusinessDate")
        try:
            today = response.json().get('data').get('value')
            today = datetime.strptime(today, '%d-%m-%Y')
        except:
            today = datetime.now()
        current_date = today
        logger.info("Current date: " + current_date.strftime('%Y-%m-%d'))

        query_date = current_date + timedelta(days=5)
        dmd_query_date = current_date - timedelta(days=270)
        dmd_query_date = dmd_query_date.strftime('%Y-%m-%d')
        cursor = connection.cursor()
        s = 'select fec_dbsync_robolrsview.LOAN_ACCT_NUM, fec_dbsync_robolrsview.NEXT_DMD_DATE,fec_dbsync_robolrsview.FLOW_AMT, COUNT(CASE WHEN fec_dbsync_roboidtview.DMD_AMT - fec_dbsync_roboidtview.TOT_ADJ_AMT <= 0 and fec_dbsync_roboidtview.LAST_ADJ_DATE > "{}" THEN 1 ELSE NULL END) as months from fec_dbsync_robolrsview LEFT OUTER JOIN fec_dbsync_roboidtview ON fec_dbsync_roboidtview.LOAN_ACCT_NUM = fec_dbsync_robolrsview.LOAN_ACCT_NUM group by fec_dbsync_robolrsview.LOAN_ACCT_NUM,fec_dbsync_robolrsview.NEXT_DMD_DATE,fec_dbsync_robolrsview.FLOW_AMT'
        cursor.execute(s.format(dmd_query_date))
        data  = {
                    "contractId" : "",
                    "dueDate" : "",
                    "dueAmount" : "",
                    "sendSMS" : True,
                    "sendNotification" : True,
                    "sendEmail" : True,
                    "smsTemplateKey" : "",
                    "notificationTemplateKey" : "",
                    "emailTemplateKey" : ""
                }
        URL = settings.WORKFLOW_BASE_URL + "/notify/"
        for row in cursor:
            contract_number = row[0]

            gam_object = GeneralAccount.objects.get(LOAN_ACCT_NUM=contract_number)

            if gam_object.DPD_CNTR > 0:
                continue

            count  = row[3]
            diff = row[1] - current_date.date()
            data["contractId"] = row[0]
            data["dueDate"] = row[1].strftime('%d-%m-%Y')
            data["dueAmount"] = row[2]
            logger.debug ("Count: " + str(count))
            logger.debug ("Diff: " + str(diff))
            logger.debug ("Current_Date: " + current_date.strftime('%Y-%m-%d'))
            if count>=9:
                if diff.days == 3 :
                    data["smsTemplateKey"] = "DPD_3"
                    data["notificationTemplateKey"] = "DPD_3"
                    data["emailTemplateKey"] = "DPD_3"
                elif diff.days == 0 :
                    data["smsTemplateKey"] = "DPD_0"
                    data["notificationTemplateKey"] = "DPD_0"
                    data["emailTemplateKey"] = "DPD_0"
                else:
                    continue

            if count<=9 and count>=6:
                if diff.days == 5 :
                    data["smsTemplateKey"] = "DPD_5"
                    data["notificationTemplateKey"] = "DPD_5"
                    data["emailTemplateKey"] = "DPD_5"
                elif diff.days == 0 :
                    data["smsTemplateKey"] = "DPD_0"
                    data["notificationTemplateKey"] = "DPD_0"
                    data["emailTemplateKey"] = "DPD_0"
                else:
                    continue

            if count<=6 and count>=3:
                if diff.days == 5:
                    data["smsTemplateKey"] = "DPD_5"
                    data["notificationTemplateKey"] = "DPD_5"
                    data["emailTemplateKey"] = "DPD_5"
                elif diff.days == 3:
                    data["smsTemplateKey"] = "DPD_3"
                    data["notificationTemplateKey"] = "DPD_3"
                    data["emailTemplateKey"] = "DPD_3"
                elif diff.days == 0:
                    data["smsTemplateKey"] = "DPD_0"
                    data["notificationTemplateKey"] = "DPD_0"
                    data["emailTemplateKey"] = "DPD_0"
                else:
                    continue

            if count<=3 :
                if diff.days == 5:
                    data["smsTemplateKey"] = "DPD_5"
                    data["notificationTemplateKey"] = "DPD_5"
                    data["emailTemplateKey"] = "DPD_5"
                elif diff.days == 3:
                    data["smsTemplateKey"] = "DPD_3"
                    data["notificationTemplateKey"] = "DPD_3"
                    data["emailTemplateKey"] = "DPD_3"
                elif diff.days == 0:
                    data["smsTemplateKey"] = "DPD_0"
                    data["notificationTemplateKey"] = "DPD_0"
                    data["emailTemplateKey"] = "DPD_0"
                else:
                    continue
            logger.info("Request payload: " + str(data))
            headers = {'content-type':'application/json'}

            response = requests.post(URL, data=json.dumps(data), headers=headers)
            logger.info("Response : " + str(response.content))