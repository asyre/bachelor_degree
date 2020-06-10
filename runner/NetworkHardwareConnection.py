import logging
from collections import Callable

# TODO перенести в параметры
from runner.SSH import SSHSession

log_level = "DEBUG"


class NetworkHardwareMachineConnection:
    def __init__(self,
                 ssh_session_builder):
        self.ssh_session_builder = ssh_session_builder
        self.session: SSHSession = ssh_session_builder()

    def execute(self, command: str):
        return self.session.send(command)

    def return_to_root(self):
        return self.session.go_ro_root()

    def close(self):
        self.session.disconnect()

    def reconnect(self, none_context_commands):
        self.session.disconnect()
        self.session = self.ssh_session_builder()
        for command in none_context_commands:
            self.execute(command)


def create_machine_connection(hostname: str,
                              port: int,
                              username: str,
                              password: str = None) -> NetworkHardwareMachineConnection:
    ch = logging.FileHandler('execute.log', "w")
    loglevel = log_level
    if loglevel == 'DEBUG':
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s: %(message)s')
    ch.setFormatter(formatter)

    logger = logging.getLogger('Connection[%s]' % hostname)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    def session_builder() -> SSHSession:
        connection = SSHSession(logger)

        connection.connect(
            ip=hostname,
            port=port,
            user=username,
            password=password
        )

        return connection

    return NetworkHardwareMachineConnection(session_builder)
