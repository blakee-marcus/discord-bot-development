// js_broken/unbounded_collector.js — DB005 positive fixture
// This file uses a collector without timeout (BAD)

const { Client, GatewayIntentBits } = require('discord.js');
const client = new Client({ intents: [GatewayIntentBits.Guilds] });

client.on('interactionCreate', async interaction => {
    if (!interaction.isMessageComponent()) return;

    // BAD: No time limit on collector
    const collector = message.createMessageComponentCollector({
        filter: i => i.user.id === interaction.user.id,
    });

    collector.on('collect', async i => {
        await i.update({ content: 'Collected' });
    });
});

client.login('a.b.c');
