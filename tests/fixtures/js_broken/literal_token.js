// js_broken/literal_token.js — DB011 positive fixture
// This file passes a literal token to client.run (BAD)
// WARNING: The token below is intentionally fake and for testing only

const { Client, GatewayIntentBits } = require('discord.js');
const client = new Client({ intents: [GatewayIntentBits.Guilds] });

// BAD: Literal token passed to login (fake token for testing only)
client.login('FAKE_TOKEN_FOR_TESTING_ONLY_1234567890abcdef1234567890abcdef1234567890');
