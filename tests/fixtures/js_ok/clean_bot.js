// js_ok/clean_bot.js — negative fixture (should PASS)
// This file demonstrates clean discord.js 14 patterns

const { Client, GatewayIntentBits } = require('discord.js');

// GOOD: Explicit intents
const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
    ],
});

// GOOD: No hardcoded token
client.login(process.env.DISCORD_TOKEN);
