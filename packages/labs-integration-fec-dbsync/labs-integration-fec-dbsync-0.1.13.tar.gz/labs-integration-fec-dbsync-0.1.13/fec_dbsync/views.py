
import datetime
import json
import cx_Oracle
import traceback
from base_app import utils as base_app_utils
from django.db.models import Sum, Max
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from fec_dbsync import models as fec_dbsync_models
from fec_lms.models import CIFGenDetailsModel
from fec_dbsync import serializers as fec_dbsync_serializers
from fec_dbsync.utils import get_transaction_history
from . import utils as Utils


class GetLmsData(APIView):
    """
    API to get lms data
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        :param request:
        :return:
        """
        rq_srl = fec_dbsync_serializers.GetLmsDataRequestSerializer(
            data=request.data)
        if rq_srl.is_valid():
            # get objects
            try:
                general_account_obj = get_object_or_404(
                    klass=fec_dbsync_models.GeneralAccount, LOAN_ACCT_NUM=rq_srl.data.get(
                        'contract_id')
                )
            except Http404 as e:
                error = {'type': 's', 'reason': repr(e)}
                return base_app_utils.response(data=None, code=status.HTTP_400_BAD_REQUEST, error=error)

            try:
                robo_eit_obj = get_object_or_404(
                    klass=fec_dbsync_models.RoboEitView, LOAN_ACCT_NUM=rq_srl.data.get(
                        'contract_id')
                )
            except Http404 as e:
                error = {'type': 's', 'reason': repr(e)}
                return base_app_utils.response(data=None, code=status.HTTP_400_BAD_REQUEST, error=error)

            try:
                robo_chat_object = get_object_or_404(
                    klass=fec_dbsync_models.RoboChatView, LOAN_ACCT_NUM=rq_srl.data.get(
                        'contract_id'),
                    CHARGE_TYPE="MISC2"
                )
            except Http404 as e:
                error = {'type': 's', 'reason': repr(e)}
                return base_app_utils.response(data=None, code=status.HTTP_400_BAD_REQUEST, error=error)

            rorbo_clelarsh_after_business_date = fec_dbsync_models.RoboClelarshView.objects.filter(
                LOAN_ACCT_NUM=rq_srl.data.get('contract_id'),
                REP_SHDL_DATE__gte=rq_srl.data.get('business_date')
            ).order_by('REP_SHDL_DATE')

            robo_idt_objects = fec_dbsync_models.RoboIdtView.objects.filter(
                LOAN_ACCT_NUM=rq_srl.data.get('contract_id')
            ).values('DMD_EFF_DATE').annotate(DMD_AMT_SUM=Sum('DMD_AMT')).annotate(
                TOT_ADJ_AMT_SUM=Sum('TOT_ADJ_AMT')).order_by('DMD_EFF_DATE')

            robo_lrs_obj = fec_dbsync_models.RoboLrsView.objects.filter(
                LOAN_ACCT_NUM=rq_srl.data.get('contract_id')
            )

            robo_repay_objects = fec_dbsync_models.RoboRepayUplView.objects.filter(
                LOAN_ACCT_NUM=rq_srl.data.get('contract_id'), FAIL_FLG='N'
            )

            # outstanding amount
            outstanding_amount = abs(general_account_obj.CURRENT_BAL)

            # no of entries in clelarsh after business date for given loan account number
            remaining_months = rorbo_clelarsh_after_business_date.count()

            upcoming_installation_payment_due_date = Utils.get_upcoming_due_date(
                robo_lrs_obj)
            monthly_installment = Utils.get_monthly_installment(robo_lrs_obj)

            overdue_amount, months_overdue, total_installments_paid, last_inst_obj = \
                Utils.calculate_total_overdue_amount(
                    robo_idt_objects, robo_eit_obj, robo_chat_object)
            overdue_fee = Utils.get_overdue_fee(robo_chat_object)
            total_overdue_amount = overdue_amount + overdue_fee
            # repayment_fee = get_repayment_fee()

            repayment_information = Utils.get_repayments_info(
                robo_idt_objects, rq_srl.data.get("business_date"))

            # upcoming payment amount
            upcoming_emi = 0 if rorbo_clelarsh_after_business_date.count() == 0 else \
                rorbo_clelarsh_after_business_date[0].TOTAL_FLOW
            upcoming_payment_amount = upcoming_emi + overdue_amount

            total_payment_amount = total_overdue_amount + monthly_installment

            current_principle = 0
            current_interest = 0
            current_repayment = 0
            current_outstanding = 0
            if rorbo_clelarsh_after_business_date.count() != 0:
                current_principle = rorbo_clelarsh_after_business_date[0].PRIN_CMP
                current_interest = rorbo_clelarsh_after_business_date[0].INT_CMP
                current_repayment = rorbo_clelarsh_after_business_date[0].CHRG_CMP
                current_outstanding = int(
                    current_principle) + int(current_interest) + int(current_repayment)

            prdem_idtobjects = fec_dbsync_models.RoboIdtView.objects.filter(
                LOAN_ACCT_NUM=rq_srl.data.get('contract_id'), DMD_FLOW_ID='PRDEM'
            ).values('DMD_EFF_DATE').annotate(DMD_AMT_SUM=Sum('DMD_AMT')).annotate(
                TOT_ADJ_AMT_SUM=Sum('TOT_ADJ_AMT')).order_by('DMD_EFF_DATE')
            indem_idtobjects = fec_dbsync_models.RoboIdtView.objects.filter(
                LOAN_ACCT_NUM=rq_srl.data.get('contract_id'), DMD_FLOW_ID='INDEM'
            ).values('DMD_EFF_DATE').annotate(DMD_AMT_SUM=Sum('DMD_AMT')).annotate(
                TOT_ADJ_AMT_SUM=Sum('TOT_ADJ_AMT')).order_by('DMD_EFF_DATE')
            pidem_idtobjects = fec_dbsync_models.RoboIdtView.objects.filter(
                LOAN_ACCT_NUM=rq_srl.data.get('contract_id'), DMD_FLOW_ID='PIDEM'
            ).values('DMD_EFF_DATE').annotate(DMD_AMT_SUM=Sum('DMD_AMT')).annotate(
                TOT_ADJ_AMT_SUM=Sum('TOT_ADJ_AMT')).order_by('DMD_EFF_DATE')

            principle_overdue = Utils.get_overdue_amount(prdem_idtobjects)
            interest_overdue = Utils.get_overdue_amount(indem_idtobjects)
            penal_overdue = Utils.get_overdue_amount(pidem_idtobjects)

            repayment_overdue = robo_chat_object.CHARGE_OUTSTANDING
            excess_amounts = ""
            next_month_emi = current_outstanding

            # payment history
            payment_history = fec_dbsync_serializers.RepaySerializer(
                robo_repay_objects, many=True)

            transaction_history = get_transaction_history(
                rq_srl.data.get('contract_id'))
            res = []
            for txn in transaction_history:
                d = dict()
                d['transactionDate'] = txn['repay_object'].PAID_DATE
                d['paidAmt'] = txn['repay_object'].PAID_AMT
                d['referenceNumber'] = txn['repay_object'].REF_NUM
                d['paymentMethod'] = Utils.get_payment_mode(
                    txn['repay_object'])
                d['adjustmentDate'] = txn['last_adj_date']
                d['bookDate'] = txn['repay_object'].PAID_DATE  # TODO
                res.append(d)
            repayment_tab_data = dict()
            repayment_tab_data['transaction_history'] = res

            current = dict()
            current['currentPrinciple'] = current_principle
            current['currentInterest'] = current_interest
            current['currentRepayment'] = current_repayment
            current['currentOutstanding'] = current_outstanding
            current['interestRate'] = ""
            repayment_tab_data["current"] = current

            overdue = dict()
            overdue['principleOverdue'] = principle_overdue
            overdue['interestOverdue'] = interest_overdue
            overdue['overdueDuePenalInterest'] = penal_overdue
            overdue['repaymentFeeOverdue'] = repayment_overdue
            overdue['excessAmounts'] = excess_amounts
            overdue['nextMonthApi'] = next_month_emi
            overdue['earlyTerminationAmount'] = ""
            overdue['overdueOutstanding'] = principle_overdue + \
                interest_overdue + penal_overdue
            repayment_tab_data['overdue'] = overdue
            repayment_tab_data['total'] = {
                "totalOutstanding": outstanding_amount}
            repayment_tab_data['repaymentStatus'] = repayment_information

            response = {
                'outstanding_amount': outstanding_amount, 'remaining_months': remaining_months,
                'upcoming_installation_payment_due_date': upcoming_installation_payment_due_date,
                'overdue_amount': overdue_amount, 'overdue_fee': overdue_fee, 'total_overdue_amount':
                    total_overdue_amount, 'upcoming_payment_amount': upcoming_payment_amount, 'total_payment_amount':
                    total_payment_amount, 'payment_history': payment_history.data,
                'repayment_information': repayment_information,
                'no_of_months_overdue': months_overdue, "monthly_installment": monthly_installment,
                'repayment_tab_data': repayment_tab_data
            }
            return base_app_utils.response(data=response, code=status.HTTP_200_OK, error='')
        error = rq_srl.errors
        error.update({'type': 's', 'reason': 'bad request'})
        return base_app_utils.response(data=None, code=status.HTTP_400_BAD_REQUEST, error=error)


class GetRoboActiveApps(APIView):
    """
    API to get lms data
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            rq_srl = fec_dbsync_serializers.GetActiveAppsRequestSerializer(
                data=request.data)
            if rq_srl.is_valid():
                # get objects
                cifgen_objects = CIFGenDetailsModel.objects.filter(
                    IDNUMBER=rq_srl.data.get('national_id'))
                count = 0
                for cifgen_object in cifgen_objects:
                    print(cifgen_object.CIF_ID)
                    general_account_obj = fec_dbsync_models.GeneralAccount.objects.filter(
                        CIF_ID=cifgen_object.CIF_ID)
                    try:
                        outstanding_amount = abs(
                            general_account_obj[0].CURRENT_BAL)
                    except:
                        outstanding_amount = 0
                    if outstanding_amount != 0:
                        count = count+1

                response = {
                    'totalActiveLoanAppsRobo': count
                }
                return base_app_utils.response(data=response, code=status.HTTP_200_OK, error='')
            error = rq_srl.errors
            error.update({'type': 's', 'reason': 'bad request'})
            return base_app_utils.response(data=None, code=status.HTTP_400_BAD_REQUEST, error=error)
        except Exception as e:
            print(e)
            return base_app_utils.response(data=None, code=status.HTTP_400_BAD_REQUEST, error='')


class GetRepaymentSchedule(APIView):
    """
    API to repayment schedule pdf
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        rq_srl = fec_dbsync_serializers.GetLmsDataRequestSerializer(
            data=request.data)
        if rq_srl.is_valid():
            robo_clelarsh = fec_dbsync_models.RoboClelarshView.objects.filter(
                LOAN_ACCT_NUM=rq_srl.data.get('contract_id')
            ).order_by('REP_SHDL_DATE')
            repayment_schedule = list()
            try:
                general_account = get_object_or_404(
                    klass=fec_dbsync_models.GeneralAccount, LOAN_ACCT_NUM=rq_srl.data.get(
                        'contract_id')
                )
            except Http404:
                return base_app_utils.response(data=None, code=status.HTTP_200_OK, error="No Data Available")
            try:
                maturity_date = datetime.datetime.strptime(str(general_account.MATURITY_DATE), '%Y-%m-%d') \
                    .strftime('%d-%m-%Y')
            except:
                maturity_date = general_account.MATURITY_DATE
            for clelarsh in robo_clelarsh:
                outstanding_principle = fec_dbsync_models.RoboClelarshView.objects.filter(
                    LOAN_ACCT_NUM=rq_srl.data.get('contract_id'), SRL_NUM__gt=clelarsh.SRL_NUM
                ).aggregate(Sum('PRIN_CMP'))
                try:
                    repayment_schedule_date = datetime.datetime.strptime(str(clelarsh.REP_SHDL_DATE), '%Y-%m-%d') \
                        .strftime('%d-%m-%Y')
                except:
                    repayment_schedule_date = clelarsh.REP_SHDL_DATE
                repayment_schedule.append({
                    'repayment_date': repayment_schedule_date,
                    'payable_principle': clelarsh.PRIN_CMP,
                    'payable_interest': clelarsh.INT_CMP,
                    'outstanding_principle': 0 if not outstanding_principle['PRIN_CMP__sum'] else outstanding_principle[
                        'PRIN_CMP__sum'],
                    'payable_collection_fee': clelarsh.CHRG_CMP,
                    'total_payable_amount': clelarsh.TOTAL_FLOW + clelarsh.CHRG_CMP,
                })
            response = {
                'repayment_schedule': repayment_schedule,
                'maturity_date': maturity_date
            }
            return base_app_utils.response(data=response, code=status.HTTP_200_OK, error='')
        error = rq_srl.errors
        error.update({'type': 's', 'reason': 'bad request'})
        return base_app_utils.response(data=None, code=status.HTTP_400_BAD_REQUEST, error=error)


class GenerateMISReport(APIView):
    """
    API to generate MIS report
    """

    def post(self, request):
        response = fec_dbsync_serializers.MISSerializer(data=request.data)
        if response.is_valid():
            try:
                mis_data = fec_dbsync_models.MISReportRequestTracking(
                    report_request=response.data.get('report'),
                    filters=json.dumps(response.data.get('filters')),
                    emails=json.dumps(response.data.get('emails')),
                    requester=response.data.get('requester')
                )
                mis_data.save()
                return base_app_utils.response({"message": "Request Received"}, status.HTTP_200_OK)
            except:
                return base_app_utils.response({"message": "Something went wrong"},
                                               status.HTTP_500_INTERNAL_SERVER_ERROR, error="error")
        return base_app_utils.response(response.errors, status.HTTP_400_BAD_REQUEST, error="error")


class DedupeCheck(APIView):
    def post(self, request):
        rq_srl = fec_dbsync_serializers.DedupeCheckRequestSerializer(
            data=request.data)
        if rq_srl.is_valid():
            try:
                response = Utils.get_data_from_oracle(rq_srl.data.get(
                    'national_id'), rq_srl.data.get('phone_number'))
                return base_app_utils.response(response[0], status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return base_app_utils.response({"message": "Something went wrong"},
                                               status.HTTP_500_INTERNAL_SERVER_ERROR, error="error")
        return base_app_utils.response(rq_srl.errors, status.HTTP_400_BAD_REQUEST, error="error")


class DedupeCheckRobo(APIView):
    def post(self, request):
        rq_srl = fec_dbsync_serializers.DedupeCheckRoboRequestSerializer(
            data=request.data)
        if rq_srl.is_valid():
            try:
                response = Utils.get_data_from_oracle_robo(rq_srl.data.get(
                    'p_Phone'), rq_srl.data.get('p_NID'), rq_srl.data.get('p_Product_Channel'))
                return base_app_utils.response(response[0], status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return base_app_utils.response({"message": "Something went wrong"},
                                               status.HTTP_500_INTERNAL_SERVER_ERROR, error="error")
        return base_app_utils.response(rq_srl.errors, status.HTTP_400_BAD_REQUEST, error="error")


class RetrieveReferences(APIView):
    def post(self, request):
        rq_srl = fec_dbsync_serializers.RetreiveReferencesRequestSerializer(
            data=request.data)
        if rq_srl.is_valid():
            try:
                response = Utils.get_references_from_oracle(
                    rq_srl.data.get('national_id'), rq_srl.data.get('phone_number'))
                return base_app_utils.response(response, status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return base_app_utils.response({"message": "Something went wrong"},
                                               status.HTTP_500_INTERNAL_SERVER_ERROR, error="error")
        return base_app_utils.response(rq_srl.errors, status.HTTP_400_BAD_REQUEST, error="error")


class CollectionsRepayment(APIView):
    def get(self, request):
        loan_acct_num = request.GET.get('loanAcctNum', None)
        business_date = request.GET.get('businessDate', None)
        if not business_date:
            business_date = datetime.date.today().strftime("%d-%m-%Y")
        if not loan_acct_num:
            return base_app_utils.response(data=None, code=status.HTTP_400_BAD_REQUEST,
                                           error="Missing loan account number.")
        try:
            repayments = []
            robo_clelarsh_objects = fec_dbsync_models.RoboClelarshView.objects.filter(
                LOAN_ACCT_NUM=loan_acct_num)
            for a in robo_clelarsh_objects:
                closing_principal = 0
                b = fec_dbsync_models.RoboClelarshView.objects.filter(LOAN_ACCT_NUM=loan_acct_num,
                                                                      SRL_NUM__gt=a.SRL_NUM)
                for object in b:
                    closing_principal = closing_principal + object.PRIN_CMP
                installment_number = a.SRL_NUM
                due_date = a.REP_SHDL_DATE
                total_installment_amount = a.PRIN_CMP + a.INT_CMP + a.CHRG_CMP
                repayment_fee = a.CHRG_CMP
                interest_component = a.INT_CMP
                principal_component = a.PRIN_CMP
                payload = {
                    "installmentNumber": installment_number,
                    "dueDate": due_date,
                    "totalInstallmentAmount": total_installment_amount,
                    "principalComponent": principal_component,
                    "interestComponent": interest_component,
                    "repaymentFee": repayment_fee,
                    "closing_principal": closing_principal
                }
                repayments.append(payload)

            return base_app_utils.response(data={"repayments": repayments})
        except Exception as e:
            import traceback
            return base_app_utils.response(data=None, code=status.HTTP_400_BAD_REQUEST, error=traceback.format_exc())


class CollectionsStatement(APIView):
    def get(self, request):
        loan_acct_num = request.GET.get('loanAcctNum', None)
        if not loan_acct_num:
            return base_app_utils.response(data=None, code=status.HTTP_400_BAD_REQUEST, error=None)
        try:
            robo_lrs_obj = fec_dbsync_models.RoboLrsView.objects.filter(
                LOAN_ACCT_NUM=loan_acct_num
            )

            robo_idt_objects = fec_dbsync_models.RoboIdtView.objects.filter(
                LOAN_ACCT_NUM=loan_acct_num
            ).values('DMD_EFF_DATE').annotate(DMD_AMT_SUM=Sum('DMD_AMT')).annotate(
                TOT_ADJ_AMT_SUM=Sum('TOT_ADJ_AMT')).order_by('DMD_EFF_DATE')

            robo_cxl = fec_dbsync_models.RoboCxlView.objects.filter(
                LOAN_ACCT_NUM=loan_acct_num, EVENT_ID='MISC2')

            robo_clelarsh = fec_dbsync_models.RoboClelarshView.objects.filter(
                LOAN_ACCT_NUM=loan_acct_num)

            monthly_installment = Utils.get_monthly_installment(robo_lrs_obj)

            months_overdue = Utils.calculate_overdue_terms(robo_idt_objects)

            cxl_actual_amt_coll = robo_cxl[0].ACTUAL_AMT_COLL if robo_cxl else 0

            installment_amount = robo_clelarsh[0].TOTAL_FLOW if robo_clelarsh else 0

            statements = []

            list_schedules = fec_dbsync_models.RoboIdtView.objects.filter(
                LOAN_ACCT_NUM=loan_acct_num)

            schedule_numbers = set()
            for schedule in list_schedules:
                schedule_numbers.add(schedule.SHDL_NUM)

            for schedule_number in schedule_numbers:
                due_dates = fec_dbsync_models.RoboIdtView.objects.filter(LOAN_ACCT_NUM=loan_acct_num,
                                                                         SHDL_NUM=schedule_number)

                max_indem = fec_dbsync_models.RoboIdtView.objects.filter(LOAN_ACCT_NUM=loan_acct_num,
                                                                         DMD_FLOW_ID="INDEM",
                                                                         SHDL_NUM=schedule_number).aggregate(
                    Max('DMD_SRL_NUM'))
                max_prdem = fec_dbsync_models.RoboIdtView.objects.filter(LOAN_ACCT_NUM=loan_acct_num,
                                                                         DMD_FLOW_ID="PRDEM",
                                                                         SHDL_NUM=schedule_number).aggregate(
                    Max('DMD_SRL_NUM'))
                max_pidem = fec_dbsync_models.RoboIdtView.objects.filter(LOAN_ACCT_NUM=loan_acct_num,
                                                                         DMD_FLOW_ID="PIDEM",
                                                                         SHDL_NUM=schedule_number).aggregate(
                    Max('DMD_SRL_NUM'))

                max_interest_row = fec_dbsync_models.RoboIdtView.objects.filter(LOAN_ACCT_NUM=loan_acct_num,
                                                                                DMD_FLOW_ID="INDEM",
                                                                                DMD_SRL_NUM=max_indem[
                                                                                    'DMD_SRL_NUM__max'])
                max_principal_row = fec_dbsync_models.RoboIdtView.objects.filter(LOAN_ACCT_NUM=loan_acct_num,
                                                                                 DMD_FLOW_ID="PRDEM",
                                                                                 DMD_SRL_NUM=max_prdem[
                                                                                     'DMD_SRL_NUM__max'])
                max_late_payment_row = fec_dbsync_models.RoboIdtView.objects.filter(LOAN_ACCT_NUM=loan_acct_num,
                                                                                    DMD_FLOW_ID="PIDEM",
                                                                                    DMD_SRL_NUM=max_pidem[
                                                                                        'DMD_SRL_NUM__max'])
                due_date = due_dates[0].DMD_EFF_DATE if due_dates else ''
                interest = max_interest_row[0].DMD_AMT if max_interest_row else 0
                principal = max_principal_row[0].DMD_AMT if max_principal_row else 0
                late_payment = max_late_payment_row[0].DMD_AMT if max_late_payment_row else 0

                tot_adj_amt_indem = max_interest_row[0].TOT_ADJ_AMT if max_interest_row else 0
                tot_adj_amt_prdem = max_principal_row[0].TOT_ADJ_AMT if max_principal_row else 0
                tot_adj_amt_pidem = max_late_payment_row[0].TOT_ADJ_AMT if max_late_payment_row else 0

                last_adj_date_indem = max_interest_row[0].LAST_ADJ_DATE if max_interest_row else datetime.date.min
                last_adj_date_prdem = max_principal_row[0].LAST_ADJ_DATE if max_principal_row else datetime.date.min
                last_adj_date_pidem = max_late_payment_row[
                    0].LAST_ADJ_DATE if max_late_payment_row else datetime.date.min

                last_adj_date = max(last_adj_date_indem if last_adj_date_indem else datetime.date.min,
                                    last_adj_date_prdem if last_adj_date_prdem else datetime.date.min,
                                    last_adj_date_pidem if last_adj_date_pidem else datetime.date.min)

                robo_clelarsh = fec_dbsync_models.RoboRepayUplView.objects.filter(LOAN_ACCT_NUM=loan_acct_num,
                                                                                  PAID_DATE__lte=last_adj_date) \
                    .order_by('-PAID_DATE').first()

                receipt_date = robo_clelarsh.PAID_DATE if robo_clelarsh else ''
                receipt_number = robo_clelarsh.REF_NUM if robo_clelarsh else ''

                statement = {
                    "dueDate": due_date,
                    "installmentAmount": installment_amount,
                    "interest": interest,
                    "principalAmount": principal,
                    "latePaymentFee": late_payment,
                    "repaymentFee": 12000,
                    "totalAmount": interest + principal + late_payment + 12000,
                    "paidAmount": tot_adj_amt_indem + tot_adj_amt_prdem + tot_adj_amt_pidem + cxl_actual_amt_coll,
                    "paymentDate": last_adj_date,
                    "receiptDate": receipt_date,
                    "receiptNumber": receipt_number
                }
                statements.append(statement)

            payload = {
                "loanDetails": {
                    "installmentOverdue": months_overdue,
                    "instrumentAmount": monthly_installment
                },
                "statementOfAccount": statements
            }

            return base_app_utils.response(data=payload)
        except Exception as e:
            import traceback
            return base_app_utils.response(data=None, code=status.HTTP_400_BAD_REQUEST, error=traceback.format_exc())


class CollectionsPayment(APIView):
    def get(self, request):
        loan_acct_num = request.GET.get('loanAcctNum', None)
        if not loan_acct_num:
            return base_app_utils.response(data=None, code=status.HTTP_400_BAD_REQUEST, error=None)
        try:
            response = {}
            payments = []
            fdv_objects = fec_dbsync_models.RoboCollectionFdv.objects.filter(
                APPL_ID=loan_acct_num)
            for fdv_obj in fdv_objects:
                payload = {
                    "payment": {
                        "prinicipalAmount": fdv_obj.PRINCIPAL_PAID,
                        "interestAmount": fdv_obj.INTEREST_PAID,
                        "lpcAmount": fdv_obj.LPC_PAID,
                        "bccAmount": fdv_obj.BCC_PAID,
                        "otherAmount": fdv_obj.OTHER_PAID,
                        "totalAmount": fdv_obj.PRINCIPAL_PAID + fdv_obj.INTEREST_PAID + fdv_obj.LPC_PAID + fdv_obj.BCC_PAID + fdv_obj.OTHER_PAID
                    },
                    "outstanding": {
                        "prinicipalAmount": fdv_obj.PRINCIPAL_DUE,
                        "interestAmount": fdv_obj.INTEREST_DUE,
                        "lpcAmount": fdv_obj.LPC_DUE,
                        "bccAmount": fdv_obj.BCC_DUE,
                        "otherAmount": fdv_obj.OTHER_DUE,
                        "totalAmount": fdv_obj.PRINCIPAL_DUE + fdv_obj.INTEREST_DUE + fdv_obj.LPC_DUE + fdv_obj.BCC_DUE + fdv_obj.OTHER_DUE
                    }
                }
                payments.append(payload)
            response["payments"] = payments
            response["lastPaymentMadeOn"] = fec_dbsync_models.RoboRepayUplView.objects.filter(
                LOAN_ACCT_NUM=loan_acct_num).aggregate(lastPaymentMadeOn=Max('PAID_DATE')).get("lastPaymentMadeOn")
            if type(response["lastPaymentMadeOn"]) == str:
                response["lastPaymentMadeOn"] = response["lastPaymentMadeOn"][-2:] + response["lastPaymentMadeOn"][
                    4:-2] + response[
                    "lastPaymentMadeOn"][:4]
            if type(response["lastPaymentMadeOn"]) == datetime.date:
                response["lastPaymentMadeOn"] = datetime.datetime.strptime(str(response["lastPaymentMadeOn"]),
                                                                           '%Y-%m-%d').strftime('%d-%m-%Y')
            return base_app_utils.response(data=response)
        except Exception as e:
            import traceback
            return base_app_utils.response(data=None, code=status.HTTP_400_BAD_REQUEST, error=traceback.format_exc())


class CollectionsSummary(APIView):
    def get(self, request):
        loan_acct_num = request.GET.get('loanAcctNum', None)
        business_date = request.GET.get('businessDate', None)
        if not business_date:
            business_date = datetime.date.today().strftime("%d-%m-%Y")
        if not loan_acct_num:
            return base_app_utils.response(data=None, code=status.HTTP_400_BAD_REQUEST, error=None)
        try:
            try:
                robo_eit_obj = get_object_or_404(
                    klass=fec_dbsync_models.RoboEitView, LOAN_ACCT_NUM=loan_acct_num
                )
            except Http404 as e:
                error = {'type': 's', 'reason': repr(e)}
                return base_app_utils.response(data=None, code=status.HTTP_400_BAD_REQUEST, error=error)

            try:
                robo_chat_object = get_object_or_404(
                    klass=fec_dbsync_models.RoboChatView, LOAN_ACCT_NUM=loan_acct_num,
                    CHARGE_TYPE="MISC2"
                )
            except Http404 as e:
                error = {'type': 's', 'reason': repr(e)}
                return base_app_utils.response(data=None, code=status.HTTP_400_BAD_REQUEST, error=error)

            robo_idt_objects = fec_dbsync_models.RoboIdtView.objects.filter(
                LOAN_ACCT_NUM=loan_acct_num, DMD_EFF_DATE__lte=business_date
            ).order_by("DMD_SRL_NUM").values('DMD_EFF_DATE').annotate(DMD_AMT_SUM=Sum('DMD_AMT')).annotate(
                TOT_ADJ_AMT_SUM=Sum('TOT_ADJ_AMT'))

            robo_lrs_obj = fec_dbsync_models.RoboLrsView.objects.filter(
                LOAN_ACCT_NUM=loan_acct_num
            )

            robo_repay_objects = fec_dbsync_models.RoboRepayUplView.objects.filter(
                LOAN_ACCT_NUM=loan_acct_num, FAIL_FLG='N'
            ).order_by('-SRL_NUM')

            fdv_objects = fec_dbsync_models.RoboCollectionFdv.objects.filter(
                APPL_ID=loan_acct_num)

            monthly_installment = Utils.get_monthly_installment(robo_lrs_obj)

            next_due_date = Utils.get_upcoming_due_date(robo_lrs_obj)

            overdue_amount, months_overdue, total_installments_paid, last_inst_obj = \
                Utils.calculate_total_overdue_amount(
                    robo_idt_objects, robo_eit_obj, robo_chat_object)
            total_repayment_fee = fec_dbsync_models.RoboChatView.objects.filter(
                LOAN_ACCT_NUM=loan_acct_num,
                CHARGE_TYPE="MISC2"
            ).aggregate(
                Sum('CHRGE_AMT_COLLECTED')
            )
            repayment_information = Utils.get_repayments_info(
                robo_idt_objects, business_date)

            interest_overdue_obj = fec_dbsync_models.RoboIdtView.objects.filter(
                LOAN_ACCT_NUM=loan_acct_num, DMD_EFF_DATE__lte=business_date, DMD_FLOW_ID=Utils.fec_dbsync_cons.INDEM
            ).aggregate(DMD_AMT_SUM=Sum('DMD_AMT'), TOT_ADJ_AMT_SUM=Sum('TOT_ADJ_AMT'))

            principal_overdue_obj = fec_dbsync_models.RoboIdtView.objects.filter(
                LOAN_ACCT_NUM=loan_acct_num, DMD_EFF_DATE__lte=business_date, DMD_FLOW_ID=Utils.fec_dbsync_cons.PRDEM
            ).aggregate(DMD_AMT_SUM=Sum('DMD_AMT'), TOT_ADJ_AMT_SUM=Sum('TOT_ADJ_AMT'))

            penalty_overdue_obj = fec_dbsync_models.RoboIdtView.objects.filter(
                LOAN_ACCT_NUM=loan_acct_num, DMD_EFF_DATE__lte=business_date, DMD_FLOW_ID=Utils.fec_dbsync_cons.PIDEM
            ).aggregate(DMD_AMT_SUM=Sum('DMD_AMT'), TOT_ADJ_AMT_SUM=Sum('TOT_ADJ_AMT'))

            charge_calc = fec_dbsync_models.RoboChatView.objects.filter(
                LOAN_ACCT_NUM=loan_acct_num).aggregate(TOTAL_SYS_CALC_CHRGE_AMT=Sum('SYS_CALC_CHRGE_AMT'),
                                                       TOTAL_USER_CALC_CHRGE_AMT=Sum(
                                                           'USER_CALC_CHRGE_AMT'),
                                                       TOTAL_CHRGE_AMT_COLLECTED=Sum('CHRGE_AMT_COLLECTED'))

            principal_outstanding = None
            interest_outstanding = None
            tentative_foreclosure = None
            interest_overdue = None
            principal_overdue = None
            penalty_overdue = None
            last_payment_date = None
            last_payment_amount = None
            total_payment_amount = 0

            if robo_repay_objects:
                last_payment_amount = robo_repay_objects[0].PAID_AMT
                for robo_repay_object in robo_repay_objects:
                    total_payment_amount += robo_repay_object.PAID_AMT
                try:
                    last_payment_date = datetime.datetime.strptime(str(robo_repay_objects[0].PAID_DATE), '%Y-%m-%d') \
                        .strftime('%d-%m-%Y')
                except:
                    last_payment_date = robo_repay_objects[0].PAID_DATE
            if fdv_objects:
                fdv_objects = fdv_objects[0]
                principal_outstanding = fdv_objects.PRINCIPAL_BALANCE
                interest_outstanding = fdv_objects.UNBILLED_INSTALLMENT
                tentative_foreclosure = fdv_objects.TENTATIVE_FORECLOSURE_AMT

            if interest_overdue_obj and interest_overdue_obj.get("DMD_AMT_SUM", -1) > -1 and interest_overdue_obj.get(
                    "TOT_ADJ_AMT_SUM", -1) > -1:
                interest_overdue = interest_overdue_obj.get(
                    "DMD_AMT_SUM") - interest_overdue_obj.get("TOT_ADJ_AMT_SUM")

            if principal_overdue_obj and principal_overdue_obj.get("DMD_AMT_SUM",
                                                                   -1) > -1 and principal_overdue_obj.get(
                    "TOT_ADJ_AMT_SUM", -1) > -1:
                principal_overdue = principal_overdue_obj.get("DMD_AMT_SUM") - principal_overdue_obj.get(
                    "TOT_ADJ_AMT_SUM")
            if penalty_overdue_obj and penalty_overdue_obj.get("DMD_AMT_SUM") and penalty_overdue_obj.get(
                "TOT_ADJ_AMT_SUM") and penalty_overdue_obj.get("DMD_AMT_SUM", -1) > -1 and penalty_overdue_obj.get(
                    "TOT_ADJ_AMT_SUM", -1) > -1:
                penalty_overdue = penalty_overdue_obj.get(
                    "DMD_AMT_SUM") - penalty_overdue_obj.get("TOT_ADJ_AMT_SUM")

            try:
                general_account = fec_dbsync_models.GeneralAccount.objects.filter(
                    LOAN_ACCT_NUM=loan_acct_num
                ).first()
            except Exception as e:
                pass

            total_charges = 0
            if charge_calc:
                total_charges = charge_calc.get("TOTAL_USER_CALC_CHRGE_AMT") if \
                    charge_calc.get("TOTAL_USER_CALC_CHRGE_AMT") and charge_calc.get("TOTAL_SYS_CALC_CHRGE_AMT") and \
                    charge_calc.get("TOTAL_USER_CALC_CHRGE_AMT") > charge_calc.get("TOTAL_SYS_CALC_CHRGE_AMT") else \
                    charge_calc.get("TOTAL_SYS_CALC_CHRGE_AMT")
                if charge_calc.get("TOTAL_CHRGE_AMT_COLLECTED") and total_charges:
                    total_charges -= charge_calc.get(
                        "TOTAL_CHRGE_AMT_COLLECTED")
            payload = {
                "overdueDetails": {
                    "overdueAmount": overdue_amount + total_charges,
                    "bucket": general_account.DPD_CNTR / 30,
                    "dpd": general_account.DPD_CNTR,
                    "noOfOverdueInstallements": months_overdue,
                    "interestOverdue": interest_overdue,
                    "chargesOverdue": total_charges,
                    "principalOverdue": principal_overdue,
                    "penaltyInterestOverdue": penalty_overdue,
                    "totalPenaltyInterest ": penalty_overdue_obj.get("DMD_AMT_SUM") if penalty_overdue_obj else "",
                    "brokenPromiseIndicator": "",
                    "brokenPromiseCounter": ""
                },
                "repaymentStatus": repayment_information[0]['payment_status'] if repayment_information else None,
                "lastPaymentDateDefault": repayment_information[0]['payment_date'] if repayment_information else None,
                "clientInformation": {
                    "currentInstallementStatus": "Due" if last_inst_obj and last_inst_obj['DMD_AMT_SUM'] -
                    last_inst_obj[
                        'TOT_ADJ_AMT_SUM'] > 0 else "Paid" if last_inst_obj else ""
                },
                "loanDetails": {
                    "nextOverdueDate": next_due_date,
                    "totalInstallementAmount": monthly_installment + Utils.fec_dbsync_cons.PROCESSING_FEE
                    if monthly_installment else None,
                    "repaymentFee": "12000",
                    "sumOfRepaymentFee": total_repayment_fee['CHRGE_AMT_COLLECTED__sum']
                },
                "accountSummary": {
                    "balanceO/S": principal_outstanding + interest_outstanding
                    if principal_outstanding and interest_outstanding else None,
                    "principalO/S": principal_outstanding,
                    "interestO/S": interest_outstanding,
                    "tentativeForeclosure": tentative_foreclosure,
                    "accountStatus": "",
                    "lastPaymentDate": last_payment_date,
                    "lastPaymentAmount": last_payment_amount,
                    "totalPaidAmount": total_payment_amount,
                    "totalPaidNoOfInstallments ": total_installments_paid
                }
            }
            return base_app_utils.response(data=payload)
        except Exception as e:
            import traceback
            return base_app_utils.response(data=None, code=status.HTTP_400_BAD_REQUEST, error=traceback.format_exc())


class CollectionsForeClosure(APIView):
    def get(self, request):
        loan_acct_num = request.GET.get('loanAcctNum', None)
        if not loan_acct_num:
            return base_app_utils.response(data=None, code=status.HTTP_400_BAD_REQUEST, error=None)
        try:
            fdv_obj = fec_dbsync_models.RoboCollectionFdv.objects.filter(
                APPL_ID=loan_acct_num).first()
            if fdv_obj:
                try:
                    closure_date = datetime.datetime.strptime(str(fdv_obj.CLOSURE_DATE), '%Y-%m-%d') \
                        .strftime('%d-%m-%Y')
                except:
                    closure_date = fdv_obj.CLOSURE_DATE
                payload = {
                    "penaltyInterestPaid": fdv_obj.PREPAYMENT_PENALTY,
                    "due": fdv_obj.PRINCIPAL_DUE + fdv_obj.INTEREST_DUE + fdv_obj.LPC_DUE + fdv_obj.BCC_DUE + fdv_obj.OTHER_DUE,
                    "principalBalance": fdv_obj.PRINCIPAL_BALANCE,
                    "installment": fdv_obj.INSTALLMENT,
                    "prepaymentPenalty": fdv_obj.PREPAYMENT_PENALTY,
                    "unbilledInstallment": fdv_obj.UNBILLED_INSTALLMENT,
                    "overdueCharges": fdv_obj.OVERDUE_CHARGES,
                    "totalReceivable": fdv_obj.TOTAL_RECEIVABLE,
                    "netTotal": fdv_obj.NET_TOTAL,
                    "penaltyCalculatedOn": closure_date,
                    "closureDate": closure_date,
                    "refunds": fdv_obj.REFUNDS,
                    "totalPayable": fdv_obj.NET_TOTAL,
                    "penaltyInterestUnapplied": fdv_obj.ACCRUED_PENAL_INTEREST
                }
                return base_app_utils.response(data=payload)
            else:
                return base_app_utils.response(data=None, error="Record for loan account number doesn't exist.")
        except Exception as e:
            import traceback
            return base_app_utils.response(data=None, code=status.HTTP_400_BAD_REQUEST, error=traceback.format_exc())


class CollectionsStaCard(APIView):
    def get(self, request):
        loan_acct_num = request.GET.get('loanAcctNum', None)
        if not loan_acct_num:
            return base_app_utils.response(data=None, code=status.HTTP_400_BAD_REQUEST, error=None)
        try:
            payload = {"processingFee": Utils.fec_dbsync_cons.PROCESSING_FEE}
            ldt_obj = fec_dbsync_models.RoboIdtView.objects.filter(LOAN_ACCT_NUM=loan_acct_num). \
                order_by('-DMD_SRL_NUM').first()
            fdv_obj = fec_dbsync_models.RoboCollectionFdv.objects.filter(
                APPL_ID=loan_acct_num).first()
            gam_obj = fec_dbsync_models.GeneralAccount.objects.filter(
                LOAN_ACCT_NUM=loan_acct_num).first()
            lrs_obj = fec_dbsync_models.RoboLrsView.objects.filter(
                LOAN_ACCT_NUM=loan_acct_num).first()
            robo_repay_objects = fec_dbsync_models.RoboRepayUplView.objects.filter(LOAN_ACCT_NUM=loan_acct_num,
                                                                                   FAIL_FLG='N').order_by('-SRL_NUM')
            robo_idt_objects = fec_dbsync_models.RoboIdtView.objects.filter(
                LOAN_ACCT_NUM=loan_acct_num
            ).order_by("DMD_SRL_NUM").values('DMD_EFF_DATE').annotate(DMD_AMT_SUM=Sum('DMD_AMT')).annotate(
                TOT_ADJ_AMT_SUM=Sum('TOT_ADJ_AMT'))

            overdue_amount, months_overdue, total_installments_paid, last_inst_obj = \
                Utils.calculate_total_overdue_amount(robo_idt_objects)
            payment_history = fec_dbsync_serializers.RepaySerializer(
                robo_repay_objects, many=True)
            if not (ldt_obj or fdv_obj or gam_obj or lrs_obj or robo_repay_objects):
                return base_app_utils.response(data=None, error="Record for loan account number doesn't exist.")
            if ldt_obj:
                try:
                    overdue_date = datetime.datetime.strptime(str(ldt_obj.DMD_OVDU_DATE), '%Y-%m-%d') \
                        .strftime('%d-%m-%Y')
                except:
                    overdue_date = ldt_obj.DMD_OVDU_DATE
                payload["overdueDate"] = overdue_date
            if lrs_obj:
                payload["emiAmount"] = lrs_obj.FLOW_AMT + \
                    Utils.fec_dbsync_cons.PROCESSING_FEE
            if gam_obj:
                try:
                    loan_start_date = datetime.datetime.strptime(str(gam_obj.INST_START_DATE), '%Y-%m-%d') \
                        .strftime('%d-%m-%Y')
                except:
                    loan_start_date = gam_obj.INST_START_DATE
                payload["loanStartDate"] = loan_start_date
                payload["outstandingPrincipal"] = gam_obj.CURRENT_BAL
            if fdv_obj:
                payload["principalOverdue"] = fdv_obj.PRINCIPAL_DUE
                payload["interestOverdue"] = fdv_obj.INTEREST_DUE
                payload["lpcDue"] = fdv_obj.LPC_DUE
                payload["bccDue"] = fdv_obj.BCC_DUE
                payload["otherPenalty"] = fdv_obj.OTHER_DUE
                payload['earlyTerminationAmount'] = ""
            if payment_history.data:
                payload["latestPaymentDate"] = payment_history.data[0].get(
                    "payment_date")
            payload["missedPaymentCount"] = months_overdue
            return base_app_utils.response(data={"loanDetails": payload})
        except Exception as e:
            import traceback
            return base_app_utils.response(data=None, code=status.HTTP_400_BAD_REQUEST, error=traceback.format_exc())

# nguyenhuuvinh4 START


class GetDataCustConAdd(APIView):
    def post(self, request):
        rq_srl = fec_dbsync_serializers.GetDataCustConAddRequestSerializer(
            data=request.data)
        if rq_srl.is_valid():
            try:
                response = Utils.get_data_from_cust_con_add(
                    rq_srl.data.get('contract_number'))
                return base_app_utils.response(response, status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return base_app_utils.response({"message": "Something went wrong"},
                                               status.HTTP_500_INTERNAL_SERVER_ERROR, error="error")
        return base_app_utils.response(rq_srl.errors, status.HTTP_400_BAD_REQUEST, error="error")

class GetRegisAndActHiFromDWHRequestSerializer(APIView):
    print("tests GetRegisAndActHiFromDWHRequestSerializer")
    def post(self, request):
        rq_srl = fec_dbsync_serializers.GetRegisAndActHiFromDWHRequestSerializer(
            data=request.data)
        if rq_srl.is_valid():
            try:
                response = Utils.get_registration_and_act_hi_var_from_dwh(
                    rq_srl.data.get('appId'))
                return base_app_utils.response(response, status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return base_app_utils.response({"message": "Something went wrong"},
                                               status.HTTP_500_INTERNAL_SERVER_ERROR, error="error")
        return base_app_utils.response(rq_srl.errors, status.HTTP_400_BAD_REQUEST, error="error")
# nguyenhuuvinh4 END


class GetActiveLoanByAppIds(APIView):
    def post(self, request):
        rq_srl = fec_dbsync_serializers.GetActiveLoanByAppIdsRequestSerializer(
            data=request.data)
        if rq_srl.is_valid():
            try:
                response = Utils.getActiveLoanByAppIds(
                    rq_srl.data.get('app_ids'))
                return base_app_utils.response(response, status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return base_app_utils.response({"message": "Something went wrong"},
                                               status.HTTP_500_INTERNAL_SERVER_ERROR, error="error")
        return base_app_utils.response(rq_srl.errors, status.HTTP_400_BAD_REQUEST, error="error")


class FraudCheckRule(APIView):
    def post(self, request):
        fraudSrl = fec_dbsync_serializers.FraudSerializer(data=request.data)
        if fraudSrl.is_valid():
            try:
                result = {'dataFlags': {}, 'fraudFlag': False,
                          'softRejectFlag': False, 'freezeFlag': False, 'dataFraudFlag': False}
                productCode = ""
                if fraudSrl.data.get('productCode') != None:
                    productCode = fraudSrl.data.get('productCode')

                if fraudSrl.data.get('pincode') != None and bool(fraudSrl.data.get('pinCode')):
                    result = Utils.check(Utils.getFraudDataFromOracle(
                        'pinCode', fraudSrl.data.get('pincode'), False, productCode), result, 'pinCodeFraud')
                if fraudSrl.data.get('tsaCode') != None and bool(fraudSrl.data.get('tsaCode')):
                    result = Utils.check(Utils.getFraudDataFromOracle(
                        'salesAgentEmailId', fraudSrl.data.get('tsaCode'), False, productCode), result, 'tsaCodeFraud')
                if fraudSrl.data.get('dsaCode') != None and bool(fraudSrl.data.get('dsaCode')):
                    result = Utils.check(Utils.getFraudDataFromOracle(
                        'salesAgentEmailId', fraudSrl.data.get('dsaCode'), False, productCode), result, 'dsaCodeFraud')
                if fraudSrl.data.get('ccCode') != None and bool(fraudSrl.data.get('ccCode')):
                    result = Utils.check(Utils.getFraudDataFromOracle(
                        'salesAgentEmailId', fraudSrl.data.get('ccCode'), False, productCode), result, 'ccCodeFraud')
                if fraudSrl.data.get('temporaryProvince') != None and bool(fraudSrl.data.get('temporaryProvince')):
                    result = Utils.check(Utils.getFraudDataFromOracle('temporaryProvince', fraudSrl.data.get(
                        'temporaryProvince'), False, productCode), result, 'temporaryProvinceFraud')
                if fraudSrl.data.get('temporaryAddressCityDistrict') != None and bool(fraudSrl.data.get('temporaryAddressCityDistrict')):
                    result = Utils.check(Utils.getFraudDataFromOracle('temporaryCityDistrict', fraudSrl.data.get(
                        'temporaryAddressCityDistrict'), False, productCode), result, 'temporaryAddressCityDistrictFraud')
                if fraudSrl.data.get('temporaryAddressCityDistrictWard') != None and bool(fraudSrl.data.get('temporaryAddressCityDistrictWard')):
                    result = Utils.check(Utils.getFraudDataFromOracle('temporaryWard', fraudSrl.data.get(
                        'temporaryAddressCityDistrictWard'), False, productCode), result, 'temporaryAddressCityDistrictWardFraud')
                if fraudSrl.data.get('permanentAddressCity') != None and bool(fraudSrl.data.get('permanentAddressCity')):
                    result = Utils.check(Utils.getFraudDataFromOracle('permanentProvince', fraudSrl.data.get(
                        'permanentAddressCity'), False, productCode), result, 'permanentAddressCityFraud')
                if fraudSrl.data.get('permanentAddressCityDistrict') != None and bool(fraudSrl.data.get('permanentAddressCityDistrict')):
                    result = Utils.check(Utils.getFraudDataFromOracle('permanentDistrict', fraudSrl.data.get(
                        'permanentAddressCityDistrict'), False, productCode), result, 'permanentAddressCityDistrictFraud')
                if fraudSrl.data.get('permanentAddressCityDistrictWard') != None and bool(fraudSrl.data.get('permanentAddressCityDistrictWard')):
                    result = Utils.check(Utils.getFraudDataFromOracle('permanentWard', fraudSrl.data.get(
                        'permanentAddressCityDistrictWard'), False, productCode), result, 'permanentAddressCityDistrictWardFraud')
                if fraudSrl.data.get('phoneNumberCustomer') != None and bool(fraudSrl.data.get('phoneNumberCustomer')):
                    result = Utils.check(Utils.getFraudDataFromOracle('mobileNumber', fraudSrl.data.get(
                        'phoneNumberCustomer'), False, productCode), result, 'phoneNumberCustomerFraud')
                if fraudSrl.data.get('phoneNumberReferenceA') != None and bool(fraudSrl.data.get('phoneNumberReferenceA')):
                    result = Utils.check(Utils.getFraudDataFromOracle('referenceMobileNumber', fraudSrl.data.get(
                        'phoneNumberReferenceA'), False, productCode), result, 'phoneNumberReferenceAFraud')
                if fraudSrl.data.get('phoneNumberReferenceB') != None and bool(fraudSrl.data.get('phoneNumberReferenceB')):
                    result = Utils.check(Utils.getFraudDataFromOracle('referenceMobileNumber', fraudSrl.data.get(
                        'phoneNumberReferenceB'), False, productCode), result, 'phoneNumberReferenceBFraud')
                if fraudSrl.data.get('phoneNumberReferenceC') != None and bool(fraudSrl.data.get('phoneNumberReferenceC')):
                    result = Utils.check(Utils.getFraudDataFromOracle('referenceMobileNumber', fraudSrl.data.get(
                        'phoneNumberReferenceC'), False, productCode), result, 'phoneNumberReferenceCFraud')
                if fraudSrl.data.get('applicationID') != None and bool(fraudSrl.data.get('applicationID')):
                    result = Utils.check(Utils.getFraudDataFromOracle('applicationId', fraudSrl.data.get(
                        'applicationID'), False, productCode), result, 'applicationIDFraud')
                if fraudSrl.data.get('bankAccount') != None and bool(fraudSrl.data.get('bankAccount')):
                    result = Utils.check(Utils.getFraudDataFromOracle(
                        'beneficiaryAccountNumber', fraudSrl.data.get('bankAccount'), False, productCode), result, 'bankAccountFraud')
                if fraudSrl.data.get('nationalId') != None and bool(fraudSrl.data.get('nationalId')):
                    result = Utils.check(Utils.getFraudDataFromOracle(
                        'nationalId', fraudSrl.data.get('nationalId'), False, productCode), result, 'nationalIdFraud')
                if fraudSrl.data.get('personId') != None and bool(fraudSrl.data.get('personId')):
                    result = Utils.check(Utils.getFraudDataFromOracle(
                        'personId', fraudSrl.data.get('personId'), False, productCode), result, 'personIdFraud')
                if fraudSrl.data.get('locationCordinate') != None and bool(fraudSrl.data.get('locationCordinate')):
                    result = Utils.check(Utils.getFraudDataFromOracle('locationCordinate', fraudSrl.data.get(
                        'locationCordinate'), False, productCode), result, 'locationCordinateFraud')
                if fraudSrl.data.get('productId') != None and bool(fraudSrl.data.get('productId')):
                    result = Utils.check(Utils.getFraudDataFromOracle(
                        'productId', fraudSrl.data.get('productId'), False, productCode), result, 'productIdFraud')

                if fraudSrl.data.get('locationCordinate') != None and bool(fraudSrl.data.get('locationCordinate')):
                    dataList = Utils.getFraudDataFromOracle(None, None, True, productCode)
                    coordinates = fraudSrl.data.get('locationCordinate')
                    lat = coordinates.split(',')[0]
                    lon = coordinates.split(',')[1]
                    fraudRuleList = []
                    try:
                        for key in dataList:
                            if Utils.calculateDistance(lat, key.split(',')[0], lon, key.split(',')[1]) <= 500:
                                fraudRuleList.append(dataList[key])
                        result = Utils.check(
                            fraudRuleList, result, 'locationZoneFraud')
                    except Exception as e:
                        traceback.print_exc()
                return base_app_utils.response(data=result, code=status.HTTP_200_OK, error="")
            except Exception as e:
                print("Exception ", e)
                traceback.print_exc()
                return base_app_utils.response({"message": "Something went wrong"}, status.HTTP_500_INTERNAL_SERVER_ERROR, error="error")

        return base_app_utils.response(fraudSrl.errors, status.HTTP_400_BAD_REQUEST, error="error")


class GetBlacklistedAccounts(APIView):
    print("tests GetBlacklistedAccounts")
    def post(self, request):
        serialized_request = fec_dbsync_serializers.GetBlacklistedAccountsRequestSerializer(
            data=request.data)

        if not serialized_request.is_valid():
            return base_app_utils.response(serialized_request.errors, status.HTTP_400_BAD_REQUEST, error="error")

        try:
            bank_account = serialized_request.data.get('bank_account')
            blacklisted_bank_accounts = Utils.getBlackListedBankAccountsFromMySQL(
                bank_account)

            response = {
                "accounts": blacklisted_bank_accounts
            }

            return base_app_utils.response(response, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return base_app_utils.response({"message": "Something went wrong"},
                                           status.HTTP_500_INTERNAL_SERVER_ERROR, error="error")

class getAMLTableData(APIView):
    def post(self, request):
        try:
            payload = fec_dbsync_serializers.GetAMLCheckServiceRequestSerializer(data=request.data)
            
            if not payload.is_valid():
                return base_app_utils.response(payload.errors, status.HTTP_400_BAD_REQUEST, error="error")
            
            rawresponse = Utils.checkAMLService(payload)
            return base_app_utils.response(rawresponse, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return base_app_utils.response({"message": "Something went wrong"},
                                            status.HTTP_500_INTERNAL_SERVER_ERROR, error="error")

class blacklistPhoneNumber(APIView):
    def post(self, request):
        try:
            payload = fec_dbsync_serializers.CheckBlackListPhoneNumberRequestSerializer(data=request.data)
            
            if not payload.is_valid():
                return base_app_utils.response(payload.errors, status.HTTP_400_BAD_REQUEST, error="error")
            
            rawresponse = Utils.blacklistPhoneNumber(payload)
            return base_app_utils.response(rawresponse, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return base_app_utils.response({"message": "Something went wrong"},
                                            status.HTTP_500_INTERNAL_SERVER_ERROR, error="error")