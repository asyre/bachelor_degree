from dataclasses import dataclass


@dataclass
class ConnectionData:
    username: str
    password: str = None
    hostname: str = "localhost"
    port: int = 22
