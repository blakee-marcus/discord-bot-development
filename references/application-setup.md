# Application Setup

**Checked on:** 2026-09-10
**Sources:**
- https://docs.discord.com/developers/quick-start/overview-of-apps
- https://docs.discord.com/developers/quick-start/getting-started
- https://docs.discord.com/developers/resources/application
- https://docs.discord.com/developers/reference#authentication

## Application Creation

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click **New Application**. New applications include a bot user by default.
3. Store these separately — never commit them:
   - **Application ID** (snowflake, public identifier)
   - **Interaction public key** (for webhook signature verification)
   - **Bot token** (secret; authorizes API requests and carries permissions)

## Token Handling

- Bot tokens authorize requests and carry the app's permissions.
- Discord's Developer Terms prohibit embedding credentials in open-source projects.
- Use environment variables or a managed secret store.
- Rotate immediately after suspected exposure.
- Never log tokens; redact on any error path.

## Installation Contexts

Discord supports multiple installation contexts:

| Context | Description |
|---------|-------------|
| `GUILD_INSTALL` (`0`) | Installed to a server/guild |
| `USER_INSTALL` (`1`) | Installed to a user account |

Set `integration_type` explicitly when constructing custom OAuth2 URLs. The
interaction payload includes the installation context, which determines the
value of `guild_id` (guild install) vs `user` (user install).

**Source:** https://docs.discord.com/developers/resources/application#installation-context

## Public Key & Signature Verification

For HTTP-based interactions (webhooks), validate every request's Ed25519
signature over the exact raw body using:
- `X-Signature-Ed25519` (hex-encoded)
- `X-Signature-Timestamp` (Unix timestamp)

Reject requests with missing headers, stale timestamps, or invalid signatures.
See `references/security-and-policy.md` for the full verification procedure.

## Enabling the Bot

In the Developer Portal:
1. Navigate to **Bot** under **Settings**.
2. Enable required **Privileged Gateway Intents** (see `references/gateway-and-intents.md`).
3. Set the bot's **Public Bot** toggle appropriately.
4. Configure **OAuth2** redirect URIs if using OAuth2 flows.

## Drift Hazards

- Discord occasionally changes the Developer Portal UI; the API surface is more stable.
- Privileged intent requirements change; always check current thresholds.
- The `integration_type` field is newer than older tutorials — older guides may omit it.
