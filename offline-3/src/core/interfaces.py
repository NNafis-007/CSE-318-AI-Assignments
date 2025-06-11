from abc import ABC, abstractmethod
import pygame
from typing import Any

class EventHandler(ABC):
    """Abstract base class for handling events"""
    
    @abstractmethod
    def handle_mouse_click(self, pos: tuple[int, int]) -> None:
        """Handle mouse click events"""
        pass
    
    @abstractmethod
    def handle_key_press(self, key: int) -> Any:
        """Handle key press events"""
        pass
