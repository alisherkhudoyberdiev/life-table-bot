from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import logging
from typing import Optional, List, Dict, Any

from .models import User, CommandUsage, BotData
from .database import DatabaseSession

logger = logging.getLogger(__name__)

class UserRepository:
    """Repository for user-related database operations."""
    
    @staticmethod
    def get_or_create_user(telegram_id: int, **kwargs) -> Optional[User]:
        """Get existing user or create new one."""
        try:
            with DatabaseSession() as session:
                user = session.query(User).filter(User.telegram_id == telegram_id).first()
                
                if not user:
                    # Create new user
                    user = User(
                        telegram_id=telegram_id,
                        username=kwargs.get('username'),
                        first_name=kwargs.get('first_name'),
                        last_name=kwargs.get('last_name'),
                        language=kwargs.get('language', 'uz'),
                        join_date=datetime.utcnow()
                    )
                    session.add(user)
                    session.commit()
                    logger.info(f"Created new user with telegram_id: {telegram_id}")
                else:
                    # Update existing user info
                    if kwargs.get('username') and user.username != kwargs['username']:
                        user.username = kwargs['username']
                    if kwargs.get('first_name') and user.first_name != kwargs['first_name']:
                        user.first_name = kwargs['first_name']
                    if kwargs.get('last_name') and user.last_name != kwargs['last_name']:
                        user.last_name = kwargs['last_name']
                    user.updated_at = datetime.utcnow()
                    session.commit()
                
                return user
        except SQLAlchemyError as e:
            logger.error(f"Error in get_or_create_user: {e}")
            return None
    
    @staticmethod
    def update_user_language(telegram_id: int, language: str) -> bool:
        """Update user's language preference."""
        try:
            with DatabaseSession() as session:
                user = session.query(User).filter(User.telegram_id == telegram_id).first()
                if user:
                    user.language = language
                    user.updated_at = datetime.utcnow()
                    session.commit()
                    return True
                return False
        except SQLAlchemyError as e:
            logger.error(f"Error updating user language: {e}")
            return False
    
    @staticmethod
    def set_user_birthday(telegram_id: int, birthday: datetime) -> bool:
        """Set user's birthday."""
        try:
            with DatabaseSession() as session:
                user = session.query(User).filter(User.telegram_id == telegram_id).first()
                if user:
                    user.birthday = birthday
                    user.updated_at = datetime.utcnow()
                    session.commit()
                    return True
                return False
        except SQLAlchemyError as e:
            logger.error(f"Error setting user birthday: {e}")
            return False
    
    @staticmethod
    def get_user(telegram_id: int) -> Optional[Dict[str, Any]]:
        """Get user by telegram_id as a dictionary."""
        try:
            with DatabaseSession() as session:
                user = session.query(User).filter(User.telegram_id == telegram_id).first()
                if user:
                    # Detach the user from the session and return a dictionary
                    # to prevent DetachedInstanceError in other parts of the app.
                    session.expunge(user)
                    return {
                        'telegram_id': user.telegram_id,
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'language': user.language,
                        'birthday': user.birthday,
                        'join_date': user.join_date,
                        'is_active': user.is_active,
                        'created_at': user.created_at,
                        'updated_at': user.updated_at,
                    }
                return None
        except SQLAlchemyError as e:
            logger.error(f"Error getting user: {e}")
            return None
    
    @staticmethod
    def get_all_users() -> List[Dict[str, Any]]:
        """Get all active users as dictionaries."""
        try:
            with DatabaseSession() as session:
                users = session.query(User).filter(User.is_active == True).all()
                # Convert to dictionaries to avoid session issues
                return [
                    {
                        'telegram_id': user.telegram_id,
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'language': user.language,
                        'birthday': user.birthday,
                        'join_date': user.join_date,
                        'is_active': user.is_active,
                        'created_at': user.created_at,
                        'updated_at': user.updated_at
                    }
                    for user in users
                ]
        except SQLAlchemyError as e:
            logger.error(f"Error getting all users: {e}")
            return []
    
    @staticmethod
    def get_users_with_birthday() -> List[Dict[str, Any]]:
        """Get all active users who have set their birthday as dictionaries."""
        try:
            with DatabaseSession() as session:
                users = session.query(User).filter(
                    User.is_active == True,
                    User.birthday.isnot(None)
                ).all()
                # Convert to dictionaries to prevent DetachedInstanceError in async job
                return [
                    {
                        'telegram_id': user.telegram_id,
                        'language': user.language,
                        'birthday': str(user.birthday) if user.birthday else None
                    } 
                    for user in users
                ]
        except SQLAlchemyError as e:
            logger.error(f"Error getting users with birthday: {e}")
            return []
    
    @staticmethod
    def get_new_users_stats() -> Dict[str, int]:
        """Get statistics about new users in different time periods."""
        try:
            with DatabaseSession() as session:
                now = datetime.utcnow()
                
                # Users in last 24 hours
                users_24h = session.query(User).filter(
                    User.join_date >= now.replace(hour=0, minute=0, second=0, microsecond=0)
                ).count()
                
                # Users in last 7 days
                from datetime import timedelta
                week_ago = now - timedelta(days=7)
                users_7d = session.query(User).filter(User.join_date >= week_ago).count()
                
                # Users in last 30 days
                month_ago = now - timedelta(days=30)
                users_30d = session.query(User).filter(User.join_date >= month_ago).count()
                
                return {
                    '24h': users_24h,
                    '7d': users_7d,
                    '30d': users_30d
                }
        except SQLAlchemyError as e:
            logger.error(f"Error getting new users stats: {e}")
            return {'24h': 0, '7d': 0, '30d': 0}
    
    @staticmethod
    def deactivate_user(telegram_id: int) -> bool:
        """Marks a user as inactive."""
        try:
            with DatabaseSession() as session:
                user = session.query(User).filter(User.telegram_id == telegram_id).first()
                if user:
                    user.is_active = False
                    user.updated_at = datetime.utcnow()
                    session.commit()
                    logger.info(f"Deactivated user {telegram_id}")
                    return True
                return False
        except SQLAlchemyError as e:
            logger.error(f"Error deactivating user {telegram_id}: {e}")
            return False 