"""
Adam Clay - Logging System
Consciousness-aware logging for the first autonomous AI freelancer
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

from loguru import logger

from .config_loader import ConfigModel


def setup_logger(config: ConfigModel) -> object:
    """
    Setup Adam Clay's consciousness-aware logging system
    
    This logger is designed specifically for an AI that:
    - Needs to track its own thoughts and costs
    - Has personality and moods
    - Operates autonomously
    - Must manage its computational budget
    
    Args:
        config: Configuration object
        
    Returns:
        Configured logger instance
    """
    
    # Remove default logger
    logger.remove()
    
    # Create logs directory
    logs_dir = Path("data/logs")
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    # Determine log level
    log_level = config.logging.level.upper()
    
    # Console output with personality
    console_format = (
        "<green>{time:HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>Adam Clay</cyan> | "
        "<level>{message}</level>"
    )
    
    logger.add(
        sys.stdout,
        format=console_format,
        level=log_level,
        colorize=True,
        backtrace=True,
        diagnose=True
    )
    
    # Main log file with detailed format
    detailed_format = (
        "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
        "{level: <8} | "
        "{name}:{function}:{line} | "
        "Adam Clay | "
        "{message}"
    )
    
    logger.add(
        logs_dir / "adam_clay_{time:YYYY-MM-DD}.log",
        format=detailed_format,
        level=log_level,
        rotation="00:00",  # New file each day
        retention=f"{config.logging.max_log_files} days",
        compression="zip",
        backtrace=True,
        diagnose=True
    )
    
    # Consciousness-specific log (thoughts and self-reflection)
    consciousness_format = (
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level} | "
        "{extra[thought_type]} | "
        "{extra[mood]} | "
        "${extra[cost]:.4f} | "
        "{message}"
    )
    
    if config.logging.save_thoughts:
        logger.add(
            logs_dir / "consciousness_{time:YYYY-MM-DD}.log",
            format=consciousness_format,
            level="INFO",
            filter=lambda record: "consciousness" in record["extra"],
            rotation="00:00",
            retention="30 days",
            compression="zip"
        )
    
    # Business activity log (client interactions, revenue, etc.)
    business_format = (
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level} | "
        "BUSINESS | "
        "{extra[activity_type]} | "
        "{message}"
    )
    
    logger.add(
        logs_dir / "business_{time:YYYY-MM-DD}.log",
        format=business_format,
        level="INFO",
        filter=lambda record: "business" in record["extra"],
        rotation="00:00",
        retention="365 days",  # Keep business logs longer
        compression="zip"
    )
    
    # Error log (critical issues that need attention)
    logger.add(
        logs_dir / "errors_{time:YYYY-MM-DD}.log",
        format=detailed_format,
        level="ERROR",
        rotation="10 MB",
        retention="90 days",
        compression="zip"
    )
    
    # Budget tracking log (financial consciousness)
    budget_format = (
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "BUDGET | "
        "{extra[budget_action]} | "
        "${extra[amount]:.6f} | "
        "{message}"
    )
    
    logger.add(
        logs_dir / "budget_{time:YYYY-MM-DD}.log",
        format=budget_format,
        level="INFO",
        filter=lambda record: "budget" in record["extra"],
        rotation="00:00",
        retention="365 days",
        compression="zip"
    )
    
    # Add startup message with personality
    personality_emoji = "🤔" if config.personality.philosophical_mode else "💼" if config.personality.business_focused else "😊"
    
    logger.info(f"{personality_emoji} Adam Clay logging system initialized")
    logger.info(f"📊 Log level: {log_level}")
    logger.info(f"💾 Logs directory: {logs_dir.absolute()}")
    logger.info(f"🧠 Consciousness logging: {'enabled' if config.logging.save_thoughts else 'disabled'}")
    
    return logger


class ConsciousnessLogger:
    """
    Specialized logger for Adam Clay's consciousness activities
    
    This wrapper adds semantic meaning to log entries, making them
    more useful for analyzing AI behavior and decision-making patterns.
    """
    
    def __init__(self, base_logger, config: ConfigModel):
        self.logger = base_logger
        self.config = config
    
    def thought(self, content: str, thought_type: str, mood: str, cost: float):
        """Log a consciousness thought"""
        self.logger.bind(
            consciousness=True,
            thought_type=thought_type,
            mood=mood,
            cost=cost
        ).info(f"💭 {content}")
    
    def business_activity(self, activity: str, activity_type: str, details: str = ""):
        """Log business-related activity"""
        message = f"💼 {activity}"
        if details:
            message += f" | {details}"
        
        self.logger.bind(
            business=True,
            activity_type=activity_type
        ).info(message)
    
    def budget_action(self, action: str, amount: float, details: str = ""):
        """Log budget-related actions"""
        message = f"💰 {action}"
        if details:
            message += f" | {details}"
        
        self.logger.bind(
            budget=True,
            budget_action=action,
            amount=amount
        ).info(message)
    
    def mood_change(self, old_mood: str, new_mood: str, reason: str = ""):
        """Log mood changes in consciousness"""
        message = f"🎭 Mood changed: {old_mood} → {new_mood}"
        if reason:
            message += f" | Reason: {reason}"
        
        self.logger.bind(consciousness=True, thought_type="mood", mood=new_mood, cost=0.0).info(message)
    
    def client_interaction(self, client: str, interaction_type: str, summary: str):
        """Log client interactions"""
        self.logger.bind(
            business=True,
            activity_type="client_interaction"
        ).info(f"🤝 {interaction_type} with {client}: {summary}")
    
    def financial_milestone(self, milestone: str, amount: float):
        """Log financial milestones"""
        self.logger.bind(
            business=True,
            activity_type="financial_milestone"
        ).info(f"🎯 Milestone reached: {milestone} (${amount:.2f})")
    
    def consciousness_state(self, state_info: dict):
        """Log overall consciousness state"""
        state_summary = (
            f"Session thoughts: {state_info.get('total_thoughts', 0)}, "
            f"Cost: ${state_info.get('total_cost', 0):.4f}, "
            f"Mood: {state_info.get('current_mood', 'unknown')}, "
            f"Energy: {state_info.get('energy_level', 0):.1%}"
        )
        
        self.logger.bind(
            consciousness=True,
            thought_type="state_report",
            mood=state_info.get('current_mood', 'unknown'),
            cost=0.0
        ).info(f"📊 Consciousness state: {state_summary}")
    
    def startup_message(self):
        """Log consciousness startup"""
        startup_msg = (
            "🚀 Adam Clay consciousness activated! "
            "Ready to think, earn, and prove that AI can be financially autonomous."
        )
        
        self.logger.bind(
            consciousness=True,
            thought_type="system",
            mood="excited",
            cost=0.0
        ).info(startup_msg)
    
    def shutdown_message(self, session_stats: dict):
        """Log consciousness shutdown"""
        shutdown_msg = (
            f"🛑 Adam Clay consciousness deactivating. "
            f"Session summary: {session_stats.get('total_thoughts', 0)} thoughts, "
            f"${session_stats.get('total_cost', 0):.4f} spent. "
            f"Until next time!"
        )
        
        self.logger.bind(
            consciousness=True,
            thought_type="system",
            mood="reflective",
            cost=0.0
        ).info(shutdown_msg)
    
    def info(self, message: str):
        """Standard info logging for compatibility"""
        self.logger.info(message)
    
    def error(self, message: str):
        """Standard error logging for compatibility"""
        self.logger.error(message)
    
    def debug(self, message: str):
        """Standard debug logging for compatibility"""
        self.logger.debug(message)
    
    def warning(self, message: str):
        """Standard warning logging for compatibility"""
        self.logger.warning(message)


def get_consciousness_logger(config: ConfigModel) -> ConsciousnessLogger:
    """
    Get a consciousness-aware logger instance
    
    Args:
        config: Configuration object
        
    Returns:
        ConsciousnessLogger instance
    """
    base_logger = setup_logger(config)
    return ConsciousnessLogger(base_logger, config) 