from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_required
from app import db
from models.chat import Chat, Message
from chat.forms import ChatMessageForm, ChatTitleForm
from chat.langchain_utils import ChatbotService
from chat import chat

# Initialize chatbot service
chatbot_service = ChatbotService()

@chat.route('/new', methods=['GET'])
@login_required
def new_chat():
    """Create a new chat and redirect to it."""
    new_chat = Chat(user_id=current_user.id)
    db.session.add(new_chat)
    db.session.commit()
    
    return redirect(url_for('chat.chat_view', chat_id=new_chat.id))

@chat.route('/<int:chat_id>', methods=['GET'])
@login_required
def chat_view(chat_id):
    """Display the chat interface for a specific chat."""
    chat_obj = Chat.query.get_or_404(chat_id)
    
    # Ensure the chat belongs to the current user
    if chat_obj.user_id != current_user.id:
        flash('Access denied: This chat does not belong to you.', 'danger')
        return redirect(url_for('dashboard.index'))
    
    messages = Message.query.filter_by(chat_id=chat_id).order_by(Message.created_at).all()
    message_form = ChatMessageForm()
    title_form = ChatTitleForm()
    title_form.title.data = chat_obj.title
    
    return render_template(
        'chat/chat.html',
        chat=chat_obj,
        messages=messages,
        message_form=message_form,
        title_form=title_form
    )

@chat.route('/<int:chat_id>/send', methods=['POST'])
@login_required
def send_message(chat_id):
    """Process and respond to a user message."""
    chat_obj = Chat.query.get_or_404(chat_id)
    
    # Ensure the chat belongs to the current user
    if chat_obj.user_id != current_user.id:
        return jsonify({'error': 'Access denied'}), 403
    
    form = ChatMessageForm()
    if form.validate_on_submit():
        user_message_content = form.message.data
        
        # Save user message to database
        user_message = Message(
            content=user_message_content,
            is_user=True,
            chat_id=chat_id
        )
        db.session.add(user_message)
        
        # Generate and save bot response
        chat_history = Message.query.filter_by(chat_id=chat_id).order_by(Message.created_at).all()
        bot_response = chatbot_service.generate_response(user_message_content, chat_history)
        
        bot_message = Message(
            content=bot_response,
            is_user=False,
            chat_id=chat_id
        )
        db.session.add(bot_message)
        
        # If this is the first message, generate a title for the chat
        if len(chat_history) == 0:
            chat_obj.title = chatbot_service.generate_chat_title(user_message_content)
        
        # Update the chat's last modified timestamp
        chat_obj.updated_at = db.func.current_timestamp()
        
        db.session.commit()
        
        return jsonify({
            'user_message': {
                'content': user_message.content,
                'timestamp': user_message.created_at.strftime('%Y-%m-%d %H:%M:%S')
            },
            'bot_message': {
                'content': bot_message.content,
                'timestamp': bot_message.created_at.strftime('%Y-%m-%d %H:%M:%S')
            },
            'chat_title': chat_obj.title
        })
    
    return jsonify({'error': 'Invalid form data'}), 400

@chat.route('/<int:chat_id>/update-title', methods=['POST'])
@login_required
def update_title(chat_id):
    """Update the title of a chat."""
    chat_obj = Chat.query.get_or_404(chat_id)
    
    # Ensure the chat belongs to the current user
    if chat_obj.user_id != current_user.id:
        flash('Access denied: This chat does not belong to you.', 'danger')
        return redirect(url_for('dashboard.index'))
    
    form = ChatTitleForm()
    if form.validate_on_submit():
        chat_obj.title = form.title.data
        db.session.commit()
        flash('Chat title updated successfully!', 'success')
    
    return redirect(url_for('chat.chat_view', chat_id=chat_id))

@chat.route('/<int:chat_id>/delete', methods=['POST'])
@login_required
def delete_chat(chat_id):
    """Delete a chat and all its messages."""
    chat_obj = Chat.query.get_or_404(chat_id)
    
    # Ensure the chat belongs to the current user
    if chat_obj.user_id != current_user.id:
        flash('Access denied: This chat does not belong to you.', 'danger')
        return redirect(url_for('dashboard.index'))
    
    db.session.delete(chat_obj)
    db.session.commit()
    flash('Chat deleted successfully!', 'success')
    
    return redirect(url_for('dashboard.index'))
