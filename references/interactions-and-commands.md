# Interactions and Commands

**Checked on:** 2026-09-10
**Sources:**
- https://docs.discord.com/developers/interactions/receiving-and-responding
- https://docs.discord.com/developers/interactions/application-commands
- https://docs.discord.com/developers/interactions/message-components
- https://docs.discord.com/developers/components/reference

## Interaction Lifecycle

An interaction is the message your app receives when a user uses an application
command or message component. For slash commands, it includes the submitted values.

### Acknowledgement Timing (CRITICAL)

- **3-second deadline**: Send an initial interaction response or defer within
  3 seconds or the interaction token invalidates.
- **15-minute token validity**: Interaction tokens remain valid for 15 minutes
  for edits and follow-ups.
- **Exact-one initial response**: A given interaction can be acknowledged exactly
  once. Use `is_done()` guards before any response method.

### Callback Types

| Type | Name | Use When |
|------|------|----------|
| 4 | `CHANNEL_MESSAGE_WITH_SOURCE` | Response is ready immediately |
| 5 | `DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE` | Work cannot finish in 3s |
| 6 | `DEFERRED_UPDATE_MESSAGE` | Deferring a component interaction |
| 7 | `UPDATE_MESSAGE` | Updating a component's message |
| 8 | `APPLICATION_COMMAND_AUTOCOMPLETE_RESULT` | Returning autocomplete choices |
| 9 | `MODAL` | Showing a modal |
| 10 | `PREMIUM_REQUIRED` | Premium upsell |

**Source:** https://docs.discord.com/developers/interactions/receiving-and-responding#interaction-callback

## Application Commands

### Command Types

| Type | Description |
|------|-------------|
| `CHAT_INPUT` (1) | Slash command |
| `USER` (2) | User context menu |
| `MESSAGE` (3) | Message context menu |

### Registration

**Commands can only be registered via HTTP endpoints, never over the Gateway.**

- **Guild commands**: scoped to a specific guild; update instantly.
- **Global commands**: available on all guilds; propagate up to 1 hour.

**Development workflow**: Use guild commands for development (instant updates),
then bulk-overwrite to global for release.

### Bulk Registration

Use `PUT /applications/{application.id}/commands` (global) or
`PUT /applications/{application.id}/guilds/{guild.id}/commands` (guild) to
bulk-overwrite all commands. This replaces the entire command set.

**Rate limit**: 200 application command creates per day, per guild.

### Command Names

- Unique per application, per type, within each scope (global and guild).
- Must match `^[-_\p{L}\p{N}\p{sc=Deva}\p{sc=Thai}]{1,32}$` (updated regex).
- Guild commands are not available in DMs.

## Message Components

Components are interactive elements attached to messages:

- Buttons
- Select menus (string, user, role, mentionable, channel)
- Text inputs (in modals)

**Component v2** is the current standard (2026). Components are identified by
`custom_id` — never trust this value without authorization.

## Modals

Modals are pop-up forms for additional input. They block the user until
submitted or dismissed. Use callback type `9` (`MODAL`) to show a modal.

## Autocomplete

Autocomplete interactions return choices as the user types. Respond within
3 seconds with callback type `8`.

## Contexts

Commands have two sets of contexts:
- **Guild install**: available in guilds
- **User install**: available in DMs and group DMs

Configure `contexts` and `integration_types` when creating commands.

## Drift Hazards

- Command name regex changed in 2022; older guides may show the old pattern.
- Component v1 is deprecated; use v2.
- The `description` field is required for `CHAT_INPUT` commands.
- `default_member_permissions` replaced `default_permission` (boolean).
