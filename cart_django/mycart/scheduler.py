import os
import django
import schedule
import time
from loguru import logger

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mycart.settings')
django.setup()


from product_cart.models import Plyer, Level, Clik

logger.debug("That's it, beautiful and simple logging!")
logger.add("file_{time}.log", rotation='10 mb', level='DEBUG')


@logger.catch
def check_level():
    logger.debug("check level!")
    players = Plyer.objects.all()
    for plyer in players:
        level_obj, created = Level.objects.get_or_create(plaer=plyer)
        if level_obj.level == 8:
            counter, created = Clik.objects.get_or_create(plaer=plyer)
            counter.count += 100
            counter.save()


schedule.every(60).seconds.do(check_level)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
