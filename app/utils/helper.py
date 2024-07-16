import logging
import datetime
from pytz import timezone

from .firebase_connector import initialize_firebase
from .db.database import db

defined_timezone = timezone("America/Sao_Paulo")


# Classe de formatter personalizado
class CustomFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.datetime.fromtimestamp(record.created)
        dt = dt.astimezone(defined_timezone)
        if datefmt:
            return dt.strftime(datefmt)
        else:
            return dt.isoformat()


logging.basicConfig(level=logging.INFO)

# Obtendo o logger root
logger = logging.getLogger()

# Configurando o formatter no handler padrão
for handler in logger.handlers:
    handler.setFormatter(
        CustomFormatter(fmt="%(asctime)s - %(levelname)s - %(message)s")
    )

logging.info("Starting RDS connection")
database = db
logging.info("RDS connection started")

logging.info("Starting Firebase connection")
firebase = initialize_firebase()
logging.info("Firebase connection started")
