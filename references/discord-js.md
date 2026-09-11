# discord.js Reference

**Checked on:** 2026-09-10
**Sources:**
- https://discord.js.org/docs/packages/discord.js/14.27.0
- https://discordjs.guide/
- https://raw.githubusercontent.com/discordjs/discord.js/14.27.0/packages/discord.js/package.json

## Version Snapshot

| Field | Value |
|-------|-------|
| Version | **14.27.0** |
| Released | 2026-07-15 |
| Node (package) | >=18 |
| Node (guide rec) | >=22.12.0 |
| discord-api-types | v10 |
| Status | Stable |

discord.js v15 is **pre-release** — do not use for production.

## Installation

```bash
npm install discord.js
# or
yarn add discord.js
# or
pnpm add discord.js
```

## Client Setup

```javascript
const { Client, GatewayIntentBits } = require('discord.js');

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent,  // Privileged
    ],
});

client.login(process.env.DISCORD_TOKEN);
```

## Intents

Always specify intents explicitly:

```javascript
const { GatewayIntentBits } = require('discord.js');

const intents = [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.GuildMembers,      // Privileged
    GatewayIntentBits.GuildPresences,    // Privileged
    GatewayIntentBits.MessageContent,    // Privileged
];
```

## Events

### Ready Event

```javascript
client.once('ready', () => {
    console.log(`Logged in as ${client.user.tag}`);
});
```

### Interaction Create

```javascript
client.on('interactionCreate', async interaction => {
    if (interaction.isChatInputCommand()) {
        await handleCommand(interaction);
    } else if (interaction.isButton()) {
        await handleButton(interaction);
    } else if (interaction.isModalSubmit()) {
        await handleModal(interaction);
    }
});
```

## REST / Gateway Separation

The umbrella `discord.js` client exposes both:
- `client.rest` — REST operations, command registration
- `client.ws` — Gateway WebSocket

For command registration scripts, use `REST` only:

```javascript
const { REST, Routes } = require('discord.js');

const rest = new REST({ version: '10' }).setToken(process.env.DISCORD_TOKEN);

await rest.put(Routes.applicationCommands(clientId), { body: commands });
```

## Collectors

Collectors are time-limited listeners. **Always set a timeout:**

```javascript
const filter = i => i.user.id === interaction.user.id;
const collector = message.createMessageComponentCollector({
    filter,
    time: 15_000,  // 15 seconds
    max: 1,
});

collector.on('collect', async i => {
    await i.update({ content: 'Collected!' });
});

collector.on('end', collected => {
    if (collected.size === 0) {
        interaction.editReply({ content: 'Timed out!' });
    }
});
```

## Modals

```javascript
const { ModalBuilder, TextInputBuilder, TextInputStyle, ActionRowBuilder } = require('discord.js');

const modal = new ModalBuilder()
    .setCustomId('myModal')
    .setTitle('My Modal');

const input = new TextInputBuilder()
    .setCustomId('myInput')
    .setLabel('Input')
    .setStyle(TextInputStyle.Short);

const row = new ActionRowBuilder().addComponents(input);
modal.addComponents(row);

await interaction.showModal(modal);
```

## Cache Sweepers

discord.js caches everything by default. Configure sweepers to reduce memory:

```javascript
const client = new Client({
    intents: [GatewayIntentBits.Guilds],
    sweepers: {
        messages: {
            interval: 300,  // 5 minutes
            lifetime: 600,  // 10 minutes
        },
    },
});
```

## Error Handling

```javascript
client.on('error', error => {
    console.error('Client error:', error);
});

client.on('warn', info => {
    console.warn('Client warning:', info);
});

process.on('unhandledRejection', error => {
    console.error('Unhandled promise rejection:', error);
});
```

## Rate Limit Handling

discord.js handles 429s automatically with `Retry-After`. For custom handling:

```javascript
client.rest.on('rateLimited', info => {
    console.warn('Rate limited:', info);
});
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `new Discord.Client()` | `new Client({ intents: [...] })` — intents required |
| `client.on('message')` | `client.on('messageCreate')` — v14 renamed |
| `message.reply()` without `allowed_mentions` | Always set `allowed_mentions` |
| `interaction.reply()` twice | Use `is_done()` guard or `deferReply` |
| `await` outside `async` | All interaction handlers must be async |
| `require('discord.js').Client` | Use `const { Client } = require('discord.js')` |
| `new MessageEmbed()` | `new EmbedBuilder()` — v14 renamed |
| `client.destroy()` without re-login | Call `client.login()` again to reconnect |
| Collectors without timeout | Always set `time` option |
| `guild.members.fetch()` without `GUILD_MEMBERS` intent | Add intent or use cache |
| `client.login(token)` with token in code | Use `process.env.DISCORD_TOKEN` |

## Drift Hazards

- v14 → v15 migration is breaking; v15 is pre-release.
- The `main` branch shows Node 22.12.0 requirement; tagged 14.27.0 package says >=18.
- `discord-api-types` v10 is current; v9 is deprecated.
- Event names changed between v13 and v14.
- Embed builder replaced `MessageEmbed`.
