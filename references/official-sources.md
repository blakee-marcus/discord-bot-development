# Official Sources

**Checked on:** 2026-09-10
**Purpose:** Canonical URL inventory with checked-on dates, drift hazards, and changelog review checklist.

## Discord Developer Documentation

| URL | Topic | Checked |
|-----|-------|---------|
| https://docs.discord.com/developers/intro.md | Platform overview | 2026-09-10 |
| https://docs.discord.com/developers/quick-start/overview-of-apps | Application setup | 2026-09-10 |
| https://docs.discord.com/developers/quick-start/getting-started | Getting started | 2026-09-10 |
| https://docs.discord.com/developers/resources/application | Application resource | 2026-09-10 |
| https://docs.discord.com/developers/reference#authentication | Authentication | 2026-09-10 |
| https://docs.discord.com/developers/events/gateway | Gateway API | 2026-09-10 |
| https://docs.discord.com/developers/events/gateway#gateway-intents | Gateway intents | 2026-09-10 |
| https://docs.discord.com/developers/events/gateway#sharding | Sharding | 2026-09-10 |
| https://docs.discord.com/developers/events/gateway#rate-limiting | Gateway rate limits | 2026-09-10 |
| https://docs.discord.com/developers/interactions/receiving-and-responding | Interactions | 2026-09-10 |
| https://docs.discord.com/developers/interactions/application-commands | Application commands | 2026-09-10 |
| https://docs.discord.com/developers/interactions/message-components | Message components | 2026-09-10 |
| https://docs.discord.com/developers/components/reference | Component reference | 2026-09-10 |
| https://docs.discord.com/developers/topics/permissions | Permissions | 2026-09-10 |
| https://docs.discord.com/developers/topics/oauth2 | OAuth2 | 2026-09-10 |
| https://docs.discord.com/developers/topics/rate-limits | Rate limits | 2026-09-10 |
| https://docs.discord.com/developers/policies-and-agreements/developer-terms-of-service | Developer ToS | 2026-09-10 |

## discord.js Documentation

| URL | Topic | Checked |
|-----|-------|---------|
| https://discord.js.org/docs/packages/discord.js/14.27.0 | discord.js 14.27 docs | 2026-09-10 |
| https://discordjs.guide/ | discord.js Guide | 2026-09-10 |
| https://discordjs.guide/legacy/app-creation/deploying-commands | Command registration | 2026-09-10 |
| https://discordjs.guide/legacy/improving-dev-environment/pm2 | PM2 deployment | 2026-09-10 |
| https://raw.githubusercontent.com/discordjs/discord.js/14.27.0/packages/discord.js/package.json | 14.27.0 package.json | 2026-09-10 |
| https://github.com/discordjs/discord.js/releases/tag/14.27.0 | 14.27.0 release | 2026-09-10 |

## discord.py Documentation

| URL | Topic | Checked |
|-----|-------|---------|
| https://discordpy.readthedocs.io/en/stable/ | Stable docs | 2026-09-10 |
| https://discordpy.readthedocs.io/en/stable/faq.html | FAQ | 2026-09-10 |
| https://discordpy.readthedocs.io/en/stable/api.html | API reference | 2026-09-10 |
| https://discordpy.readthedocs.io/en/stable/interactions/api.html | Interactions API | 2026-09-10 |
| https://pypi.org/project/discord.py/ | PyPI | 2026-09-10 |
| https://raw.githubusercontent.com/Rapptz/discord.py/master/pyproject.toml | pyproject.toml | 2026-09-10 |

## Changelog Review Checklist

When Discord or the frameworks release updates, review:

- [ ] Discord API version changes (currently v10)
- [ ] Privileged intent threshold changes
- [ ] Rate limit value changes
- [ ] Command name regex changes
- [ ] discord.js major version releases
- [ ] discord.py major version releases
- [ ] New permissions or events
- [ ] Deprecated events or methods
- [ ] Security requirement changes
- [ ] Gateway version changes

## Drift Hazards

**High-risk (check monthly):**
- Privileged intent thresholds
- Rate limit values
- Sharding requirements
- discord.js main branch vs tagged release

**Medium-risk (check quarterly):**
- Command name regex
- OAuth2 scopes
- Permission bit values

**Low-risk (check semi-annually):**
- Endpoint URLs
- Authentication methods
- General workflow patterns

**Known Contradictions:**
1. discord.js 14.27.0 package.json says Node >=18; docs/main say Node >=22.12.0
2. Discord's privileged-intent thresholds conflict across doc pages
3. discord.py's GitHub releases are informal; PyPI is authoritative
