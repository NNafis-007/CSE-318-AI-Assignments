#!/usr/bin/env python3
"""
Chain Reaction Game - Web Version
Entry point for pygbag
"""

import asyncio
import pygame

# Simple pygame initialization
pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=1024)
pygame.init()

from chain_reaction_gui import ChainReactionGUI

async def main():
    """Main entry point for the web version"""
    gui = ChainReactionGUI()
    await gui.run()

if __name__ == "__main__":
    asyncio.run(main())
