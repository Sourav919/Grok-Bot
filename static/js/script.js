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
        let assistantMessageText = `Assistant: ${data.reply}`;

        // Format the response:
        // 1. Make **text** bold by replacing it with <strong>text</strong>
        assistantMessageText = assistantMessageText.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

        // 2. Ensure numbered points start on a new line.
        assistantMessageText = assistantMessageText.replace(/^(\d+\.)/gm, '<br>$1');

        // Create a new div to hold the assistant's formatted message
        const assistantMessage = document.createElement('div');
        assistantMessage.innerHTML = assistantMessageText;  // Use innerHTML to insert formatted text
        assistantMessage.classList.add('message', 'assistant-message');
        
        chatMessages.appendChild(assistantMessage);

        // Scroll to the bottom after the assistant's message is added
        setTimeout(() => {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }, 100);
    } catch (error) {
        alert('Error communicating with GROK API.');
    }
}
