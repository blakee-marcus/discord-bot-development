// js_broken/legacy_api.js — DB002 positive fixture
// This file uses legacy discord.js v12/v13 APIs (BAD)

const Discord = require('discord.js');
const client = new Discord.Client();

// BAD: Legacy event name
client.on('message', message => {
    console.log(message.content);
});

// BAD: Legacy embed API
client.on('messageCreate', message => {
    const embed = new Discord.MessageEmbed()
        .setTitle('Test')
        .addField('Field', 'Value')
        .addFields({ name: 'F1', value: 'V1' })
        .setThumbnail('https://example.com/img.png');
    message.channel.send({ embeds: [embed] });
});

// BAD: Legacy reaction collector
const collector = message.createReactionCollector({ time: 15000 });
collector.on('collect', (reaction, user) => {
    console.log(user.username);
});

client.login('a.b.c');
