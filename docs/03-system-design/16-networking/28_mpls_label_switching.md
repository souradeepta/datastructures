# MPLS (Multiprotocol Label Switching)

## Objective

MPLS forwards packets through a provider or enterprise network using short
labels and pre-established forwarding paths. It is useful when an operator
needs predictable traffic engineering, service separation, or VPN forwarding;
it is not an application protocol or a generic replacement for IP routing.

## Core concepts

- **FEC (Forwarding Equivalence Class):** packets treated the same way, such
  as a destination prefix, a VPN route, or a quality-of-service class.
- **LER (Label Edge Router):** an ingress LER classifies an IP packet and
  pushes a label; an egress LER removes the label and forwards the resulting
  IP packet. Edge routers may perform both roles for different flows.
- **LSR (Label Switch Router):** a core router forwards using the incoming
  label and its label-forwarding table rather than repeatedly making an IP
  longest-prefix decision.
- **LSP (Label-Switched Path):** the sequence of routers and labels used by a
  FEC from ingress to egress.

An MPLS label contains a label value, traffic-class bits, a bottom-of-stack
bit, and a TTL field. Labels can be stacked, which is central to provider
backbone and VPN designs.

## Push, swap, and pop

```text
IP packet → ingress LER: push  → core LSR: swap → egress LER: pop → IP packet
                 label 100                 100 → 240
```

- **Push:** classify the packet and add an outer label.
- **Swap:** replace the incoming label with the next-hop label.
- **Pop:** remove the label at the egress. Penultimate-hop popping can remove
  the outer label one hop earlier to simplify egress processing.

The control plane distributes label bindings; the data plane then uses the
resulting label-forwarding entries. A link or node failure requires control
plane convergence or a precomputed protection path.

## Label distribution and path control

| Mechanism | Main use | Path behavior |
|---|---|---|
| LDP | Ordinary label switching for IGP-reachable destinations | Usually follows the underlying IGP shortest path |
| RSVP-TE | Explicit traffic-engineered LSPs | Reserves or signals constraints such as bandwidth and affinity |
| BGP labeled-unicast | Carry labeled reachability between domains or route reflectors | BGP policy determines reachability; it complements, rather than replaces, the IGP |

LDP is operationally simpler and appropriate when shortest-path forwarding is
enough. RSVP-TE provides explicit constraints and fast-reroute options but adds
state, signaling, and reservation complexity. BGP-LU is useful for labeled
inter-domain or labeled core reachability and must be designed with route
policy and failure behavior in mind.

## VPN and traffic-engineering use cases

In an MPLS Layer 3 VPN, a provider edge router maps a customer route into a
VRF and typically uses a stack: an outer transport label selects the egress
provider edge, while an inner VPN label selects the customer VRF. Provider
core LSRs can forward the stack without knowing customer routes.

Other common uses include:

- steering latency-sensitive or capacity-sensitive traffic around congested
  links;
- fast reroute for planned protection paths;
- separating customers or services with VRFs and VPN labels;
- carrying IPv4, IPv6, Ethernet, or pseudowire services over one provider
  backbone.

## Failure modes and operations

- An LDP or RSVP session failure can remove label bindings and blackhole a FEC
  until alternate paths converge.
- A mismatch between IGP reachability, label bindings, and LFIB entries can
  create loops or silent drops.
- RSVP-TE bandwidth reservations can become stale after topology changes;
  admission control and alarms must reflect actual capacity.
- MTU must account for label-stack overhead, or packets may fragment or drop.
- PHP and explicit-null choices affect QoS and TTL handling; document them per
  platform and service.

Use control-plane session monitoring, label/LSP tracing, interface counters,
loss and latency probes, and tested failover procedures. Protect the control
plane and restrict who can signal or modify paths.

## MPLS versus SRv6

| Concern | MPLS | SRv6 |
|---|---|---|
| Forwarding identifier | Compact label stack | IPv6 Segment Routing Header and segment addresses |
| Existing deployment | Mature in many provider backbones and VPNs | Requires IPv6-capable forwarding and operations |
| State model | LSP and label distribution state | Source-encoded path with less per-path signaling in some designs |
| Overhead | Small labels, but stack depth matters | Larger IPv6/SRH headers can affect MTU |
| Interoperability | Strong with established MPLS VPN tooling | Attractive where IPv6 and programmable segments are already standard |

Neither is universally superior. MPLS may minimize migration risk in an
existing provider network; SRv6 can simplify explicit path programming and
service composition when the IPv6 hardware, tooling, and operational skills
are available. Compare forwarding support, MTU, observability, control-plane
complexity, and migration cost for the actual network.

## Interview prompts

1. Walk through a labeled VPN packet from customer ingress to egress.
2. When would LDP be enough, and when would RSVP-TE be justified?
3. How would you distinguish a label-forwarding failure from an IP reachability
   failure?
4. What would make you choose SRv6 for a new network?
