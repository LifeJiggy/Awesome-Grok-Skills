# Zero Trust Security Resources

## Quick Reference

| Resource | Type | Description |
|----------|------|-------------|
| `oauth-config.md` | Config | OAuth 2.0 Authorization Server Configuration |
| `envoy-mtls.yaml` | Config | Mutual TLS Configuration for Envoy |
| `compliance-checklist.md` | Documentation | Zero Trust Compliance Checklist |
| `security-tools.md` | Documentation | Security Testing Tools |

---

## OAuth 2.0 / OIDC Configuration

```yaml
authorization_server:
  issuer: "https://auth.example.com"
  authorization_endpoint: "https://auth.example.com/oauth2/authorize"
  token_endpoint: "https://auth.example.com/oauth2/token"
  userinfo_endpoint: "https://auth.example.com/oauth2/userinfo"
  jwks_uri: "https://auth.example.com/.well-known/jwks.json"
  
  supported_grant_types:
    - "authorization_code"
    - "refresh_token"
    - "client_credentials"
  
  token_config:
    access_token_lifetime: 3600
    refresh_token_lifetime: 2592000
    token_signing_algorithm: "RS256"
```

---

## API Gateway Security Policy (Kong)

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: zero-trust-auth
config:
  jwt_verification:
    key_claim_name: "iss"
    claims_to_verify:
      - "exp"
      - "iat"
      - "nbf"
    run_on_preflight: true
  
  rate_limiting:
    minute: 100
    hour: 1000
  
  ip_restriction:
    allow:
      - "10.0.0.0/8"
      - "172.16.0.0/12"
```

---

## mTLS Configuration (Envoy)

```yaml
static_resources:
  listeners:
    - name: https
      address:
        socket_address:
          address: 0.0.0.0
          port_value: 443
      filter_chains:
        - filters:
            - name: envoy.filters.network.http_connection_manager
              typed_config:
                "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
                stat_prefix: ingress_http
                route_config:
                  name: local_route
                  virtual_hosts:
                    - name: backend
                      domains: ["*"]
                      routes:
                        - match:
                            prefix: "/"
                          route:
                            cluster: backend_service
          transport_socket:
            name: envoy.transport_socket.tls
            typed_config:
              "@type": type.googleapis.com/envoy.extensions.transport_sockets.tls.v3.DownstreamTlsContext
              require_client_certificate: true
              common_tls_context:
                tls_certificates:
                  - certificate_chain:
                      filename: /etc/envoy/certs/server.crt
                    private_key:
                      filename: /etc/envoy/certs/server.key
                validation_context:
                  trusted_ca:
                    filename: /etc/envoy/certs/ca.crt
```

---

## Security Header Middleware (Node.js)

```typescript
import { Request, Response, NextFunction } from 'express';

interface SecurityConfig {
  contentSecurityPolicy?: Record<string, string[]>;
  strictTransportSecurity?: {
    maxAge: number;
    includeSubDomains: boolean;
    preload: boolean;
  };
}

const defaultConfig: SecurityConfig = {
  contentSecurityPolicy: {
    "default-src": ["'self'"],
    "script-src": ["'self'", "'unsafe-inline'"],
    "style-src": ["'self'", "'unsafe-inline'"],
    "img-src": ["'self'", 'data:', 'https:'],
    "object-src": ["'none'"],
    "frame-src": ["'none'"]
  },
  strictTransportSecurity: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  }
};

export function securityHeaders(config: SecurityConfig = defaultConfig) {
  return (req: Request, res: Response, next: NextFunction): void => {
    if (config.contentSecurityPolicy) {
      const directives = Object.entries(config.contentSecurityPolicy)
        .map(([k, v]) => `${k.replace(/([A-Z])/g, '-$1').toLowerCase()} ${v.join(' ')}`)
        .join('; ');
      res.setHeader('Content-Security-Policy', directives);
    }
    
    if (config.strictTransportSecurity) {
      const sts = `max-age=${config.strictTransportSecurity.maxAge}`;
      const includeSubDomains = config.strictTransportSecurity.includeSubDomains ? '; includeSubDomains' : '';
      const preload = config.strictTransportSecurity.preload ? '; preload' : '';
      res.setHeader('Strict-Transport-Security', sts + includeSubDomains + preload);
    }
    
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('X-Frame-Options', 'DENY');
    res.removeHeader('X-Powered-By');
    res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
    
    next();
  };
}
```

---

## Zero Trust Compliance Checklist

### Identity & Access Management
- Multi-factor authentication (MFA) enabled for all users
- Password policy enforced (min 12 chars, complexity)
- Account lockout after 5 failed attempts
- Privileged access management (PAM) implemented
- Just-in-time (JIT) access for admin rights
- Regular access reviews (quarterly)

### Network Security
- Network segmentation implemented
- Micro-segmentation for critical workloads
- All traffic encrypted (TLS 1.3 minimum)
- mTLS for service-to-service communication
- DDoS protection enabled
- Web Application Firewall (WAF) configured

### Monitoring & Logging
- Centralized logging (SIEM)
- Real-time threat detection
- User behavior analytics (UBA)
- All API calls logged and monitored
- Alerting for suspicious activity
- 90+ days log retention

### Data Protection
- Data classification implemented
- Encryption at rest (AES-256)
- Encryption in transit (TLS 1.3)
- Key management (HSM/KMS)
- DLP policies configured

### Application Security
- SAST/DAST in CI/CD pipeline
- Dependency vulnerability scanning
- Container image scanning
- Code signing for releases

---

## Security Testing Tools

| Tool | Purpose | URL |
|------|---------|-----|
| OWASP ZAP | Web app security testing | https://www.zaproxy.org/ |
| Nmap | Network scanning | https://nmap.org/ |
| Metasploit | Penetration testing | https://www.metasploit.com/ |
| Burp Suite | Web security testing | https://portswigger.net/burp |
| Wireshark | Network protocol analysis | https://www.wireshark.org/ |
| Vault | Secrets management | https://www.vaultproject.io/ |
