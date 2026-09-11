// js_broken/missing_intents.js — DB004 positive fixture
// This file creates a client without explicit intents (BAD)

const { Client } = require('discord.js');

// BAD: No intents specified
const client = new Client();

client.on('ready', () => {
    console.log('Ready');
});

client.login('a.b.c');
