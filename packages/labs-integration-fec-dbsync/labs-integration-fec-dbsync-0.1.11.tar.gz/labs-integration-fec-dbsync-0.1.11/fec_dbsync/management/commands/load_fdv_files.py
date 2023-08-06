from django.core.management.base import BaseCommand
from fec_dbsync.models import RoboCollectionFdv
import logging
from datetime import datetime
import os


logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def handle(self, *args, **options):
        verbosity = int(options['verbosity'])

        root_logger = logging.getLogger('')

        if verbosity > 1:
            root_logger.setLevel(logging.DEBUG)

        # TODO: Move this to a config once everything is tested
        # file_1_path = "/tmp/COLLECTION_FDV_ROBO_DEL_Finacle_25062018.txt"
        # file_2_path = "/tmp/COLLECTION_FDV_ROBO_PRE_Finacle_25062018.txt"
        file_1_path = os.environ.get('FDV_DEL_FILE_PATH', "/opt/fdv_files/COLLECTION_FDV_ROBO_DEL_Finacle_26092018.txt")
        file_2_path = os.environ.get('FDV_PRE_FILE_PATH', "/opt/fdv_files/COLLECTION_FDV_ROBO_PRE_Finacle_26092018.txt")

        RoboCollectionFdv.objects.all().delete()

        for line in open(file_1_path):
            parsed_line = line.rstrip('\n').split('|')
            RoboCollectionFdv.objects.create(TAG=parsed_line[0],
                                             FINANCIER_ID=parsed_line[1],
                                             APPL_ID=parsed_line[2],
                                             CUST_ID=float(parsed_line[3]) if parsed_line[3] else 0,
                                             PRINCIPAL_PAID=float(parsed_line[4]) if parsed_line[4] else 0,
                                             INTEREST_PAID=float(parsed_line[5]) if parsed_line[5] else 0,
                                             BCC_PAID=float(parsed_line[6]) if parsed_line[6] else 0,
                                             OTHER_PAID=float(parsed_line[7]) if parsed_line[7] else 0,
                                             PREPAYPENALTY_PAID=float(parsed_line[8]) if parsed_line[8] else 0,
                                             PRINCIPAL_DUE=float(parsed_line[9]) if parsed_line[9] else 0,
                                             INTEREST_DUE=float(parsed_line[10]) if parsed_line[10] else 0,
                                             BCC_DUE=float(parsed_line[11]) if parsed_line[11] else 0,
                                             OTHER_DUE=float(parsed_line[12]) if parsed_line[12] else 0,
                                             PREPAYPENALTY_DUE=float(parsed_line[13]) if parsed_line[13] else 0,
                                             LPC_PAID=float(parsed_line[14]) if parsed_line[14] else 0,
                                             LPC_DUE=float(parsed_line[15]) if parsed_line[15] else 0,
                                             FORMAT=parsed_line[16],
                                             TENTATIVE_FORECLOSURE_AMT=float(parsed_line[17]) if parsed_line[17] else 0,
                                             PREPAYPENALTY_PERCENT=float(parsed_line[18]) if parsed_line[18] else 0,
                                             PRINCIPAL_BALANCE=float(parsed_line[19]) if parsed_line[19] else 0,
                                             INSTALLMENT=float(parsed_line[20]) if parsed_line[20] else 0,
                                             PREPAYMENT_PENALTY=float(parsed_line[21]) if parsed_line[21] else 0,
                                             UNBILLED_INSTALLMENT=float(parsed_line[22]) if parsed_line[22] else 0,
                                             OVERDUE_CHARGES=float(parsed_line[23]) if parsed_line[23] else 0,
                                             ADVICE_OUTSTANDING_REPAYMENT_FEE=float(parsed_line[24]) if parsed_line[24] else 0,
                                             TOTAL_RECEIVABLE=float(parsed_line[25]) if parsed_line[25] else 0,
                                             NET_TOTAL=float(parsed_line[26]) if parsed_line[26] else 0,
                                             REFUNDS=float(parsed_line[27]) if parsed_line[27] else 0,
                                             CLOSURE_DATE=datetime.strptime(parsed_line[28], '%d-%m-%Y').strftime('%Y-%m-%d'),
                                             ACCRUED_PENAL_INTEREST=parsed_line[29])

        for line in open(file_2_path):
            parsed_line = line.rstrip('\n').split('|')
            RoboCollectionFdv.objects.create(TAG=parsed_line[0],
                                             FINANCIER_ID=parsed_line[1],
                                             APPL_ID=parsed_line[2],
                                             CUST_ID=float(parsed_line[3]) if parsed_line[3] else 0,
                                             PRINCIPAL_PAID=float(parsed_line[4]) if parsed_line[4] else 0,
                                             INTEREST_PAID=float(parsed_line[5]) if parsed_line[5] else 0,
                                             BCC_PAID=float(parsed_line[6]) if parsed_line[6] else 0,
                                             OTHER_PAID=float(parsed_line[7]) if parsed_line[7] else 0,
                                             PREPAYPENALTY_PAID=float(parsed_line[8]) if parsed_line[8] else 0,
                                             PRINCIPAL_DUE=float(parsed_line[9]) if parsed_line[9] else 0,
                                             INTEREST_DUE=float(parsed_line[10]) if parsed_line[10] else 0,
                                             BCC_DUE=float(parsed_line[11]) if parsed_line[11] else 0,
                                             OTHER_DUE=float(parsed_line[12]) if parsed_line[12] else 0,
                                             PREPAYPENALTY_DUE=float(parsed_line[13]) if parsed_line[13] else 0,
                                             LPC_PAID=float(parsed_line[14]) if parsed_line[14] else 0,
                                             LPC_DUE=float(parsed_line[15]) if parsed_line[15] else 0,
                                             FORMAT=parsed_line[16],
                                             TENTATIVE_FORECLOSURE_AMT=float(parsed_line[17]) if parsed_line[17] else 0,
                                             PREPAYPENALTY_PERCENT=float(parsed_line[18]) if parsed_line[18] else 0,
                                             PRINCIPAL_BALANCE=float(parsed_line[19]) if parsed_line[19] else 0,
                                             INSTALLMENT=float(parsed_line[20]) if parsed_line[20] else 0,
                                             PREPAYMENT_PENALTY=float(parsed_line[21]) if parsed_line[21] else 0,
                                             UNBILLED_INSTALLMENT=float(parsed_line[22]) if parsed_line[22] else 0,
                                             OVERDUE_CHARGES=float(parsed_line[23]) if parsed_line[23] else 0,
                                             ADVICE_OUTSTANDING_REPAYMENT_FEE=float(parsed_line[24]) if parsed_line[24] else 0,
                                             TOTAL_RECEIVABLE=float(parsed_line[25]) if parsed_line[25] else 0,
                                             NET_TOTAL=float(parsed_line[26]) if parsed_line[26] else 0,
                                             REFUNDS=float(parsed_line[27]) if parsed_line[27] else 0,
                                             CLOSURE_DATE=datetime.strptime(parsed_line[28], '%d-%m-%Y').strftime('%Y-%m-%d'),
                                             ACCRUED_PENAL_INTEREST=parsed_line[29])


