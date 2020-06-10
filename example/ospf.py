# import executor
# from assert_statement.asserts import should_raise_error, should_not_contains, should_contains
# from executor.meta import scheduler
# from executor.meta.connection import connection
# from executor.meta.env import env
# from executor.meta.node import node
# from executor.meta.order import order
# from executor.router_test import RouterTest
# from shared.cisco import *
#
#
# @connection("ospf_connection.yml")
# @scheduler("parallel")
# class OspfTestSuite(RouterTest):
#     @node("node1")
#     @order(value=1)
#     def Node1OspfConfigureTestCase(self, connection: Connection):
#         configure_terminal(connection)
#
#         interface(connection, "eth1")
#         ip(connection, "address", "20.20.20.1/24")
#         no_shutdown(connection)
#         exit_from_command(connection)
#
#         interface(connection, "lo", "1")
#         ip(connection, "address", "101.0.0.1/24")
#         no_shutdown(connection)
#         exit_from_command(connection)
#
#         router(connection, "ospf")
#         osfp_router_id(connection, "1.1.1.1")
#         network_area(connection, "20.20.20.0/24", "1")
#         network_area(connection, "101.0.0.0/24", "1")
#         area(connection, "1", "stub")
#         exit_from_command(connection)
#
#     @node("node2")
#     @order(value=1)
#     def Node2OspfConfigureTestCase(self, connection: Connection):
#         configure_terminal(connection)
#
#         interface(connection, "eth0")
#         ip(connection, "address", "20.20.20.2/24")
#         no_shutdown(connection)
#         exit_from_command(connection)
#
#         interface(connection, "eth1")
#         ip(connection, "address", "60.60.60.1/24")
#         no_shutdown(connection)
#         exit_from_command(connection)
#
#         interface(connection, "eth3")
#         ip(connection, "address", "30.30.30.1/24")
#         no_shutdown(connection)
#         exit_from_command(connection)
#
#         interface(connection, "eth2")
#         ip(connection, "address", "50.50.50.1/24")
#         no_shutdown(connection)
#         exit_from_command(connection)
#
#         interface(connection, "lo", "1")
#         ip(connection, "address", "102.0.0.1/24")
#         no_shutdown(connection)
#         exit_from_command(connection)
#
#         router(connection, "ospf")
#         osfp_router_id(connection, "2.2.2.2")
#         network_area(connection, "20.20.20.0/24", "1")
#         network_area(connection, "30.30.30.0/24", "2")
#         network_area(connection, "50.50.50.0/24", "0")
#         network_area(connection, "60.60.60.0/24", "3")
#         network_area(connection, "102.0.0.0/24", "0")
#         area(connection, "1", "stub")
#         area(connection, "2", "nssa")
#         area(connection, "3", "stub", "no-summary")
#         area(connection, "0", "range", "105.0.0.0/8")
#         exit_from_command(connection)
#
#     @node("node3")
#     @order(value=1)
#     def Node3OspfConfigureTestCase(self, connection: Connection):
#         configure_terminal(connection)
#
#         interface(connection, "eth0")
#         ip(connection, "address", "30.30.30.2/24")
#         no_shutdown(connection)
#         exit_from_command(connection)
#
#         interface(connection, "eth1")
#         ip(connection, "address", "40.40.40.1/24")
#         no_shutdown(connection)
#         exit_from_command(connection)
#
#         interface(connection, "lo", "1")
#         ip(connection, "address", "103.0.0.1/24")
#         no_shutdown(connection)
#         exit_from_command(connection)
#
#         router(connection, "ospf")
#         osfp_router_id(connection, "3.3.3.3")
#         network_area(connection, "30.30.30.0/24", "2")
#         network_area(connection, "103.0.0.0/24", "2")
#         area(connection, "2", "nssa")
#         redistribute(connection, "rip", "metric-type", "2")
#         redistribute(connection, "rip", "metric", "20")
#         exit_from_command(connection)
#
#         router(connection, "rip")
#         redistribute(connection, "ospf", "metric", "5")
#         network(connection, "40.40.40.0/24")
#         exit_from_command(connection)
#
#     @node("node4")
#     @order(value=1)
#     def Node4OspfConfigureTestCase(self, connection: Connection):
#         configure_terminal(connection)
#
#         interface(connection, "eth0")
#         ip(connection, "address", "40.40.40.2/24")
#         no_shutdown(connection)
#         exit_from_command(connection)
#
#         interface(connection, "lo", "1")
#         ip(connection, "address", "104.0.0.1/24")
#         no_shutdown(connection)
#         exit_from_command(connection)
#
#         router(connection, "rip")
#         redistribute(connection, "ospf", "metric", "5")
#         network(connection, "40.40.40.0/24")
#         network(connection, "104.0.0.0/24")
#         exit_from_command(connection)
#
#         ip_route(connection, "default", "40.40.40.1")
#
#     @node("node5")
#     @order(value=1)
#     def Node5OspfConfigureTestCase(self, connection: Connection):
#         configure_terminal(connection)
#
#         interface(connection, "eth0")
#         ip(connection, "address", "50.50.50.2/24")
#         no_shutdown(connection)
#         exit_from_command(connection)
#
#         interface(connection, "lo", "1")
#         ip(connection, "address", "105.1.0.1/24")
#         no_shutdown(connection)
#         exit_from_command(connection)
#
#         interface(connection, "lo", "2")
#         ip(connection, "address", "105.2.0.1/24")
#         no_shutdown(connection)
#         exit_from_command(connection)
#
#         router(connection, "ospf")
#         osfp_router_id(connection, "5.5.5.5")
#         network_area(connection, "50.50.50.0/24", "0")
#         network_area(connection, "105.1.0.0/24", "0")
#         network_area(connection, "105.2.0.0/24", "0")
#         exit_from_command(connection)
#
#     @node("node6")
#     @order(value=1)
#     def Node6OspfConfigureTestCase(self, connection: Connection):
#         configure_terminal(connection)
#
#         interface(connection, "eth0")
#         ip(connection, "address", "60.60.60.2/24")
#         no_shutdown(connection)
#         exit_from_command(connection)
#
#         interface(connection, "lo", "1")
#         ip(connection, "address", "106.0.0.1/24")
#         no_shutdown(connection)
#         exit_from_command(connection)
#
#         router(connection, "ospf")
#         osfp_router_id(connection, "6.6.6.6")
#         network_area(connection, "60.60.60.0/24", "3")
#         network_area(connection, "106.0.0.0/24", "3")
#         area(connection, "3", "stub")
#         exit_from_command(connection)
#
#     @node("node1")
#     @order(value=2)
#     def Node1PingTestCase(self, connection: Connection):
#         should_contains(do_ping(connection, "102.0.0.1", "101.0.0.1", 10), "10 packets transmitted")
#         should_contains(do_ping(connection, "103.0.0.1", "101.0.0.1", 10), "10 packets transmitted")
#         should_contains(do_ping(connection, "104.0.0.1", "101.0.0.1", 10), "10 packets transmitted")
#         should_contains(do_ping(connection, "105.0.0.1", "101.0.0.1", 10), "10 packets transmitted")
#
#     @node("node2")
#     @order(value=2)
#     def Node2PingTestCase(self, connection: Connection):
#         should_contains(do_ping(connection, "101.0.0.1", "102.0.0.1", 10), "10 packets transmitted")
#         should_contains(do_ping(connection, "103.0.0.1", "102.0.0.1", 10), "10 packets transmitted")
#         should_contains(do_ping(connection, "104.0.0.1", "102.0.0.1", 10), "10 packets transmitted")
#         should_contains(do_ping(connection, "105.0.0.1", "102.0.0.1", 10), "10 packets transmitted")
#
#     @node("node3")
#     @order(value=2)
#     def Node3PingTestCase(self, connection: Connection):
#         should_contains(do_ping(connection, "101.0.0.1", "103.0.0.1", 10), "10 packets transmitted")
#         should_contains(do_ping(connection, "102.0.0.1", "103.0.0.1", 10), "10 packets transmitted")
#         should_contains(do_ping(connection, "104.0.0.1", "103.0.0.1", 10), "10 packets transmitted")
#         should_contains(do_ping(connection, "105.0.0.1", "103.0.0.1", 10), "10 packets transmitted")
#
#     @node("node4")
#     @order(value=2)
#     def Node4PingTestCase(self, connection: Connection):
#         should_contains(do_ping(connection, "101.0.0.1", "104.0.0.1", 10), "10 packets transmitted")
#         should_contains(do_ping(connection, "102.0.0.1", "104.0.0.1", 10), "10 packets transmitted")
#         should_contains(do_ping(connection, "103.0.0.1", "104.0.0.1", 10), "10 packets transmitted")
#         should_contains(do_ping(connection, "105.0.0.1", "104.0.0.1", 10), "10 packets transmitted")
#
#     @node("node5")
#     @order(value=2)
#     def Node5PingTestCase(self, connection: Connection):
#         should_contains(do_ping(connection, "101.0.0.1", "105.0.0.1", 10), "10 packets transmitted")
#         should_contains(do_ping(connection, "102.0.0.1", "105.0.0.1", 10), "10 packets transmitted")
#         should_contains(do_ping(connection, "103.0.0.1", "105.0.0.1", 10), "10 packets transmitted")
#         should_contains(do_ping(connection, "104.0.0.1", "105.0.0.1", 10), "10 packets transmitted")
#
#     @node("node6")
#     @order(value=2)
#     def Node6PingTestCase(self, connection: Connection):
#         should_contains(do_ping(connection, "101.0.0.1", "106.0.0.1", 10), "10 packets transmitted")
#         should_contains(do_ping(connection, "102.0.0.1", "106.0.0.1", 10), "10 packets transmitted")
#         should_contains(do_ping(connection, "103.0.0.1", "106.0.0.1", 10), "10 packets transmitted")
#         should_contains(do_ping(connection, "104.0.0.1", "106.0.0.1", 10), "10 packets transmitted")
#         should_contains(do_ping(connection, "105.0.0.1", "106.0.0.1", 10), "10 packets transmitted")
#
#
# if __name__ == '__main__':
#     executor.main()
