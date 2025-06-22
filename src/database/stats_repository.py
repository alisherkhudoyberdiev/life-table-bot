import json
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import logging
from typing import Dict, List, Optional, Any

from .models import CommandUsage, BotData
from .database import DatabaseSession

logger = logging.getLogger(__name__)

class StatsRepository:
    """Repository for statistics and bot data operations."""
    
    def track_command_usage(self, command: str, user_id: Optional[int] = None):
        """Track command usage in the database."""
        try:
            with DatabaseSession() as session:
                usage = session.query(CommandUsage).filter_by(command_name=command).first()
                if usage:
                    usage.usage_count += 1
                    usage.last_used = datetime.utcnow()
                    if user_id:
                        usage.user_id = user_id
                else:
                    usage = CommandUsage(
                        command_name=command,
                        user_id=user_id
                    )
                    session.add(usage)
                session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Error tracking command usage for '{command}': {e}")
            
    def get_command_usage_stats(self) -> Dict[str, int]:
        """Get command usage statistics."""
        try:
            with DatabaseSession() as session:
                results = session.query(
                    CommandUsage.command_name,
                    CommandUsage.usage_count
                ).all()
                return {command: count for command, count in results}
        except SQLAlchemyError as e:
            logger.error(f"Error getting command usage stats: {e}")
            return {}
    
    @staticmethod
    def get_top_commands(limit: int = 10) -> List[tuple]:
        """Get top used commands."""
        try:
            with DatabaseSession() as session:
                results = session.query(
                    CommandUsage.command_name,
                    CommandUsage.usage_count
                ).all()
                
                # Aggregate counts by command
                command_counts = {}
                for command, count in results:
                    if command in command_counts:
                        command_counts[command] += count
                    else:
                        command_counts[command] = count
                
                # Sort by usage count and return top N
                sorted_commands = sorted(
                    command_counts.items(),
                    key=lambda x: x[1],
                    reverse=True
                )
                
                return sorted_commands[:limit]
        except SQLAlchemyError as e:
            logger.error(f"Error getting top commands: {e}")
            return []
    
    @staticmethod
    def set_bot_data(key: str, value: Any) -> bool:
        """Set bot data in the database."""
        try:
            with DatabaseSession() as session:
                # Convert value to JSON string if it's not a string
                if not isinstance(value, str):
                    value = json.dumps(value)
                
                # Check if data already exists
                bot_data = session.query(BotData).filter(BotData.key == key).first()
                
                if bot_data:
                    # Update existing record
                    bot_data.value = value
                    bot_data.updated_at = datetime.utcnow()
                else:
                    # Create new record
                    bot_data = BotData(
                        key=key,
                        value=value
                    )
                    session.add(bot_data)
                
                session.commit()
                return True
        except SQLAlchemyError as e:
            logger.error(f"Error setting bot data: {e}")
            return False
    
    @staticmethod
    def get_bot_data(key: str) -> Optional[Any]:
        """Get bot data from the database."""
        try:
            with DatabaseSession() as session:
                bot_data = session.query(BotData).filter(BotData.key == key).first()
                
                if bot_data and bot_data.value:
                    try:
                        # Try to parse as JSON
                        return json.loads(bot_data.value)
                    except json.JSONDecodeError:
                        # Return as string if not JSON
                        return bot_data.value
                
                return None
        except SQLAlchemyError as e:
            logger.error(f"Error getting bot data: {e}")
            return None
    
    @staticmethod
    def delete_bot_data(key: str) -> bool:
        """Delete bot data from the database."""
        try:
            with DatabaseSession() as session:
                bot_data = session.query(BotData).filter(BotData.key == key).first()
                if bot_data:
                    session.delete(bot_data)
                    session.commit()
                    return True
                return False
        except SQLAlchemyError as e:
            logger.error(f"Error deleting bot data: {e}")
            return False 