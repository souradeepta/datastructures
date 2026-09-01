from python.system_design.load_balancer import (
    LeastConnectionsStrategy,
    LoadBalancer,
    RoundRobinStrategy,
    Server,
)


def make_servers():
    return [
        Server(1, "10.0.0.1", 8000),
        Server(2, "10.0.0.2", 8000),
        Server(3, "10.0.0.3", 8000),
    ]


def test_round_robin_routes_in_rotation():
    servers = make_servers()
    balancer = LoadBalancer(RoundRobinStrategy())
    for server in servers:
        balancer.add_server(server)

    responses = [balancer.route_request(str(i)) for i in range(4)]
    assert ["Server 1" in response for response in responses] == [True, False, False, True]
    assert ["Server 2" in response for response in responses] == [False, True, False, False]


def test_round_robin_skips_unhealthy_server():
    servers = make_servers()
    servers[1].set_healthy(False)
    strategy = RoundRobinStrategy()

    assert strategy.select_server(servers) is servers[0]
    assert strategy.select_server(servers) is servers[2]
    assert strategy.select_server(servers) is servers[0]


def test_least_connections_selects_lowest_healthy_count():
    servers = make_servers()
    servers[0].active_connections = 4
    servers[1].active_connections = 1
    servers[2].active_connections = 2
    servers[1].set_healthy(False)

    assert LeastConnectionsStrategy().select_server(servers) is servers[2]


def test_remove_server_and_no_healthy_server_behavior():
    servers = make_servers()
    balancer = LoadBalancer(RoundRobinStrategy())
    for server in servers:
        balancer.add_server(server)
    balancer.remove_server(2)
    assert all(server.server_id != 2 for server in balancer.servers)

    for server in balancer.servers:
        server.set_healthy(False)
    assert balancer.route_request("request") == "No healthy servers available"
