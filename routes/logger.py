import logging


logger = logging.basicConfig(filename="logs/app.log",
                             level=logging.INFO,
                             format="%(asctime)s %(level)s %(message)s")

logger =logging.getLogger(__name__)







