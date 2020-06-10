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
# @connection("isis_connection.yml")
# @scheduler("parallel")
# class IsIsTestSuite(RouterTest):
#     @node("node1")
#     @order(value=1)
#     def NodeIsIsConfigureTestCase(self, connection: Connection):
#         configure_terminal(connection)
#         # system(connection, "host-name", "R1", "domain-name", "home")
#         # system(connection, "ssh", "timeout", "0")
#         router_id(connection, "1.0.0.1")
#         interface(connection, "lo", "1")
#         ip(connection, "address", "1.0.0.1/32")
#         no_shutdown(connection)
#         exit_from_command(connection)
#
#         interface(connection, "eth1")
#         ip(connection, "address", "10.0.0.1/24")
#         ip(connection, "router", "isis", "ABC")
#         isis(connection, "circuit-type", " level-2-only")
#         no_shutdown(connection)
#         exit_from_command(connection)
#
#         router(connection, "isis", "ABC")
#         net(connection, "49.0001.0010.0000.0001.00")
#         is_type(connection, "level-1-2")
#         passive_interface(connection, "lo1")
#         distance(connection, "122")
#         end(connection)
#
#         save(connection, "isis")
#
#     @node("node2")
#     @order(value=1)
#     def Node2IsIsConfigureTestCase(self, connection: Connection):
#         configure_terminal(connection)
#
#         # system(connection, "host-name", "R2", "domain-name", "home")
#         # system(connection, "ssh", "timeout", "0")
#         router_id(connection, "2.0.0.1")
#         interface(connection, "lo", "1")
#         ip(connection, "address", "2.0.0.1/32")
#         ip(connection, "router", "isis", "ABC")
#         no_shutdown(connection)
#         exit_from_command(connection)
#
#         interface(connection, "eth0")
#         ip(connection, "address", "10.0.0.2/24")
#         ip(connection, "router", "isis", "ABC")
#         isis(connection, "circuit-type", " level-2-only")
#         no_shutdown(connection)
#         exit_from_command(connection)
#
#         interface(connection, "eth1")
#         vid(connection, "100")
#         ip(connection, "mtu", "1496")
#         ip(connection, "address", "20.0.0.1/24")
#         ip(connection, "router", "isis", "ABC")
#         isis(connection, "network", "point-to-point")
#         no_shutdown(connection)
#         exit_from_command(connection)
#
#         router(connection, "isis", "ABC")
#         net(connection, "49.0001.0020.0000.0001.00")
#         is_type(connection, "level-2-only")
#         end(connection)
#
#         save(connection, "isis")
#
#     @node("node3")
#     @order(value=1)
#     def Node3IsIsConfigureTestCase(self, connection: Connection):
#         configure_terminal(connection)
#
#         # system(connection, "host-name", "R3", "domain-name", "home")
#         # system(connection, "ssh", "timeout", "0")
#
#         router_id(connection, "3.0.0.1")
#
#         interface(connection, "lo", "1")
#         ip(connection, "address", "3.0.0.1/32")
#         ip(connection, "router", "isis", "ABC")
#         no_shutdown(connection)
#         exit_from_command(connection)
#
#         interface(connection, "eth1")
#         vid(connection, "100")
#         ip(connection, "mtu", "1496")
#         ip(connection, "address", "20.0.0.2/24")
#         ip(connection, "router", "isis", "ABC")
#         isis(connection, "network", "point-to-point")
#         no_shutdown(connection)
#         exit_from_command(connection)
#
#         interface(connection, "eth0")
#         ip(connection, "address", "30.0.0.1/24")
#         ip(connection, "router", "isis", "ABC")
#         no_shutdown(connection)
#         exit_from_command(connection)
#
#         router(connection, "isis", "ABC")
#         net(connection, "49.0002.0030.0000.0001.00")
#         is_type(connection, "level-1-2")
#         area_password(connection, "1234qwer", "authenticate", "snp", "validate")
#         end(connection)
#
#         save(connection, "isis")
#
#     @node("node4")
#     @order(value=1)
#     def Node4IsIsConfigureTestCase(self, connection: Connection):
#         configure_terminal(connection)
#
#         # system(connection, "host-name", "R4", "domain-name", "home")
#         # system(connection, "ssh", "timeout", "0")
#
#         router_id(connection, "4.0.0.1")
#         interface(connection, "lo", "1")
#         ip(connection, "address", "4.0.0.1/32")
#         ip(connection, "router", "isis", "ABC")
#         no_shutdown(connection)
#         exit_from_command(connection)
#
#         interface(connection, "eth0")
#         ip(connection, "address", "30.0.0.2/24")
#         ip(connection, "router", "isis", "ABC")
#         no_shutdown(connection)
#         exit_from_command(connection)
#
#         router(connection, "isis", "ABC")
#         net(connection, "49.0002.0040.0000.0001.00")
#         is_type(connection, "level-1")
#         area_password(connection, "1234qwer", "authenticate", "snp", "validate")
#         end(connection)
#
#         save(connection, "isis")
#
#     @node("node1")
#     @order(value=2)
#     def Node1PingTestCase(self, connection: Connection):
#         should_contains(do_ping(connection, "4.0.0.1", "1.0.0.1", 10), "10 packets transmitted")
#
#     @node("node2")
#     @order(value=2)
#     def Node2PingTestCase(self, connection: Connection):
#         should_contains(tcpdump(connection, "eth0", "packets", "10"), "IP 4.0.0.1 > 1.0.0.1: ICMP echo reply")
#         should_contains(tcpdump(connection, "eth0", "packets", "10"), "IP 30.0.0.2 > 10.0.0.1: ICMP echo reply")
#
#
# if __name__ == '__main__':
#     executor.main()
