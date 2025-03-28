from flask import render_template, request
from flask_login import current_user, login_required
from app import db
from models.chat import Chat, Message
from dashboard import dashboard

@dashboard.route('/', methods=['GET'])
@login_required
def index():
    """Display the user's dashboard with chat history."""
    # Get sort parameter from query string (default to newest first)
    sort = request.args.get('sort', 'newest')
    
    # Query user's chats with sorting
    if sort == 'oldest':
        chats = Chat.query.filter_by(user_id=current_user.id).order_by(Chat.created_at.asc()).all()
    elif sort == 'title':
        chats = Chat.query.filter_by(user_id=current_user.id).order_by(Chat.title.asc()).all()
    else:  # Default to 'newest'
        chats = Chat.query.filter_by(user_id=current_user.id).order_by(Chat.updated_at.desc()).all()
    
    # Get chat statistics
    chat_count = len(chats)
    
    total_messages = 0
    chat_previews = {}
    
    for chat in chats:
        # Count messages in each chat
        messages = Message.query.filter_by(chat_id=chat.id).all()
        message_count = len(messages)
        total_messages += message_count
        
        # Get the last message for preview (if any)
        if message_count > 0:
            last_message = messages[-1]
            # Truncate message if too long
            preview = last_message.content[:50] + '...' if len(last_message.content) > 50 else last_message.content
            chat_previews[chat.id] = preview
    
    return render_template(
        'dashboard/index.html',
        chats=chats,
        chat_count=chat_count,
        total_messages=total_messages,
        chat_previews=chat_previews,
        current_sort=sort
    )
