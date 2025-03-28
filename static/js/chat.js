document.addEventListener('DOMContentLoaded', function() {
    const messageForm = document.getElementById('message-form');
    const chatMessages = document.getElementById('chat-messages');
    const sendButton = document.getElementById('send-button');
    const sendSpinner = document.getElementById('send-spinner');
    const chatTitle = document.getElementById('chat-title');
    
    // Function to scroll to the bottom of the chat
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Scroll to the bottom on page load
    scrollToBottom();
    
    // Handle message form submission
    if (messageForm) {
        messageForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(messageForm);
            const messageInput = messageForm.querySelector('textarea');
            const message = messageInput.value.trim();
            
            if (!message) {
                return;
            }
            
            // Disable form submission and show spinner
            messageInput.disabled = true;
            sendButton.querySelector('span:first-child').classList.add('d-none');
            sendSpinner.classList.remove('d-none');
            
            // Send message using fetch API
            fetch(messageForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Add user message to the chat
                const userMessageHTML = `
                    <div class="message user-message">
                        <div class="message-content">
                            <div class="message-text">${data.user_message.content}</div>
                            <div class="message-time">${data.user_message.timestamp}</div>
                        </div>
                    </div>
                `;
                chatMessages.insertAdjacentHTML('beforeend', userMessageHTML);
                
                // Add bot message to the chat
                const botMessageHTML = `
                    <div class="message bot-message">
                        <div class="message-content">
                            <div class="message-text">${data.bot_message.content}</div>
                            <div class="message-time">${data.bot_message.timestamp}</div>
                        </div>
                    </div>
                `;
                chatMessages.insertAdjacentHTML('beforeend', botMessageHTML);
                
                // Update chat title if it was generated
                if (data.chat_title && chatTitle) {
                    chatTitle.textContent = data.chat_title;
                    document.title = data.chat_title;
                }
                
                // Scroll to the bottom of the chat
                scrollToBottom();
                
                // Clear the input and enable form submission
                messageInput.value = '';
                messageInput.focus();
                
                // Reset button state
                sendButton.querySelector('span:first-child').classList.remove('d-none');
                sendSpinner.classList.add('d-none');
                messageInput.disabled = false;
            })
            .catch(error => {
                console.error('Error:', error);
                
                // Reset button state
                sendButton.querySelector('span:first-child').classList.remove('d-none');
                sendSpinner.classList.add('d-none');
                messageInput.disabled = false;
                
                // Show error message
                const errorHTML = `
                    <div class="alert alert-danger">
                        An error occurred while sending your message. Please try again.
                    </div>
                `;
                chatMessages.insertAdjacentHTML('beforeend', errorHTML);
                scrollToBottom();
            });
        });
    }
    
    // Enable textarea resizing with a maximum height
    const textarea = messageForm.querySelector('textarea');
    if (textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            const maxHeight = 150; // Maximum height in pixels
            this.style.height = Math.min(this.scrollHeight, maxHeight) + 'px';
        });
        
        // Allow sending message with Enter key (Shift+Enter for new line)
        textarea.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendButton.click();
            }
        });
    }
    
    // Highlight code blocks for better readability
    function highlightCodeBlocks() {
        document.querySelectorAll('.message-text pre code').forEach(block => {
            // If using a syntax highlighting library like Prism.js or highlight.js,
            // you would call their highlighting functions here
            block.classList.add('highlighted');
        });
    }
    
    // Call initially and after new messages are added
    highlightCodeBlocks();
});
