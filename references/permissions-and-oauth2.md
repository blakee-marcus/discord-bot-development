# Permissions and OAuth2

**Checked on:** 2026-09-10
**Sources:**
- https://docs.discord.com/developers/topics/permissions
- https://docs.discord.com/developers/topics/oauth2
- https://docs.discord.com/developers/resources/application#installation-context
- https://docs.discord.com/developers/interactions/application-commands#authorizing-your-application

## Permission System

Permissions are a way to limit and grant abilities to users in Discord. A set of
base permissions can be configured at the guild level for different roles.

### Bitwise Permission Flags

Each permission has a bitwise integer value. Use bitwise OR to combine.

| Permission | Bitwise | Description |
|------------|---------|-------------|
| `ADMINISTRATOR` | `1 << 3` | All permissions |
| `MANAGE_GUILD` | `1 << 5` | Manage guild |
| `MANAGE_ROLES` | `1 << 28` | Manage roles |
| `MANAGE_CHANNELS` | `1 << 4` | Manage channels |
| `MANAGE_MESSAGES` | `1 << 13` | Manage messages |
| `MANAGE_WEBHOOKS` | `1 << 29` | Manage webhooks |
| `MANAGE_THREADS` | `1 << 34` | Manage threads |
| `KICK_MEMBERS` | `1 << 1` | Kick members |
| `BAN_MEMBERS` | `1 << 2` | Ban members |
| `MODERATE_MEMBERS` | `1 << 40` | Timeout members |
| `SEND_MESSAGES` | `1 << 11` | Send messages |
| `SEND_MESSAGES_IN_THREADS` | `1 << 35` | Send messages in threads |
| `READ_MESSAGE_HISTORY` | `1 << 16` | Read message history |
| `MENTION_EVERYONE` | `1 << 17` | Mention @everyone |
| `USE_EXTERNAL_EMOJIS` | `1 << 18` | Use external emojis |
| `EMBED_LINKS` | `1 << 14` | Embed links |
| `ATTACH_FILES` | `1 << 15` | Attach files |
| `ADD_REACTIONS` | `1 << 6` | Add reactions |
| `USE_APPLICATION_COMMANDS` | `1 << 31` | Use slash commands |
| `MANAGE_EVENTS` | `1 << 33` | Manage events |
| `MANAGE_THREADS` | `1 << 34` | Manage threads |
| `USE_EXTERNAL_STICKERS` | `1 << 37` | Use external stickers |
| `USE_EXTERNAL_SOUNDS` | `1 << 42` | Use external sounds |
| `CONNECT` | `1 << 20` | Connect to voice |
| `SPEAK` | `1 << 21` | Speak in voice |
| `MUTE_MEMBERS` | `1 << 22` | Mute members |
| `DEAFEN_MEMBERS` | `1 << 23` | Deafen members |
| `MOVE_MEMBERS` | `1 << 24` | Move members |
| `USE_VAD` | `1 << 25` | Use voice activity |
| `PRIORITY_SPEAKER` | `1 << 8` | Priority speaker |
| `STREAM` | `1 << 9` | Video/stream |

**Drift hazard**: Discord adds new permissions over time. Always check the
official permission table for current values.

## OAuth2

### Authorization URL Format

```
https://discord.com/api/oauth2/authorize
  ?client_id=YOUR_CLIENT_ID
  &permissions=YOUR_INTEGER
  &scope=bot%20applications.commands
  &redirect_uri=YOUR_ENCODED_URI
  &response_type=code
```

### Installation Contexts

- `integration_type=0` (GUILD_INSTALL): Bot installed to a guild
- `integration_type=1` (USER_INSTALL): Bot installed to a user account

When constructing custom OAuth2 URLs, set `integration_type` explicitly.

### Scopes

| Scope | Description |
|-------|-------------|
| `bot` | Adds the bot to a guild (legacy, still works) |
| `applications.commands` | Registers slash commands |
| `identify` | Access user's basic info |
| `guilds` | List guilds the user is in |
| `email` | Access user's email |
| `connections` | Access user's connections |

### OAuth2 Flows

1. **Authorization Code**: For server-side apps
2. **Client Credentials**: For bot-to-bot (limited use)

## Least-Privilege Permissions

**Never request all permissions.** Calculate the minimum your bot needs:
- Slash-command bots often only need `applications.commands` and `send_messages`
- Add permissions incrementally as features require them
- Use `default_member_permissions` to restrict commands to specific roles

## Authorization Checks

Always check permissions before acting:
1. Check the **user's** permissions (the command invoker)
2. Check the **bot's** permissions (the bot itself)
3. Check the **channel** overwrites (channel-specific permission overrides)
4. Check the **role** hierarchy (roles the user has)

**Never trust `custom_id`, cached members, or client-provided state alone.**

## Drift Hazards

- OAuth2 scopes can change; `bot` is legacy but still supported.
- `applications.commands` scope is required for slash command registration.
- Installation contexts (`integration_type`) are newer; older guides omit them.
- Discord's permission bit values are stable but can be added to.
