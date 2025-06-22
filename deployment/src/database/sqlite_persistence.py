import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from telegram.ext import BasePersistence
from telegram import Bot

from .database import init_database, DatabaseSession
from .user_repository import UserRepository
from .stats_repository import StatsRepository
from .models import User

logger = logging.getLogger(__name__)

class SQLitePersistence(BasePersistence):
    """Custom SQLite persistence for telegram bot."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize database
        init_database()
        self.user_repo = UserRepository()
        self.stats_repo = StatsRepository()
    
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
    
    async def get_bot_data(self) -> Dict[str, Any]:
        """Get bot data from database."""
        try:
            # Get command usage stats
            command_usage = self.stats_repo.get_command_usage_stats()
            
            return {
                'command_usage': command_usage
            }
        except Exception as e:
            logger.error(f"Error getting bot data: {e}")
            return {}
    
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
    
    async def update_bot_data(self, data: Dict[str, Any]) -> None:
        """Update bot data in database."""
        try:
            # Update command usage if provided
            if 'command_usage' in data:
                for command, count in data['command_usage'].items():
                    # Store each command usage separately
                    for _ in range(count):
                        self.stats_repo.track_command_usage(command)
        
        except Exception as e:
            logger.error(f"Error updating bot data: {e}")
    
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
    
    async def refresh_bot_data(self, bot_data: Dict[str, Any]) -> None:
        """Refresh bot data from database."""
        # This is called when bot data is accessed
        pass
    
    async def update_callback_data(self, callback_data: Dict[str, Any]) -> None:
        """Update callback data in database."""
        # For this bot, we don't store callback data
        pass 