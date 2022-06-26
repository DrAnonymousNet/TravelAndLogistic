from datetime import datetime, timedelta
from django.dispatch import Signal
from django.dispatch import receiver
from .tasks import CostructEmail
import dateutil.tz

payment_verify_signal = Signal()
notification_signal = Signal()

@receiver(payment_verify_signal)
def SendTicketEmail(sender, **kwargs):
    kwargs["data"]["date"] = datetime.strptime((kwargs["data"]["date"]),"%Y-%m-%d")
    kwargs["data"]["time"] = datetime.strptime(kwargs["data"]["time"],"%H:%M:%S")
    CostructEmail.delay((kwargs["data"]))

@receiver(notification_signal)
def SendTravelNotificationSignal(sender, **kwargs):
    kwargs["data"]["date"] = datetime.strptime((kwargs["data"]["date"]),"%Y-%m-%d")
    kwargs["data"]["time"] = datetime.strptime(kwargs["data"]["time"],"%H:%M:%S")
    time = kwargs["data"]["time"]
    date =kwargs["data"]["date"]
    kwargs["data"]["notification"]= "Notification"
    date= datetime(year= date.year, month=date.month, day=date.day,
     hour=time.hour, minute=time.minute,second=time.second,tzinfo=dateutil.tz.tzoffset(None, 3*60*60)) - timedelta(hours=1)
    CostructEmail.apply_async([kwargs["data"]], eta=date)







