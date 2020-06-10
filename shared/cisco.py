from executor.connection import Connection


def do_ping(connection: Connection, param, param1, param2: int) -> str:
    return connection.execute("do ping {} source {} repeat {}".format(param, param1, param2))


def configure_terminal(connection: Connection):
    connection.send("configure terminal")


def enter_bgp(connection: Connection, number: int):
    connection.send("router bgp {}".format(number))


def save_bgp(connection: Connection):
    connection.send("save bgp")


def bgp_router_id(connection: Connection, ip: str):
    connection.send("bgp router-id {}".format(ip))


def bgp_network(connection: Connection, network: str):
    connection.send("network {}".format(network))


def bgp_neighbor(connection: Connection, neighbor: str, *params: str):
    connection.send("neighbor {} {}".format(neighbor, " ".join(params)))


def timers(connection: Connection, command: str, param1: int, param2: int):
    connection.send("timers {} {} {}".format(command, param1, param2))


def distance(connection: Connection, *params: str):
    connection.send("distance {}".format(" ".join(params)))


def ip_route(connection: Connection, param1: str, param2: str):
    connection.send("ip route {} {}".format(param1, param2))


def exit_from_command(connection: Connection):
    connection.send("exit")


def router(connection: Connection, *params: str):
    connection.send("router %s" % " ".join(params))


def osfp_router_id(connection: Connection, param1: str):
    connection.send("ospf router-id {}".format(param1))


def network_area(connection: Connection, param1: str, param2: str):
    connection.send("network {} area {}".format(param1, param2))


def network(connection: Connection, *params: str):
    connection.send("network {}".format(params))


def area(connection: Connection, *params: str):
    connection.send("area %s" % " ".join(params))


def redistribute(connection: Connection, *params: str):
    connection.send("redistribute %s" % " ".join(params))


def system(connection: Connection, *params: str):
    connection.send("system %s" % " ".join(params))


def isis(connection: Connection, *params: str):
    connection.send("isis %s" % " ".join(params))


def net(connection: Connection, *params: str):
    connection.send("net %s" % " ".join(params))


def is_type(connection: Connection, type: str):
    connection.send("is-type %s" % type)


def passive_interface(connection: Connection, interface: str):
    connection.send("passive-interface %s" % interface)


def show(connection: Connection, *params: str):
    connection.send("show {}".format(" ".join(params)))


def router_id(connection: Connection, ip: str):
    connection.send("router-id {}".format(ip))


def no_shutdown(connection: Connection):
    connection.send("no shutdown")


def ip(connection: Connection, *params: str):
    connection.send("ip {}".format(" ".join(params)))


def interface(connection: Connection, *params: str):
    connection.send("interface {}".format(" ".join(params)))


def vid(connection: Connection, param: str):
    connection.send("vid {}".format(param))


def tcpdump(connection: Connection, *params: str):
    connection.send("tcpdump {}".format(" ".join(params)))


def area_password(connection: Connection, *params: str):
    connection.send("area_password {}".format(" ".join(params)))


def save(connection: Connection, param: str):
    connection.send("save {}".format(param))


def end(connection: Connection):
    connection.send("end")


def ping(connection: Connection, *params: str):
    connection.send("ping {}".format(" ".join(params)))
