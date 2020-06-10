import re
import time

import paramiko


class SSHException(Exception):
    pass


class SSHSession(object):
    def __init__(self, ssh_session_logger, default_prompt='#'):
        # self.name = name
        self.connection = None
        self.prompt = "#"
        self.commandTimeout = 2
        # stats
        self.logger = ssh_session_logger
        self.timeSendCmd = 0
        self.meanCmdTime = 0
        self.sentLines = 0
        self.sentBytes = 0
        self.errors = ["Illegal command", "No such interface in system", "Address can not be a network address"]
        self.connectionEnabled = False
        self.remote_conn = None
        reg = r'\w+@\w+#'
        self.pattern = re.compile(reg)

    def set_prompt(self, prompt):
        self.prompt = prompt

    def disconnect(self):
        if self.connectionEnabled:
            self.logger.info('Closing connection...')
            self.remote_conn.close()
            self.logger.info('Connection closed')
            self.connectionEnabled = False

    def refresh_stats(self, command, start_time, end_time):
        self.sentLines += 1
        self.sentBytes += len(command)
        self.timeSendCmd = end_time - start_time
        self.meanCmdTime = (self.meanCmdTime * (self.sentLines - 1) + self.timeSendCmd) / float(self.sentLines)

    def go_ro_root(self):
        self.connection.send('\x1A')
        time.sleep(self.commandTimeout)

    def send(self, command):
        if self.connectionEnabled:
            if command:
                start_time = time.time()
                self.logger.debug('Sending command: %s' % command)
                self.connection.send("{}\n".format(command))

                while True:
                    time.sleep(self.commandTimeout)
                    output = self.connection.recv(1000)
                    if self.pattern.match(bytes.decode(output), re.MULTILINE) is not None:
                        break
                answer, vmm = self.pattern.split(bytes.decode(output))
                for error in self.errors:
                    if error in answer:
                        self.connection.send('\x15')
                        raise ValueError("Error in answer: {}".format(answer))
                self.logger.debug('Command answer:\n%s' % answer)
                self.logger.debug("admin@vmm%s" % vmm)
                end_time = time.time()
                self.refresh_stats(command, start_time, end_time - self.commandTimeout * 2)
                return answer

    def connect(self, user, ip, port=22, password=None):
        self.logger.info('Connecting to %s@%s' % (user, ip))
        self.remote_conn = paramiko.SSHClient()
        self.remote_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.remote_conn.connect(ip, port, user, password, look_for_keys=False, allow_agent=False)
        self.logger.info('SSH connection established to ' + ip)
        self.connection = self.remote_conn.invoke_shell()
        # Print terminal to screen
        time.sleep(3)
        output = self.connection.recv(1000)
        self.logger.debug(bytes.decode(output))
        # self.logger.info('Connected')
        self.connectionEnabled = True
