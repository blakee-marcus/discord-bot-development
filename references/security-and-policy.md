# Security and Policy

**Checked on:** 2026-09-10
**Sources:**
- https://docs.discord.com/developers/policies-and-agreements/developer-terms-of-service
- https://docs.discord.com/developers/interactions/receiving-and-responding#security-and-authorization
- https://docs.discord.com/developers/reference#authentication

## Token Security

- **Never embed tokens in source code** or commit them to version control.
- **Never log tokens** in error messages or debug output.
- Use environment variables or a managed secret store.
- **Rotate immediately** after suspected exposure.
- Discord's Developer Terms prohibit embedding credentials in open-source projects.

## Webhook Signature Verification (Ed25519)

For HTTP-based interactions (webhooks), validate every request's signature:

### Headers

| Header | Description |
|--------|-------------|
| `X-Signature-Ed25519` | Hex-encoded Ed25519 signature |
| `X-Signature-Timestamp` | Unix timestamp when the request was sent |

### Verification Steps

1. Read the **exact raw request body** (do not parse/re-serialize).
2. Concatenate `timestamp + raw_body`.
3. Verify the Ed25519 signature using your interaction public key.
4. **Reject** requests with:
   - Missing headers
   - Stale timestamps (older than ~5 minutes)
   - Invalid signatures

### Python Example
```python
import nacl.signing
import nacl.exceptions

def verify_signature(body: bytes, signature: str, timestamp: str, public_key: str) -> bool:
    try:
        verify_key = nacl.signing.VerifyKey(bytes.fromhex(public_key))
        verify_key.update(timestamp.encode() + body)
        verify_key.verify(bytes.fromhex(signature))
        return True
    except nacl.exceptions.BadSignatureError:
        return False
```

### JavaScript Example
```javascript
const { verifyKey } = require('discord-interactions');

function verifySignature(body, signature, timestamp, publicKey) {
    return verifyKey(body, signature, timestamp, publicKey);
}
```

## allowed_mentions

Set `allowed_mentions` explicitly to avoid unexpected pings:

```json
{
    "allowed_mentions": {
        "parse": ["users"],
        "users": ["123456789012345678"],
        "roles": [],
        "replied_user": false
    }
}
```

**Never allow `@everyone` or `@here` mentions** unless explicitly required.

## Data Handling

- Don't store message content longer than necessary.
- Don't share user data with third parties.
- Comply with Discord's Developer Terms of Service.
- Implement proper data retention policies.

## Privileged Intent Thresholds (Known Doc Conflict)

**Discord's current privileged-intent and verification thresholds conflict across
different documentation pages.** This skill surfaces the conflict rather than
silently resolving it:

- Some docs state 100 guilds for privileged intents.
- Some docs state verification is required for 100+ guilds.
- The actual threshold may differ from what's documented.

**Always check the most current thresholds** before requesting privileged intents.

## Self-Bots

**Self-bots are prohibited.** A bot must use a bot token, not a user token.
Automating a user account is a ToS violation.

## Drift Hazards

- Discord's Developer Terms change periodically.
- Privileged intent thresholds change.
- Signature verification requirements may change.
- The `allowed_mentions` format has evolved.
