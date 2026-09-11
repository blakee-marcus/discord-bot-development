# Testing and Deployment

**Checked on:** 2026-09-10
**Sources:**
- https://discordjs.guide/improving-dev-environment/testing.html
- https://discordpy.readthedocs.io/en/stable/testing.html
- https://docs.discord.com/developers/testing

## Test Strategy

### 1. Unit Tests

Test command handlers, utility functions, and business logic in isolation.

**discord.js (Jest/Vitest):**
```javascript
const { SlashCommandBuilder } = require('discord.js');

test('ping command returns pong', async () => {
    const interaction = {
        reply: jest.fn(),
        commandName: 'ping',
        options: { data: [] },
    };
    await handlePing(interaction);
    expect(interaction.reply).toHaveBeenCalledWith('Pong!');
});
```

**discord.py (pytest):**
```python
import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.mark.asyncio
async def test_ping_command():
    interaction = MagicMock()
    interaction.response = MagicMock()
    interaction.response.send_message = AsyncMock()
    
    await ping_command(interaction)
    
    interaction.response.send_message.assert_called_once_with("Pong!")
```

### 2. Integration Tests

Test the full command flow with mocked Discord API responses.

### 3. Test-Guild Smoke Tests

- Use a **separate application** and **separate guild** for testing.
- Register guild commands to the test guild.
- Verify commands appear, can be invoked, and respond correctly.
- **Never use a production token or production guild in CI.**

## Test Matrix

| Test Type | Framework | What It Verifies |
|-----------|-----------|------------------|
| Unit tests | Jest/Vitest/pytest | Command handlers, utilities |
| Mock tests | discord.js RESTMock | API request formatting |
| Integration | Manual/Automated | Full flow with mocks |
| Smoke tests | Test guild | Real registration and invocation |
| Load tests | Custom | Shard scaling, rate limits |

## Mocking

### discord.js

Use `discord.js`'s built-in mock utilities or `RESTMock`:

```javascript
const { RESTMock } = require('discord.js');
const rest = RESTMock.setToken('test-token');
```

### discord.py

Use `unittest.mock`:

```python
from unittest.mock import AsyncMock, MagicMock, patch

@pytest.mark.asyncio
async def test_api_call():
    with patch('discord.http.HTTPClient.request') as mock_request:
        mock_request.return_value = AsyncMock(return_value={})
        # ... test code
```

## CI/CD

### GitHub Actions (Node.js)

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18.x, 20.x, 22.x]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm ci
      - run: npm test
      - run: npm run lint
```

### GitHub Actions (Python)

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11', '3.12']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -e ".[test]"
      - run: pytest
      - run: ruff check .
```

## Deployment

### Environments

| Environment | Purpose | Token |
|-------------|---------|-------|
| Development | Local testing | Dev bot token |
| Staging | Pre-prod verification | Staging bot token |
| Production | Live bot | Production bot token |

### Deployment Checklist

- [ ] All tests pass
- [ ] Linting passes
- [ ] Type checking passes (if applicable)
- [ ] Secrets configured in environment
- [ ] Process manager configured
- [ ] Observability/metrics set up
- [ ] Graceful shutdown verified
- [ ] Health checks configured

## Drift Hazards

- Discord API version changes can break mocks.
- Test guilds may have different behavior than production.
- CI runners may have different timezones/rate limits.
