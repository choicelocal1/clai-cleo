document.addEventListener('DOMContentLoaded', function() {
    // Delete chat modal functionality
    const deleteChatModal = document.getElementById('deleteChatModal');
    
    if (deleteChatModal) {
        deleteChatModal.addEventListener('show.bs.modal', function(event) {
            // Button that triggered the modal
            const button = event.relatedTarget;
            
            // Extract chat info from data attributes
            const chatId = button.getAttribute('data-chat-id');
            const chatTitle = button.getAttribute('data-chat-title');
            
            // Update the modal's content
            const deleteChatTitle = document.getElementById('deleteChatTitle');
            const deleteChatForm = document.getElementById('deleteChatForm');
            
            if (deleteChatTitle) {
                deleteChatTitle.textContent = chatTitle;
            }
            
            if (deleteChatForm) {
                deleteChatForm.action = `/chat/${chatId}/delete`;
            }
        });
    }
    
    // Function to animate stat counters
    function animateStats() {
        const statValues = document.querySelectorAll('.stats-value');
        
        statValues.forEach(statValue => {
            const finalValue = parseFloat(statValue.textContent);
            let startValue = 0;
            
            // Skip animation for zero values
            if (finalValue === 0) {
                return;
            }
            
            const duration = 1000; // Animation duration in milliseconds
            const frameDuration = 1000 / 60; // 60 fps
            const totalFrames = Math.round(duration / frameDuration);
            let frame = 0;
            
            // Save the final text for later
            const finalText = statValue.textContent;
            
            // Start the animation
            const counter = setInterval(() => {
                frame++;
                
                // Calculate the progress (0 to 1)
                const progress = frame / totalFrames;
                
                // Calculate the current value
                let currentValue = finalValue * progress;
                
                // Format the value appropriately (handle decimals)
                let formattedValue;
                if (finalValue % 1 === 0) {
                    // Integer
                    formattedValue = Math.floor(currentValue).toString();
                } else {
                    // Decimal number (keep 1 decimal place during animation)
                    formattedValue = currentValue.toFixed(1);
                }
                
                // Update the display
                statValue.textContent = formattedValue;
                
                // Stop the animation when complete
                if (frame === totalFrames) {
                    clearInterval(counter);
                    // Make sure we end with the exact final value
                    statValue.textContent = finalText;
                }
            }, frameDuration);
        });
    }
    
    // Run the animation when the page loads
    animateStats();
    
    // Add a slight delay between card appearances
    function animateCardEntrance() {
        const chatCards = document.querySelectorAll('.chat-card');
        
        chatCards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            
            // Apply staggered delay
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 100 * index);
        });
    }
    
    // Run the card entrance animation
    animateCardEntrance();
});
