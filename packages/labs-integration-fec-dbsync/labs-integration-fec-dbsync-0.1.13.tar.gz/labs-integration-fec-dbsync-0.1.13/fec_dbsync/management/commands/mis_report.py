# import os
import json
from django.core.management.base import BaseCommand
from fec_dbsync import utils as fec_dbsync_utils
from fec_dbsync.models import MISReportRequestTracking
from fec_dbsync.constants import MIS_REPORT_METHODS
import logging


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Command For Generating MIS Report for different sheets.'

    def handle(self, *args, **options):
        """
        :param args:
        :param options:
        :return:
        """
        report_to_runs = MISReportRequestTracking.objects.filter(status=False)
        if report_to_runs:
            for report_obj in report_to_runs:
                logger.info("Report running: " + report_obj.report_request)
                if hasattr(fec_dbsync_utils, MIS_REPORT_METHODS.get(report_obj.report_request)):
                    try:
                        filters = json.loads(report_obj.filters)
                    except:
                        filters = None
                        logger.debug("Filter Error in report: " + report_obj.report_request + " With filters")
                    try:
                        emails = json.loads(report_obj.emails)
                    except:
                        emails = []
                        logger.debug("Emails Error in report: " + report_obj.report_request + " With emails")
                    try:
                        request_timestamp = report_obj.requester + "_{}_" + report_obj.created_at.strftime("%Y-%m-%d_%H:%M:%S")
                    except:
                        request_timestamp = report_obj.requester + "_{}_" + str(report_obj.id)
                    try:
                        mis_report_file= getattr(fec_dbsync_utils, MIS_REPORT_METHODS.get(report_obj.report_request))(request_timestamp, filters)
                        if type(mis_report_file) == str:
                            report_obj.status = 1
                            report_obj.save()
                            # email_response = fec_dbsync_utils.send_mail(mis_report_file, emails)
                            # if email_response.get('error') is None or email_response.get('error') == "":
                            #     report_obj.update(status=True)
                            #     os.remove(mis_report_file)
                            logger.info("Report generated: " + mis_report_file)
                        else:
                            try:
                                logger.debug("Error: " + json.dumps(mis_report_file))
                            except:
                                logger.debug("Something went wrong in sheet: " + report_obj.report_request)
                    except:
                        logger.debug("Something went wrong in sheet: " + report_obj.report_request)

        logger.info("No Report to run")