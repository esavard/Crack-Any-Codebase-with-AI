# nats

_A product story reverse engineered from the codebase._

## The pitch

> It's like Gmail for software services, but messages are not stored, so a service must be online and subscribed to a subject to receive a message.

## The pain

> Priya, a developer building an e-commerce site, moves her `inventory` program to a new server, and suddenly the `shopping-cart`, `checkout`, and `shipping` programs all crash. Her real competitor isn't another messaging tool; it's the tangled web of hard-coded IP addresses and port numbers she now has to hunt down and fix in every single program.

## Where it sits

### What it gives up

- NATS gives up being a "system of record" by default, which is the core identity of systems like Kafka.
- It maintains two distinct messaging models (core pub/sub and JetStream streaming), which can add a slight learning curve.
- It forgoes the vast ecosystem of tools built specifically for Kafka's log-centric architecture, like Kafka Connect.
- Core NATS offers "at-most-once" delivery, sacrificing the default "at-least-once" guarantee that durable systems provide out of the box.

### What it gets in return

- It gains extreme operational simplicity by being a single, dependency-free binary that can run almost anywhere.
- It serves high-performance, low-latency use cases where Kafka's mandatory persistence would be unnecessary overhead.
- It offers a single system that scales from simple messaging to durable streaming, reducing architectural complexity.
- It has a native, decentralized multi-tenancy model built for modern distributed systems, avoiding complex ACL management.

### Why incumbents can't copy this

Kafka's identity and ecosystem are built entirely around the durable, replayable log. Offering a simple, non-durable mode would undermine its core value proposition as a system of record and cannibalize its own positioning. Architecturally, adding a separate transient messaging path would be like building a second product, destroying the elegance of its "everything is a log" design. Similarly, adopting NATS's decentralized security model would require a fundamental break from centralized ACLs, invalidating years of community tooling and operational knowledge.

### Side by side

**Dimensions**

- **Default Messaging Behavior**: Is the system primarily a simple message passer or a durable, replayable log out of the box?
- **Secure Data Sharing**: Can you securely and dynamically share specific data streams between different teams or tenants without a central admin?
- **Running the System**: Can you run the core system from a single file without external dependencies like Zookeeper or a language runtime?
- **Persistence is Optional**: Can you run the system in a high-performance, non-persistent mode and add durability later?

| Product | Default Messaging Behavior | Secure Data Sharing | Running the System | Persistence is Optional |
| --- | --- | --- | --- | --- |
| **NATS** | **Simple by default**. Core NATS is a fast, fire-and-forget message passer; the more complex JetStream log system is opt-in via a config flag (-js). | **Built-in**. NATS has a decentralized security model of accounts, with stream and service imports/exports managed by JWTs (server/accounts.go). | **One file**. The nats-server is a single Go binary with no external dependencies needed to run (main.go). | **Yes**. Persistence is provided by the JetStream subsystem, which is disabled by default and can be enabled with a flag (-js) and configured in server/jetstream.go. |
| **Apache Kafka** | **Durable log only**. Kafka's core abstraction is a durable, replayable log; it does not have a simple, transient messaging mode. | **Via ACLs**. Kafka uses centralized Access Control Lists for authorization, which are powerful but less tailored for dynamic, cross-tenant sharing. | **Requires framework**. Kafka is a JVM application and historically required a separate Zookeeper cluster for coordination, making it complex to deploy. | **No**. Persistence is fundamental to Kafka's design as a distributed log; it cannot be disabled. |
| **RabbitMQ** | **Message queue**. RabbitMQ is a traditional message broker that routes messages to ephemeral or durable queues, which are then consumed. | **Via vhosts**. Uses virtual hosts for multi-tenancy, which provides strong isolation but not the granular, dynamic data sharing of NATS imports/exports. | **Requires framework**. RabbitMQ requires an Erlang/OTP runtime environment, which is an external dependency that must be installed and managed. | **Partial**. Messages can be marked as transient or persistent, but the model is a queue, not a replayable log like JetStream. |
| **Redis** | **Simple by default**. Redis Pub/Sub is a simple fire-and-forget system; Redis Streams provides a log model, but it's a separate command set. | **Via ACLs**. Redis provides an ACL system for user permissions, but it lacks the decentralized, policy-based import/export model of NATS. | **One file**. Like NATS, Redis is a single binary with no external runtime dependencies, known for its operational simplicity. | **Yes**. Core Redis Pub/Sub has no persistence guarantees; persistence for the entire dataset is configured separately via RDB or AOF. |

## Hiding in the code

### Built-in service latency tracking
_server/accounts.go: serviceLatency struct, TrackServiceExportWithSampling()_

NATS is not just a transport layer, but an observable service fabric. The bet is that as request-reply workloads become more critical, built-in latency metrics will be a key differentiator against simpler message queues.

### Weighted subject mapping for traffic shaping
_server/accounts.go: AddWeightedMappings(), mapping struct_

The product is moving towards service mesh territory, managing not just message delivery but also routing logic. This enables canary deployments and A/B testing at the messaging layer, reducing client-side complexity.

### Leaf node architecture for edge computing
_server/client.go: const LEAF, server/leafnode.go_

The network edge is the next frontier for distributed systems. NATS is betting that a dedicated, secure protocol for connecting edge clusters to a central hub, with awareness of the interest graph, is critical infrastructure.

### TPM support for hardware-backed encryption
_server/jetstream.go: func (s *Server) initJetStreamEncryption()_

For high-security environments, software-only key management is insufficient. The bet is that hardware-level security for JetStream's at-rest encryption will be a requirement for adoption in finance, government, and critical IoT.

### Latency-aware data compression
_server/client.go: c.out.cw *s2.Writer, server/route.go: CompressionS2Auto_

Network bandwidth is not always cheap or plentiful, especially at the edge or between data centers. A smart, built-in compression that adapts to network conditions is a bet on optimizing for real-world, heterogeneous network environments.

### Full-featured administration via internal API
_server/jetstream_api.go: JSApiStreamSnapshot, JSApiStreamRestore, JSApiLeaderStepDown_

Cloud-native systems require automation at every level. The bet is that operators will prefer managing infrastructure using the same NATS protocol they use for applications, enabling GitOps-style management and deeper integration.

## Missing on purpose

### No plugin architecture
_Features like MQTT and websockets are compiled in; no `plugins/` directory or dynamic loading code._

Prioritizes performance, operational simplicity, and reliability over ultimate extensibility. A single binary is easy to deploy and manage, avoiding dependency hell with plugins. Risk: The core team becomes a bottleneck for new protocols.

### No built-in web dashboard
_server/server.go defines HTTP endpoints like /varz and /connz which serve JSON, but no bundled UI._

Commits to being a component in a larger observability stack, not an all-in-one solution. This avoids the cost of maintaining a complex UI and encourages integration with best-of-breed tools like Grafana. Risk: Higher barrier to entry for users wanting a simple, out-of-the-box visualization tool.

### No native SSO or federated identity support
_Auth logic in server/accounts.go and server/client.go is built on NKeys, JWTs, and tokens, with no mention of LDAP, OIDC, or SAML._

The security model is self-contained, decentralized, and built on modern cryptography, fitting its distributed systems target. This simplifies deployment in isolated environments. Risk: More integration work for enterprises needing to connect with existing identity providers.

### No external database for persistence
_Core NATS is in-memory; JetStream uses its own log-structured file store in `StoreDir`, with no database connectors._

Ensures maximum performance for core messaging by avoiding disk I/O. It positions JetStream as the single, opinionated persistence layer, preventing users from using potentially slow or misconfigured backends. Risk: Less flexibility for users wanting to leverage existing databases.

### No multi-message distributed transactions
_No BeginTx/Commit/Rollback commands in the protocol; JetStream's `AllowAtomicPublish` is for batch atomicity, not general transactions._

Keeps the server simple and fast by avoiding the complexity and performance overhead of two-phase commit protocols. This pushes transactional logic to the application layer. Risk: More complex for developers who need strict transactional guarantees across multiple, independent messages.
