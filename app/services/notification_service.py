from typing import List
from datetime import datetime
from ..database.mongodb import mongodb
from bson import ObjectId

class NotificationService:
    @staticmethod
    async def create_notification(user_id: str, message: str):
        """Create a new notification for a user"""
        notification = {
            "message": message,
            "date": datetime.utcnow(),
            "read": False
        }
        
        db = await mongodb.get_db()
        await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$push": {"notifications": notification}}
        )
        return notification

    @staticmethod
    async def mark_notification_as_read(user_id: str, notification_date: datetime):
        """Mark a notification as read"""
        db = await mongodb.get_db()
        await db.users.update_one(
            {
                "_id": ObjectId(user_id),
                "notifications.date": notification_date
            },
            {"$set": {"notifications.$.read": True}}
        )

    @staticmethod
    async def get_user_notifications(user_id: str, unread_only: bool = False) -> List:
        """Get user notifications"""
        db = await mongodb.get_db()
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            return []
        
        notifications = user.get("notifications", [])
        if unread_only:
            notifications = [n for n in notifications if not n["read"]]
        
        return sorted(notifications, key=lambda x: x["date"], reverse=True)

    @staticmethod
    async def notify_favorite_team_game(user_id: str, team_id: str, game_data: dict):
        """Notify user about their favorite team's upcoming game"""
        message = f"Upcoming game: {game_data['team1_name']} vs {game_data['team2_name']} on {game_data['date']}"
        await NotificationService.create_notification(user_id, message)

notification_service = NotificationService() 