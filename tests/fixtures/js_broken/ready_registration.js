// js_broken/ready_registration.js — DB003 positive fixture
// This file registers commands in the ready handler (BAD)

const { Client, GatewayIntentBits } = require('discord.js');
const client = new Client({ intents: [GatewayIntentBits.Guilds] });

// BAD: Registration inside ready handler
client.on('ready', async () => {
    const commands = [
        { name: 'ping', description: 'Ping command' },
    ];
    await client.application.commands.set(commands);
});

client.login('a.b.c');
