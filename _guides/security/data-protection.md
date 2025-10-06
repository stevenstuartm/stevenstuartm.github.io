---
title: "Data Protection"
category: Security
description: "Comprehensive coverage of data classification, encryption for data at rest/in transit/in use, privacy regulations like GDPR and HIPAA, and data loss prevention strategies."
---

---

## Data Classification

### Government Classifications
- **Unclassified**: General information
- **Confidential**: Could reasonably damage national security
- **Secret**: Could seriously damage national security
- **Top Secret**: Could gravely damage national security

### Private Sector Classifications
- **Public**: Freely available information
- **Internal**: Restricted to organization members
- **Confidential**: Limited access, business sensitive
- **Restricted**: Highly sensitive, strict access controls

## Data States and Protection

### Data at Rest
- **Full Disk Encryption**: Transparent disk-level protection
- **Database Encryption**: Column-level or transparent encryption
- **File-Level Encryption**: Selective file protection
- **Key Management**: Secure key storage and rotation

### Data in Transit
- **TLS/SSL**: Web traffic encryption
- **VPN**: Network-level encryption
- **Email Encryption**: PGP, S/MIME
- **API Security**: Authentication and encryption

### Data in Use
- **Application-Level Encryption**: Process memory protection
- **Secure Enclaves**: Hardware-protected execution
- **Homomorphic Encryption**: Computing on encrypted data
- **Access Controls**: Runtime permission enforcement

## Privacy Regulations

### General Data Protection Regulation (GDPR)
- **Scope**: EU citizens' personal data globally
- **Key Requirements**:
  - Lawful basis for processing
  - Data minimization principle
  - Right to be forgotten
  - Breach notification (72 hours)
  - Privacy by design
- **Penalties**: Up to 4% of annual revenue or €20 million

### Health Insurance Portability and Accountability Act (HIPAA)
- **Scope**: Protected Health Information (PHI) in US
- **Key Requirements**:
  - Administrative, physical, technical safeguards
  - Business associate agreements
  - Patient rights and access
  - Breach notification
- **Enforcement**: HHS Office for Civil Rights

### California Consumer Privacy Act (CCPA/CPRA)
- **Scope**: California residents' personal information
- **Rights**: Know, delete, correct, portability, opt-out
- **Business Requirements**: Privacy policies, data mapping
- **Enforcement**: California Privacy Protection Agency

## Data Loss Prevention (DLP)

### DLP Types
- **Network DLP**: Monitor data in transit
- **Endpoint DLP**: Control data on devices
- **Storage DLP**: Protect data at rest
- **Cloud DLP**: SaaS and cloud storage protection

### Implementation Strategy
- **Data Discovery**: Identify sensitive data locations
- **Classification**: Label data by sensitivity
- **Policy Creation**: Define protection rules
- **Monitoring**: Detect policy violations
- **Response**: Block, alert, or quarantine violations

---