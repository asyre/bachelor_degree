from typing import NoReturn

from runner.NetworkHardwareConnection import NetworkHardwareMachineConnection


class Connection:
    def __init__(self, hardware_connection: NetworkHardwareMachineConnection):
        self.connection = hardware_connection

    def send(self, *commands: str) -> NoReturn:
        for command in commands:
            self.connection.execute(command)

    def execute(self, command: str) -> str:
        return self.connection.execute(command)
