from api import iotSystem
from django.dispatch import receiver
from django.db.backends.signals import connection_created


MQTT_run_status = False


@receiver(connection_created)
def mysql_connected_callback(sender, connection, **kwargs):
    """
    连接Mysql--回调
    """
    global MQTT_run_status

    # print("123")

    if not MQTT_run_status:
        iotSystem.start()
        iotSystem.start_mq()
        MQTT_run_status = True

