function chatBot(){
    const inputField = document.getElementById('user-input');
            const userInput = inputField.value.trim();
            if (!userInput) return; // Skip empty input

            // Append user message to chat
            const messagesContainer = document.querySelector('.chatbot-messages');
            const userMessage = document.createElement('div');
            userMessage.className = 'user-message';
            userMessage.textContent = userInput;
            messagesContainer.appendChild(userMessage);

            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            inputField.value = '';

    fetch('/generate-response', { method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'user_input': userInput})})

    .then(response => response.json())
    .then(data => {
        const aiMessage = document.createElement('div');
                aiMessage.className = 'message';
                aiMessage.textContent = data.ai_response || 'No response';
                messagesContainer.appendChild(aiMessage);
    })
    console.log(userInput)
}

// To handle hiitting enter instead of just clicking.

document.addEventListener('DOMContentLoaded', () => {
    const inputField = document.getElementById('user-input');
    inputField.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            console.log('Enter key pressed, calling chatBot()');
            chatBot();
        }
    });
});
