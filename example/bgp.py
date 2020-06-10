import executor
from assert_statement.asserts import should_raise_error, should_not_contains, should_contains
from executor.meta.connection import connection
from executor.meta.env import env
from executor.meta.node import node
from executor.meta.order import order
from executor.router_test import RouterTest
from shared.cisco import *


@env("env.yml")
@connection("bgp_connection.yml")
class BGPTestSuite(RouterTest):
    ping_error = "bind: Cannot assign requested address"

    @node("node1")
    @order(value=1)
    def Node1BGPConfigureTestCase(self, connection: Connection):
        configure_terminal(connection)
        enter_bgp(connection, 100)
        bgp_router_id(connection, "1.1.1.1")
        bgp_network(connection, "11.10.10.0/24")
        bgp_network(connection, "101.0.0.0/24")
        bgp_neighbor(connection, "20.20.20.2", "remote-as", "200")
        timers(connection, "bgp", 30, 120)
        distance(connection, "bgp", "100", "150", "180")
        exit_from_command(connection)
        ip_route(connection, "default", "101.0.0.10")
        ip_route(connection, "11.10.10.0/24", "null")

    @node("node1")
    @order(value=4)
    def Node1PingTestCase(self, connection: Connection):
        should_not_contains(do_ping(connection, "102.0.0.1", "101.0.0.1", 30), self.ping_error)
        should_not_contains(do_ping(connection, "103.0.0.1", "101.0.0.1", 30), self.ping_error)

    @node("node2")
    @order(value=2)
    def Node2BGPConfigureTestCase(self, connection: Connection):
        configure_terminal(connection)
        enter_bgp(connection, 200)
        bgp_router_id(connection, "2.2.2.2")
        bgp_network(connection, "20.20.20.0/24")
        bgp_network(connection, "30.30.30.0/24")
        bgp_network(connection, "102.0.0.0/24")
        bgp_neighbor(connection, "20.20.20.1", "remote-as", "100")
        bgp_neighbor(connection, "30.30.30.2", "remote-as", "200")
        bgp_neighbor(connection, "30.30.30.2", "next-hop-self")
        bgp_neighbor(connection, "30.30.30.2", "password", "12345678")
        bgp_neighbor(connection, "30.30.30.2", "soft-reconfiguration", "inbound")
        distance(connection, "50", "30.30.30.2/32")

    @node("node3")
    @order(value=3)
    def Node3BGPConfigureTestCase(self, connection: Connection):
        configure_terminal(connection)
        enter_bgp(connection, 300)
        bgp_router_id(connection, "3.3.3.3")
        bgp_network(connection, "30.30.30.0/24")
        bgp_network(connection, "103.0.0.0/24")
        bgp_neighbor(connection, "30.30.30.1", "remote-as", "200")
        bgp_neighbor(connection, "30.30.30.1", "password", "12345678")
        bgp_neighbor(connection, "30.30.30.1", "soft-reconfiguration", "inbound")



    @node("node2")
    @order(value=5)
    def Node2PingTestCase(self, connection: Connection):
        should_not_contains(do_ping(connection, "101.0.0.1", "102.0.0.1", 40), self.ping_error)
        should_not_contains(do_ping(connection, "103.0.0.1", "102.0.0.1", 40), self.ping_error)

    @node("node3")
    @order(value=6)
    def Node3PingTestCase(self, connection: Connection):
        should_contains(do_ping(connection, "101.0.0.1", "103.0.0.1", 40), self.ping_error)
        should_contains(do_ping(connection, "102.0.0.1", "103.0.0.1", 40), self.ping_error)



if __name__ == '__main__':
    executor.main()
