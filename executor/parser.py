import re
from typing import Dict, List

from yaml import load

from runner.ConnectionData import ConnectionData


def connection_parser(file_path: str) -> Dict[str, ConnectionData]:
    connection_data: Dict[str, ConnectionData] = {}
    try:
        from yaml import CLoader as Loader, CDumper as Dumper
    except ImportError:
        from yaml import Loader, Dumper

    file = open(file_path, "r", encoding="utf-8")
    yaml_file = load(file, Loader=Loader)
    for node in yaml_file['env']:
        data = yaml_file['env'][node]
        connection_data.update(
            {node: ConnectionData(data['username'], str(data['password']), data['hostname'], data['port'])})
    file.close()
    return connection_data


def env_parser(file_path: str) -> Dict[str, List[str]]:
    env_data: Dict[str, List[str]] = {}
    try:
        from yaml import CLoader as Loader, CDumper as Dumper
    except ImportError:
        from yaml import Loader, Dumper

    file = open(file_path, "r", encoding="utf-8")
    yaml_file = load(file, Loader=Loader)
    for node in yaml_file['env']:
        data = yaml_file['env'][node]
        for command in data:
            if type(command) == str:
                env_data[node] = [command]
            else:
                command_id = command['command']
                variables = {}
                for id in command['variables']:
                    variables[id] = command['variables'][id]
                pre = []
                for common in yaml_file['common']:
                    if common['id'] == command_id:
                        for exec in common['execute']:
                            p = re.findall(r"@\D*", exec)
                            if len(p) != 0:
                                p = p[0]
                                pre.append(exec.replace(p, str(variables[p[1:]])))
                            else:
                                pre.append(exec)
                env_data[node] += pre
    file.close()
    return env_data


