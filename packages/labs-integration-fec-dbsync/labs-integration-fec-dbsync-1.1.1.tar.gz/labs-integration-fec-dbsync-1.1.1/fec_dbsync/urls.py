from django.conf.urls import url

from fec_dbsync import views


urlpatterns = [
    url(r'^lms-data/', views.GetLmsData.as_view(), name='get-lms-data'),
    url(r'^robo-active-apps-count/', views.GetRoboActiveApps.as_view(), name='get-robo-active-apps-count'),
    url(r'^get_repayment_schedule/', views.GetRepaymentSchedule.as_view(), name='get-repayment-schedule'),
    url(r'^generate_mis_report/', views.GenerateMISReport.as_view()),
    url(r'^get_repayment_schedule/',views.GetRepaymentSchedule.as_view(), name='get-repayment-schedule'),
    url(r'^collections_repayment/',views.CollectionsRepayment.as_view(), name='collections-repayment'),
    url(r'^collections_statement/', views.CollectionsStatement.as_view(), name='collections-statement'),
    url(r'^collections_payment/', views.CollectionsPayment.as_view(), name='collections-payment'),
    url(r'^collections_summary/', views.CollectionsSummary.as_view(), name='collections-summary'),
    url(r'^collections_fore_closure/', views.CollectionsForeClosure.as_view(), name='collections-fore-closure'),
    url(r'^collections_sta_card/', views.CollectionsStaCard.as_view(), name='collections-sta-card'),
    url(r'^dedupe_check/', views.DedupeCheck.as_view(), name='dedupe-check'),
    url(r'^dedupe_check_robo/', views.DedupeCheckRobo.as_view(), name='dedupe-check-robo'),
    url(r'^retrieve_references/', views.RetrieveReferences.as_view(), name='retrieve-references'),
    url(r'^fraudCheck/', views.FraudCheckRule.as_view(), name='fraud-check'),
    url(r'^get_active_loans/', views.GetActiveLoanByAppIds.as_view(), name='get-active-loan'),
    url(r'^get_data_custconadd/', views.GetDataCustConAdd.as_view(), name='get-data-custconadd'), #nguyenhuuvinh4
    url(r'^get_blacklisted_accounts/', views.GetBlacklistedAccounts.as_view(), name='get_blacklisted_accounts'),
    url(r'^get_aml_data/', views.getAMLTableData.as_view(), name='get_aml_data'),
    url(r'^get_data_dwh/', views.GetRegisAndActHiFromDWHRequestSerializer.as_view(), name='get_data_dwh'),
]