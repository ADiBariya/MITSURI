#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import asyncio
from typing import Optional, List, Dict, Any, Union, Callable
import time
from pyrogram import Client, filters, types
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from pyrogram.errors import FloodWait, UserIsBlocked, ChatWriteForbidden

from ..config import Config

logger = logging.getLogger("Mitsuri.core.bot")

class MitsuriBot(Client):
    """
    Extended Pyrogram Client for Mitsuri Bot
    with additional functionality
    """
    
    def __init__(self, api_id, api_hash, bot_token, mongodb, context):
        """Initialize the bot with API credentials and MongoDB"""
        self.mongodb = mongodb
        self.ctx = context
        self.command_cooldowns = {}
        self.message_queue = asyncio.Queue()
        self.is_message_handler_running = False
        
        # Initialize pyrogram client
        super().__init__(
            name="MitsuriBot",
            api_id=api_id,
            api_hash=api_hash,
            bot_token=bot_token,
            workers=16,
            plugins={"root": "Mitsuri.plugins"},
            parse_mode="html"
        )
        
        # Register middleware
        self.middleware = []
        
        # Add built-in middlewares
        from ..middleware.throttler import ThrottleMiddleware
        from ..middleware.blacklist import BlacklistMiddleware
        from ..middleware.logger import LoggerMiddleware
        
        self.add_middleware(ThrottleMiddleware())
        self.add_middleware(BlacklistMiddleware())
        self.add_middleware(LoggerMiddleware())
    
    async def start(self):
        """Start the bot and message handler"""
        await super().start()
        self.me = await self.get_me()
        logger.info(f"Bot started as @{self.me.username}")
        
        # Start the message queue handler
        self.loop = asyncio.get_event_loop()
        self.is_message_handler_running = True
        self.loop.create_task(self._process_message_queue())
        
        return self
    
    async def stop(self, *args):
        """Stop the bot and message handler"""
        self.is_message_handler_running = False
        await super().stop(*args)
    
    def add_middleware(self, middleware) -> None:
        """Add a middleware handler"""
        self.middleware.append(middleware)
    
    async def execute_middleware(self, update) -> bool:
        """Execute all middleware handlers for an update"""
        for handler in self.middleware:
            try:
                result = await handler.handle(update, self)
                if not result:
                    # If middleware returns False, stop processing
                    return False
            except Exception as e:
                logger.error(f"Error in middleware {handler.__class__.__name__}: {str(e)}")
        return True
    
    async def send_modular_message(
        self,
        chat_id: Union[int, str],
        text: str,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        reply_to_message_id: Optional[int] = None,
        **kwargs
    ) -> Optional[types.Message]:
        """
        Queue a message to be sent to avoid flood waits
        """
        payload = {
            "chat_id": chat_id,
            "text": text,
            "reply_markup": reply_markup,
            "reply_to_message_id": reply_to_message_id,
            **kwargs
        }
        
        # Put in queue for later processing
        await self.message_queue.put(payload)
        
        # Start the queue processor if not running
        if not self.is_message_handler_running:
            self.is_message_handler_running = True
            self.loop.create_task(self._process_message_queue())
    
    async def _process_message_queue(self):
        """Process messages from the queue with rate limiting"""
        while self.is_message_handler_running:
            try:
                if self.message_queue.empty():
                    await asyncio.sleep(0.1)
                    continue
                
                payload = await self.message_queue.get()
                await self._send_with_retry(payload)
                
                # Brief pause to avoid flood waits
                await asyncio.sleep(0.05)
            
            except Exception as e:
                logger.error(f"Error in message queue processor: {str(e)}")
                await asyncio.sleep(1)  # Wait a bit on error
    
    async def _send_with_retry(self, payload, max_retries=3):
        """Send a message with retry logic for FloodWait"""
        chat_id = payload.pop("chat_id")
        text = payload.pop("text")
        
        for attempt in range(max_retries):
            try:
                return await self.send_message(
                    chat_id=chat_id,
                    text=text,
                    **payload
                )
            
            except FloodWait as e:
                if attempt == max_retries - 1:
                    logger.warning(f"Max retries reached for message to {chat_id}")
                    return None
                
                wait_time = min(e.value, 10)  # Cap wait time at 10 seconds
                logger.info(f"FloodWait detected, waiting for {wait_time}s")
                await asyncio.sleep(wait_time)
            
            except UserIsBlocked:
                logger.info(f"User {chat_id} has blocked the bot")
                return None
            
            except ChatWriteForbidden:
                logger.info(f"Bot doesn't have permission to write in chat {chat_id}")
                return None
            
            except Exception as e:
                logger.error(f"Error sending message to {chat_id}: {str(e)}")
                if attempt == max_retries - 1:
                    return None
                await asyncio.sleep(1)
    
    async def broadcast(
        self, 
        user_ids: List[int], 
        message: str, 
        parse_mode="html", 
        disable_web_page_preview=True
    ) -> Dict[str, int]:
        """
        Broadcast a message to multiple users
        Returns stats about the broadcast
        """
        results = {"success": 0, "failed": 0}
        
        for user_id in user_ids:
            try:
                await self.send_modular_message(
                    chat_id=user_id,
                    text=message,
                    parse_mode=parse_mode,
                    disable_web_page_preview=disable_web_page_preview
                )
                results["success"] += 1
                
                # Short delay to avoid hitting limits
                await asyncio.sleep(0.1)
                
            except Exception as e:
                results["failed"] += 1
                logger.error(f"Failed to send broadcast to {user_id}: {str(e)}")
        
        return results
    
    async def set_bot_commands(self, commands_list: List[tuple]) -> bool:
        """
        Set bot commands list
        commands_list: List of (command, description) tuples
        """
        try:
            commands = [
                BotCommand(command, description)
                for command, description in commands_list
            ]
            
            await self.set_bot_commands(commands)
            return True
        
        except Exception as e:
            logger.error(f"Failed to set bot commands: {str(e)}")
            return False
    
    async def on_command_cooldown(self, user_id: int, command: str) -> bool:
        """
        Check if a user's command is on cooldown
        Returns True if command is on cooldown, False otherwise
        """
        cooldown_key = f"{user_id}:{command}"
        current_time = time.time()
        
        if cooldown_key in self.command_cooldowns:
            last_used = self.command_cooldowns[cooldown_key]
            if current_time - last_used < Config.RATE_LIMIT_WINDOW:
                return True
        
        # Update the cooldown timestamp
        self.command_cooldowns[cooldown_key] = current_time
        return False
    
    def get_uptime(self) -> str:
        """Get formatted bot uptime"""
        return self.ctx.uptime
