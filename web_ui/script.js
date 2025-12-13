// ==========================================
// Connection and Memory Settings
// ==========================================

// Relative URL to work both locally and on server
const API_URL = "/chat";
const RESET_URL = "/reset";

// Array to store chat history (so the model remembers context)
let chatHistory = [];

// Define page elements
const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

// ==========================================
// Core Functions
// ==========================================

/**
 * Function to send message and handle API interaction
 */
async function sendMessage() {
    const question = userInput.value.trim();
    
    // If no text, do nothing
    if (!question) return;

    // 1. Display user message in chat immediately
    appendMessage(question, 'user');
    userInput.value = ''; // Clear input
    sendBtn.disabled = true; // Disable button to prevent double sending

    // 2. Display "typing..." indicator
    const loadingId = appendLoading();

    try {
        // 3. Prepare payload (question + old history)
        const payload = {
            question: question,
            chat_history: chatHistory
        };

        // 4. Connect to server
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`Server Error: ${response.status}`);
        }

        const data = await response.json();

        // 5. Remove loading indicator and show AI response
        removeLoading(loadingId);
        appendMessage(data.answer, 'bot', data.sources);

        // 6. Update memory (for next question)
        // Add question and answer to the list
        chatHistory.push(["human", question]);
        chatHistory.push(["ai", data.answer]);

    } catch (error) {
        console.error("Error:", error);
        removeLoading(loadingId);
        appendMessage("Sorry, an error occurred connecting to the server. Please ensure the backend is running. 😔", 'bot');
    } finally {
        // Re-enable button and focus input
        sendBtn.disabled = false;
        userInput.focus();
    }
}

/**
 * Function to start a new chat (Reset)
 */
async function startNewChat() {
    // 1. Reset browser memory
    chatHistory = [];
    
    // 2. Clear screen (return to initial state)
    chatBox.innerHTML = `
        <div class="message bot-message">
            <div class="msg-content">
                Welcome back! 👋<br>Memory cleared, you can start a new topic.
            </div>
        </div>
    `;

    // 3. Notify server to clear memory (optional, for double confirmation)
    try {
        await fetch(RESET_URL, { method: 'POST' });
        console.log("Backend history reset.");
    } catch (e) {
        console.warn("Backend reset failed (might be stateless):", e);
    }
}

// ==========================================
// UI Helpers
// ==========================================

/**
 * Add message to screen
 * @param {string} text - Message text
 * @param {string} sender - Sender ('user' or 'bot')
 * @param {Array} sources - List of sources (optional)
 */
function appendMessage(text, sender, sources = []) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');

    // Convert newlines to <br> for proper formatting
    // Could use a library like 'marked' for full Markdown, but this is simpler
    let formattedText = text.replace(/\n/g, '<br>');
    
    // Convert text between ** ** to bold tags (simple implementation)
    formattedText = formattedText.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    let html = `<div class="msg-content">${formattedText}</div>`;

    /* 
    // If there are sources, add them in a small box below - DISABLED BY REQUEST
    if (sources && sources.length > 0) {
        // Remove duplicates from filenames
        const uniqueSources = [...new Set(sources)]; 
        html += `<div class="sources-box">📚 Sources: ${uniqueSources.join(', ')}</div>`;
    }
    */

    msgDiv.innerHTML = html;
    chatBox.appendChild(msgDiv);
    scrollToBottom();
}

/**
 * Add loading indicator (3 moving dots)
 */
function appendLoading() {
    const id = 'loading-' + Date.now();
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', 'bot-message');
    msgDiv.id = id;
    msgDiv.innerHTML = `
        <div class="msg-content">
            <div class="typing-indicator">
                <span></span><span></span><span></span>
            </div>
        </div>`;
    chatBox.appendChild(msgDiv);
    scrollToBottom();
    return id;
}

/**
 * Remove loading indicator
 */
function removeLoading(id) {
    const element = document.getElementById(id);
    if (element) element.remove();
}

/**
 * Scroll to bottom of chat automatically
 */
function scrollToBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
}

// ==========================================
// Event Listeners
// ==========================================

// When send button is clicked
sendBtn.addEventListener('click', sendMessage);

// When Enter is pressed in input box
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Focus on input box when page loads
window.onload = () => userInput.focus();