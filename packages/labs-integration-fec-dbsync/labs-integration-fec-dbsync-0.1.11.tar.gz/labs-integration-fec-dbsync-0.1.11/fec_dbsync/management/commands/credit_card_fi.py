# import os
import json
from django.core.management.base import BaseCommand
from fec_dbsync import utils as fec_dbsync_utils
from fec_dbsync.models import MISReportRequestTracking
from fec_dbsync.constants import MIS_REPORT_METHODS
import logging


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Command For Generating FI Credit Card FI Report.'

    def handle(self, *args, **options):
        """
        :param args:
        :param options:
        :return:
        """
        logger.info("Credit Card FI Running")
        try:
            fec_dbsync_utils.mis_credit_card_fi("FI_Report")
        except Exception as e:
            logger.debug("Error in FI Job: " + repr(e))

