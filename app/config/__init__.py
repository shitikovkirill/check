from app.config.db import DBConfig
from app.config.logging import LogConfig
from app.config.rabbit import RabbitMQConfig
from app.config.settings import Settings

settings = Settings()
log_config = LogConfig()
rabbit_mq = RabbitMQConfig()
db_config = DBConfig()
