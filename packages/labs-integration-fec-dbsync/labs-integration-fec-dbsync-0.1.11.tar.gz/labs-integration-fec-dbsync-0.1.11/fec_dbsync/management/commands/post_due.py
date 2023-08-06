import json
import logging
import os

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from fec_dbsync.models import GeneralAccount, RoboChatView, RoboIdtView, RoboEitView
from django.db.models import Q

from fec_dbsync.constants import collections_journey_name_config

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Command for post due.'

    def get_config(self, name):
        url = 'http://localhost:8000/integrations/api/config/?name=' + name

        try:
            response = requests.get(url)
            response = json.loads(response.content, encoding='utf-8')
            if 'response' in response and response['response']:
                return  response['response']
            return None
        except Exception:
            return  None

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

        post_due_records = GeneralAccount.objects.filter(DPD_CNTR__gt=0)

        collections_payload = []

        for application in post_due_records:
            emi = 0

            emi_records_idt = RoboIdtView.objects.filter(Q(LOAN_ACCT_NUM=application.LOAN_ACCT_NUM),
                                                         Q(DMD_FLOW_ID='PRDEM') | Q(DMD_FLOW_ID='INDEM'))
            for record in emi_records_idt:
                emi = emi + max(record.DMD_AMT - record.TOT_ADJ_AMT, 0)

            penalty_amount = 0

            penalty_records_idt = RoboIdtView.objects.filter(LOAN_ACCT_NUM=application.LOAN_ACCT_NUM,
                                                             DMD_FLOW_ID='PIDEM')
            for record in penalty_records_idt:
                penalty_amount = penalty_amount + max(record.DMD_AMT - record.TOT_ADJ_AMT, 0)

            penalty_records_eit = RoboEitView.objects.filter(LOAN_ACCT_NUM=application.LOAN_ACCT_NUM)
            for record in penalty_records_eit:
                penalty_amount = penalty_amount + max(record.PENAL_BOOKED_AMOUNT_DR - record.PENAL_INTEREST_AMOUNT_DR,
                                                      0)

            processing_fee = 0

            processing_records_chat = RoboChatView.objects.filter(LOAN_ACCT_NUM=application.LOAN_ACCT_NUM,
                                                                  CHARGE_TYPE='MISC2')
            for record in processing_records_chat:
                processing_fee = processing_fee + max(record.USER_CALC_CHRGE_AMT,
                                                      record.SYS_CALC_CHRGE_AMT) \
                                 - record.CHRGE_AMT_COLLECTED - record.CHRGE_WAIVED

            single_payload = {
                'loanContractNumber': application.LOAN_ACCT_NUM,
                'dpd': application.DPD_CNTR,
                'outstandingLoanAmount': abs(application.CURRENT_BAL),
                'penalty': penalty_amount,
                'processingFee': processing_fee,
                'emi': emi
            }

            collections_payload.append(single_payload)

        login_url = settings.WORKFLOW_BASE_URL + "/login/credentials/"
        headers = {
            'Content-Type': "application/json",
            'Cache-Control': "no-cache"
        }
        data = {
            "username": os.environ.get('FLOWABLE_WORKFLOW_COLLECTION_USER', 'collections_admin'),
            "password": os.environ.get('FLOWABLE_WORKFLOW_COLLECTION_PASSWORD', 'test')
        }
        response = requests.post(login_url, data=json.dumps(data), headers=headers)
        response = response.json()
        if not response.get('status') == 200 or not response.get('data'):
            return {"status": False, "message": "Can't Login"}
        auth_token = response.get('data').get('bpm_token')

        # journey_name = self.get_config(collections_journey_name_config)

        # Hardcoding this until config API is pushed.
        journey_name = "test"
        
        if not journey_name or len(collections_payload) == 0:
            return "No records to process."

        payload = {
            'journeyName': journey_name,
            'collections': collections_payload
        }

        URL = settings.WORKFLOW_BASE_URL + "/collections/initiate"

        logger.info("Request payload: " + str(payload))

        headers = {'content-type': 'application/json', "Authorization": "Bearer " + auth_token}

        response = requests.post(URL, data=json.dumps(payload), headers=headers)

        logger.info("Response : " + str(response.content))
