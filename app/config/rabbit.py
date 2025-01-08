from functools import cached_property

from pydantic import AmqpDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RabbitMQConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="rabbitmq_")

    user: str = "user"
    password: str = "password"
    host: str = "localhost"
    port: int = 5672
    queue: str = "test_queue"
    publish_exchanger: str = "auth"

    @cached_property
    def url(self):
        dns = AmqpDsn(f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/")
        return str(dns)
