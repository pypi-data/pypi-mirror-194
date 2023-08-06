from django.apps import AppConfig


class FecDbsyncConfig(AppConfig):
    name = 'fec_dbsync'
    verbose_name = 'FEC DBSYNC'

    # This key is used to identify the apps for Kuliza Labs Integration Broker.
    labs_integration_app = True

    # This key is used to define a prefix for all URL in the app.
    # This will only be honoured when the key 'labs_integration_app' is 'True'.
    labs_url_prefix = '/fec/vnpost/'