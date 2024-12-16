document.getElementById('send-button').addEventListener('click', async () => {
    sendMessage();
});

// Allow "Enter" to send the message
document.getElementById('user-input').addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        event.preventDefault();  // Prevent the default 'Enter' behavior (e.g., new line in textarea)
        sendMessage();
    }
});

async function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (!userInput) return alert('Message cannot be empty.');

    // Append user's message to chat
    const chatMessages = document.getElementById('chat-messages');
    const userMessage = document.createElement('div');
    userMessage.textContent = userInput;
    userMessage.classList.add('message', 'user-message');
    chatMessages.appendChild(userMessage);

    // Clear the input field
    document.getElementById('user-input').value = '';

    // Display loading message while waiting for API response
    const loadingMessage = document.createElement('div');
    loadingMessage.textContent = "Assistant is typing...";
    loadingMessage.classList.add('message', 'assistant-message');
    chatMessages.appendChild(loadingMessage);
    
    // Scroll to show latest message
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Call GROK API
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userInput }),
        });
        
        const data = await response.json();
        const assistantMessageText = `Assistant: ${data.reply}`;

        // Format the response
        let formattedMessage = assistantMessageText.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');  // Bold text
        formattedMessage = formattedMessage.replace(/^(\d+\.)/gm, '<br>$1');  // Add line break for numbered points

        // Remove the loading message
        chatMessages.removeChild(loadingMessage);

        // Create a new div to hold the assistant's formatted message
        const assistantMessage = document.createElement('div');
        assistantMessage.innerHTML = formattedMessage;  // Use innerHTML to insert formatted text
        assistantMessage.classList.add('message', 'assistant-message');
        
        chatMessages.appendChild(assistantMessage);
        
        // Scroll to the bottom of the chat to show the latest messages
        chatMessages.scrollTop = chatMessages.scrollHeight;
    } catch (error) {
        alert('Error communicating with GROK API.');
        // Remove the loading message if there's an error
        chatMessages.removeChild(loadingMessage);
    }
}
