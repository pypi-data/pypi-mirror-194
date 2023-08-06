from rest_framework import serializers

from fec_dbsync import models as fes_dbsync_models
from fec_dbsync import constants as fec_dbsync_cons


class GetLmsDataRequestSerializer(serializers.Serializer):
    """
    Get Lms Data Request Serializer
    """
    contract_id = serializers.CharField(required=True)
    business_date = serializers.DateField(required=True)
    start_date = serializers.DateField(required=False, allow_null=True)
    end_date = serializers.DateField(required=False, allow_null=True)

class GetActiveAppsRequestSerializer(serializers.Serializer):
    """
    Get Lms Data Request Serializer
    """
    national_id = serializers.CharField(required=True)

class DedupeCheckRequestSerializer(serializers.Serializer):
    """
    Dedupe Check Request Serializer
    """
    national_id = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)


class DedupeCheckRoboRequestSerializer(serializers.Serializer):
    p_Phone = serializers.CharField(required=True)
    p_NID = serializers.CharField(required=True)
    p_Product_Channel = serializers.CharField(required=True)

class RetreiveReferencesRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    national_id = serializers.CharField(required=True)


class RepaySerializer(serializers.ModelSerializer):
    """
    Repay Loan serializer
    """
    payment_date = serializers.DateField(source='PAID_DATE')
    payment_mode = serializers.SerializerMethodField()
    payment_amount = serializers.IntegerField(source='PAID_AMT')

    class Meta:
        model = fes_dbsync_models.RoboRepayUplView
        fields = ('payment_date', 'payment_mode', 'payment_amount')

    def get_payment_mode(self, obj):
        """
        utility to get payment mode
        :param obj:
        :return:
        """
        ref_num_first_two_characters = obj.REF_NUM[:2]
        try:
            int(ref_num_first_two_characters)
        except ValueError:
            channel = fec_dbsync_cons.CHANNEL_DICT.get(ref_num_first_two_characters, '')
        else:
            channel = 'VNPOST'
        return '{0} {1}'.format(channel, obj.REF_NUM)


class MISSerializer(serializers.Serializer):
    """
    MIS Report serializer
    """
    REPORT_CHOICES = (
        ("customer_journey_tracking", "customer_journey_tracking"),
        ("reject_loan_application", "reject_loan_application"),
        ("customer_portfolio", "customer_portfolio"),
        ("disbursement_status_tracking", "disbursement_status_tracking"),
        ("product_performance", "product_performance"),
        ("customer_service_tracking", "customer_service_tracking"),
        ("loan_portfolio_snapshot", "loan_portfolio_snapshot"),
        ("loan_status_tracking", "loan_status_tracking"),
        ("robo_sales", "robo_sales"),
        ("api_status_tracking", "api_status_tracking"),
        ("loan_snapshot_active", "loan_snapshot_active")
    )

    report = serializers.ChoiceField(choices=REPORT_CHOICES, required=True)
    filters = serializers.JSONField(required=True)
    emails = serializers.ListField(child=serializers.EmailField(), required=False, allow_null=True)
    requester = serializers.CharField()

    def is_valid(self, raise_exception=False):
        validity = super(MISSerializer, self).is_valid(raise_exception)
        if not validity:
            return validity
        if self.data.get('filters') and type(self.data.get('filters')) == dict:
            if not (self.data['filters'].get('to') and self.data['filters'].get('from')):
                return False
            for key, value in self.data['filters'].items():
                if type(value) == str and value.lower() == "all":
                    self.data['filters'][key] = ""
        else:
            return False
        return validity


#nguyenhuuvinh4 START
class GetDataCustConAddRequestSerializer(serializers.Serializer):
    contract_number = serializers.CharField(required=True)
#nguyenhuuvinh4 END

class GetActiveLoanByAppIdsRequestSerializer(serializers.Serializer):
    app_ids = serializers.CharField(required=True)

class FraudSerializer(serializers.Serializer):
    """
    This class serialize the data come from flowable side in form of request
    """
    pincode = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    tsaCode = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    dsaCode = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    ccCode = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    temporaryProvince = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    temporaryAddressCityDistrict = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    temporaryAddressCityDistrictWard = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    permanentAddressCity = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    permanentAddressCityDistrict = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    permanentAddressCityDistrictWard = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    locationCordinate = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    phoneNumberCustomer = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    phoneNumberReferenceA = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    phoneNumberReferenceB = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    phoneNumberReferenceC = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    applicationID = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    bankAccount = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    nationalId = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    personId = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    productId = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    productCode = serializers.CharField(required=False, allow_blank=True, allow_null=True)

class GetBlacklistedAccountsRequestSerializer(serializers.Serializer):
    bank_account = serializers.CharField(required=True)


class GetAMLCheckServiceRequestSerializer(serializers.Serializer):
    PERSON_ID = serializers.CharField()
    FULL_NAME = serializers.CharField()
    ID_NO = serializers.CharField()
    DOB = serializers.CharField()


class CheckBlackListPhoneNumberRequestSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField()