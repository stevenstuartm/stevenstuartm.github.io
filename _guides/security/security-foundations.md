---
title: "Security Foundations"
category: Security
---

---

## CIA-NAAA Triad

**Core Pillars (CIA)**:
- **Confidentiality**: Data accessible only to authorized users
- **Integrity**: Data remains accurate, complete, and unaltered
- **Availability**: Systems and data accessible when needed

**Extended Framework (NAAA)**:
- **Non-repudiation**: Prevents denial of participation in transactions
- **Authentication**: Verifies user/system identity
- **Authorization**: Determines access permissions
- **Accounting/Audit**: Tracks and records all activities

## Security Principles

### Economy of Mechanisms
- **Core Concept**: Complexity is the enemy of security
- **Application**: Keep security controls simple and well-understood
- **Benefit**: Reduces attack surface and maintenance overhead

### Fail-Safe Defaults
- **Core Concept**: Default to deny access when failure occurs
- **Examples**:
  - Network firewalls default-deny rules
  - Authentication timeouts requiring re-login
  - System lockdowns during security incidents

### Complete Mediation
- **Core Concept**: Every access request must be validated
- **Implementation**: No bypassing of security controls
- **Modern Application**: Zero Trust architecture

### Open Design (Kerckhoffs's Principle)
- **Core Concept**: Security through design, not obscurity
- **Application**: Assume attackers know your system architecture
- **Benefit**: Forces robust security implementation

### Separation of Privilege
- **Core Concept**: Require multiple conditions for access
- **Examples**:
  - Multi-factor authentication
  - Dual control for sensitive operations
  - Segregation of duties

### Least Privilege
- **Core Concept**: Minimum necessary access for job function
- **Implementation**:
  - Role-based access control (RBAC)
  - Just-in-time access
  - Regular access reviews

### Psychological Acceptance
- **Core Concept**: Security must be usable
- **Balance**: Strong security that users will actually follow
- **Key**: User education and intuitive design

### Work Factor
- **Core Concept**: Cost to attack exceeds potential gain
- **Measurement**: Time, resources, and expertise required
- **Goal**: Make attacks economically unfeasible

### Compromise Recording
- **Core Concept**: Comprehensive logging and monitoring
- **Components**:
  - Security event logging
  - Audit trails
  - Incident detection and response

---