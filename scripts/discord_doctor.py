#!/usr/bin/env python3
"""discord_doctor.py — backward-compatible wrapper.

The checker implementation has moved to `src/discord_bot_development/doctor.py`.
This wrapper preserves the historical invocation path:

    python scripts/discord_doctor.py <path>

Prefer the installed CLI:

    discord-doctor <path>

or the module invocation:

    python -m discord_bot_development <path>
"""
from __future__ import annotations

import sys

from discord_bot_development.doctor import main

if __name__ == "__main__":
    sys.exit(main())
