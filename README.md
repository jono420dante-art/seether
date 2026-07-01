# Seether Ecosystem

AI-driven technical solutions firm focusing on end-to-end technical solutions for high-ticket clients.

## Ecosystem Architecture

This project is organized as a monorepo-style ecosystem:

### Applications
- `apps/web`: React-based Dashboard (Coming Soon).
- `apps/api`: FastAPI Core for orchestration and dynamic pricing.
- `apps/worker`: Async Automation pipeline (Director-Flow V1).

### Services
- `services/dieter-core`: DIETER Scoring, Anomaly Detection, and specialized Bots (Eskom/Pricing).
- `services/neural-hub`: Security (PQC), Auth, Integrity Audit, and Financial Compliance (Invoicing Gate).

### Packages & Infrastructure
- `packages/shared`: Shared schemas, types, and configuration.
- `infra`: Docker orchestration, Postgres, Redis, and Nginx configurations.
- `docs`: Technical manuals and board-ready implementation packs.

## Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.12+

### Quick Start
```bash
cd infra
docker-compose up --build
```

## Security & Compliance
- **Quantum-Safe Key Exchange**: X25519-Shim in the core, upgradable to native ML-KEM-768.
- **DIETER Stack**: Zero-trust architecture with automated manifest hashing and real-time audit logging.
- **Financial Gates**: Automated boolean logic to enforce UK legal and financial entity compliance before invoicing.
