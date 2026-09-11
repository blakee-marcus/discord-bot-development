// js_broken/hardcoded_token.js — DB001 positive fixture
// This file contains a hardcoded token (BAD)
// WARNING: The token below is intentionally fake for testing purposes only

const Discord = require('discord.js');
const client = new Discord.Client({ intents: [] });

// BAD: Hardcoded token (obviously fake — for testing only)
client.login('FAKE_TOKEN_FOR_TESTING_ONLY_1234567890abcdef.FAKE_TOKEN.FAKE_TOKEN');

client.on('ready', () => {
    console.log('Bot is ready');
});
