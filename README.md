# PyRouterTest
PyRouterTest - фреймворк для автоматизации функционального тестирования маршрутизаторов. 

## Быстрый старт

Установка:
```bash
pip install PyRouterTest
```

Описание данных для подключения:
```yaml
env:
    node1:
        hostname: 192.168.0.105
        username: user1
        password: 12345
    node2:
        hostname: 192.168.0.110
        username: user2
        password: 12345
```

Описание окружения:

```yaml
common:
  - id: ip
    execute:
      - interface @interface
      - ip address @ip
      - no shutdown
      - exit
  - id: ip_lo
    execute:
      - interface lo @num
      - ip address @ip
      - no shutdown
      - exit

env:
  node1:
    - configure terminal
    - command: ip
      variables:
        interface: eth2
        ip: 20.20.20.1/24
    - command: ip_lo
      variables:
        num: 1
        ip: 101.0.0.1/24  
```

Создание теста:
```python
@env("env.yml")
@connection("connection.yml")
class BGPTestSuite(RouterTest):
    ping_answer = "30 packets transmitted""

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
    @order(value=2)
    def Node1PingTestCase(self, connection: Connection):
        should_not_contains(do_ping(connection, "102.0.0.1", "101.0.0.1", 30), self.ping_answer)
        should_not_contains(do_ping(connection, "103.0.0.1", "101.0.0.1", 30), self.ping_answer)


```

## Возможности

- Автоопределение тестовых случаев
- Поддержка Allure
- CLI интерфейс 

## Лицензия

[MIT](LICENSE)
