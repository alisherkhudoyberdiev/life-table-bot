import json
import logging
import sqlite3
from typing import Dict, Any, Optional
from datetime import datetime
import pickle

from telegram.ext import BasePersistence
from telegram import Bot

from .database import init_database, DatabaseSession
from .user_repository import UserRepository
from .stats_repository import StatsRepository
from .models import User

logger = logging.getLogger(__name__)

class SQLitePersistence(BasePersistence):
    """Custom SQLite persistence for telegram bot."""
    
    def __init__(self, filepath: str):
        """
        Initialize SQLite persistence.
        filepath: Path to the database file.
        """
        # Call parent constructor without arguments
        super().__init__()
        self.filepath = filepath
        self.conn = None
        self.bot_data = {}
        self._connect()
        self._load_bot_data()
        # Initialize database
        init_database()
        self.user_repo = UserRepository()
        self.stats_repo = StatsRepository()
    
    def _connect(self):
        """Connect to SQLite database."""
        try:
            self.conn = sqlite3.connect(self.filepath)
            self.conn.row_factory = sqlite3.Row
            # Create bot_data table if it doesn't exist
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bot_data (
                    key TEXT PRIMARY KEY,
                    value BLOB
                )
            """)
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to connect to SQLite: {e}")
    
    def _load_bot_data(self):
        """Load bot data from database."""
        if not self.conn:
            self._connect()
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT value FROM bot_data WHERE key = ?", ("bot_data",))
            result = cursor.fetchone()
            if result:
                self.bot_data = pickle.loads(result[0])
        except Exception as e:
            logger.error(f"Failed to load bot_data from SQLite: {e}")
            self.bot_data = {}
    
    async def get_user_data(self) -> Dict[int, Any]:
        """Get all user data from database."""
        try:
            users = self.user_repo.get_all_users()
            user_data = {}
            
            for user in users:
                # user is now a dictionary
                user_data[user['telegram_id']] = {
                    'lang': user['language'],
                    'birthday': user['birthday'].isoformat() if user['birthday'] else None,
                    'join_date': user['join_date'].isoformat(),
                    'awaiting_birthday': False,  # Default state
                    'awaiting_broadcast': False  # Default state
                }
            
            return user_data
        except Exception as e:
            logger.error(f"Error getting user data: {e}")
            return {}
    
    async def get_chat_data(self) -> Dict[int, Any]:
        """Get all chat data from database."""
        # For this bot, we don't store chat-specific data
        return {}
    
    async def get_bot_data(self) -> dict:
        """Returns the bot_data from memory."""
        return self.bot_data
    
    async def get_conversations(self, name: str) -> Dict[str, Any]:
        """Get conversations from database."""
        # For this bot, we don't store conversations
        return {}
    
    async def get_callback_data(self) -> Dict[str, Any]:
        """Get callback data from database."""
        # For this bot, we don't store callback data
        return {}
    
    async def update_user_data(self, user_id: int, data: Dict[str, Any]) -> None:
        """Update user data in database."""
        try:
            user = self.user_repo.get_user(user_id)
            if not user:
                # Create user if doesn't exist
                user = self.user_repo.get_or_create_user(user_id)
            
            if user:
                # Update language if provided
                if 'lang' in data:
                    self.user_repo.update_user_language(user_id, data['lang'])
                
                # Update birthday if provided
                if 'birthday' in data and data['birthday']:
                    try:
                        birthday = data['birthday']
                        # If it's already a datetime object, use it directly
                        if isinstance(birthday, datetime):
                            self.user_repo.set_user_birthday(user_id, birthday)
                        # If it's a string, parse it
                        elif isinstance(birthday, str):
                            birthday = datetime.fromisoformat(birthday)
                            self.user_repo.set_user_birthday(user_id, birthday)
                        else:
                            logger.warning(f"Unexpected birthday type for user {user_id}: {type(birthday)}")
                    except ValueError as e:
                        logger.warning(f"Invalid birthday format for user {user_id}: {e}")
        
        except Exception as e:
            logger.error(f"Error updating user data: {e}")
    
    async def update_chat_data(self, chat_id: int, data: Dict[str, Any]) -> None:
        """Update chat data in database."""
        # For this bot, we don't store chat-specific data
        pass
    
    async def update_bot_data(self, data: dict) -> None:
        """Updates the bot_data in memory and database."""
        self.bot_data = data
        self._write_bot_data()
    
    def _write_bot_data(self):
        """Writes bot_data to the database."""
        if not self.conn:
            self._connect()
        try:
            pickled_data = pickle.dumps(self.bot_data)
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO bot_data (key, value) VALUES (?, ?)",
                ("bot_data", pickled_data)
            )
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to write bot_data to SQLite: {e}")
    
    async def update_conversation(self, name: str, key: str, new_state: Optional[object]) -> None:
        """Update conversation in database."""
        # For this bot, we don't store conversations
        pass
    
    async def drop_chat_data(self, chat_id: int) -> None:
        """Drop chat data from database."""
        # For this bot, we don't store chat-specific data
        pass
    
    async def drop_user_data(self, user_id: int) -> None:
        """Drop user data from database."""
        # For this bot, we don't delete user data, just mark as inactive
        try:
            with DatabaseSession() as session:
                user = session.query(User).filter(User.telegram_id == user_id).first()
                if user:
                    user.is_active = False
                    user.updated_at = datetime.utcnow()
                    session.commit()
        except Exception as e:
            logger.error(f"Error dropping user data: {e}")
    
    async def drop_bot_data(self) -> None:
        """Drop bot data from database."""
        # For this bot, we don't drop bot data
        pass
    
    async def drop_conversation(self, name: str, key: str) -> None:
        """Drop conversation from database."""
        # For this bot, we don't store conversations
        pass
    
    async def flush(self) -> None:
        """Flush data to database."""
        # Data is already committed in individual operations
        pass
    
    async def refresh_user_data(self, user_id: int, user_data: Dict[str, Any]) -> None:
        """Refresh user data from database."""
        # This is called when user data is accessed
        pass
    
    async def refresh_chat_data(self, chat_id: int, chat_data: Dict[str, Any]) -> None:
        """Refresh chat data from database."""
        # For this bot, we don't store chat-specific data
        pass
    
    async def refresh_bot_data(self, bot_data: dict) -> None:
        """No-op for this persistence class."""
        pass
    
    async def update_callback_data(self, callback_data: Dict[str, Any]) -> None:
        """Update callback data in database."""
        # For this bot, we don't store callback data
        pass 