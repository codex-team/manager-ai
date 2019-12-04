from apscheduler.schedulers.blocking import BlockingScheduler

from controller import Controller
from settings import *

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.configure(**SCHEDULER)

    controller = Controller()
    controller.init_scheduler(scheduler)
    controller.run()
