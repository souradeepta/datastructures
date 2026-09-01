"""Load Balancer - Distribute requests across servers"""

from abc import ABC, abstractmethod
from enum import Enum
import random


class Server:
    """Backend server"""

    def __init__(self, server_id: int, ip: str, port: int):
        self.server_id = server_id
        self.ip = ip
        self.port = port
        self.active_connections = 0
        self.is_healthy = True

    def handle_request(self, request: str) -> str:
        """Handle incoming request"""
        if not self.is_healthy:
            return f"Server {self.server_id} is down"
        self.active_connections += 1
        result = f"Server {self.server_id} ({self.ip}:{self.port}) handled request: {request}"
        self.active_connections -= 1
        return result

    def set_healthy(self, healthy: bool):
        """Set server health status"""
        self.is_healthy = healthy


class BalancingStrategy(ABC):
    """Load balancing strategy"""

    @abstractmethod
    def select_server(self, servers: list) -> Server:
        """Choose a healthy server from the pool."""
        raise NotImplementedError


class RoundRobinStrategy(BalancingStrategy):
    """Round robin - rotate through servers"""

    def __init__(self):
        self.current_index = 0

    def select_server(self, servers: list) -> Server:
        healthy_servers = [s for s in servers if s.is_healthy]
        if not healthy_servers:
            return None
        server = healthy_servers[self.current_index % len(healthy_servers)]
        self.current_index += 1
        return server


class LeastConnectionsStrategy(BalancingStrategy):
    """Least connections - route to server with fewest active connections"""

    def select_server(self, servers: list) -> Server:
        healthy_servers = [s for s in servers if s.is_healthy]
        if not healthy_servers:
            return None
        return min(healthy_servers, key=lambda s: s.active_connections)


class RandomStrategy(BalancingStrategy):
    """Random - pick random server"""

    def select_server(self, servers: list) -> Server:
        healthy_servers = [s for s in servers if s.is_healthy]
        if not healthy_servers:
            return None
        return random.choice(healthy_servers)


class LoadBalancer:
    """Load balancer"""

    def __init__(self, strategy: BalancingStrategy):
        self.strategy = strategy
        self.servers = []

    def add_server(self, server: Server):
        """Add server to pool"""
        self.servers.append(server)

    def remove_server(self, server_id: int):
        """Remove server from pool"""
        self.servers = [s for s in self.servers if s.server_id != server_id]

    def route_request(self, request: str) -> str:
        """Route request to server"""
        server = self.strategy.select_server(self.servers)
        if not server:
            return "No healthy servers available"
        return server.handle_request(request)


if __name__ == "__main__":
    # Create servers
    servers = [
        Server(1, "192.168.1.1", 8000),
        Server(2, "192.168.1.2", 8000),
        Server(3, "192.168.1.3", 8000),
    ]

    print("=== Round Robin ===")
    lb = LoadBalancer(RoundRobinStrategy())
    for s in servers:
        lb.add_server(s)

    for i in range(5):
        print(lb.route_request(f"Request {i+1}"))

    print("\n=== Least Connections ===")
    lb2 = LoadBalancer(LeastConnectionsStrategy())
    for s in servers:
        lb2.add_server(s)

    servers[0].active_connections = 5
    servers[1].active_connections = 2
    for i in range(3):
        print(lb2.route_request(f"Request {i+1}"))

    print("\n=== Random ===")
    lb3 = LoadBalancer(RandomStrategy())
    for s in servers:
        s.active_connections = 0
        lb3.add_server(s)

    for i in range(5):
        print(lb3.route_request(f"Request {i+1}"))
