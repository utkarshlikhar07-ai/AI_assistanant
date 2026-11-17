// JARVIS AI - Chat Interface & Assistant Controller
// Handles chat messages, speech recognition, speech synthesis, and inline algorithm visual cards

let conversationHistory = [];
let isListening = false;
let isSpeaking = false;
let synth = window.speechSynthesis || null;
let recognition = null;

// ============================================================================
// SPEECH RECOGNITION (Web Speech API)
// ============================================================================
function initSpeech() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        console.warn('SpeechRecognition API is not supported in this browser.');
        const micBtn = document.getElementById('btn-mic');
        if (micBtn) {
            micBtn.title = 'Voice recognition not supported in this browser';
            micBtn.style.opacity = '0.5';
        }
        return;
    }

    try {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = true;

        recognition.onstart = () => {
            isListening = true;
            updateMicButton(true);
            showToast('Listening... Speak now', 'info', 2000);
        };

        recognition.onresult = (e) => {
            let interimTranscript = '';
            let finalTranscript = '';
            for (let i = e.resultIndex; i < e.results.length; ++i) {
                if (e.results[i].isFinal) {
                    finalTranscript += e.results[i][0].transcript;
                } else {
                    interimTranscript += e.results[i][0].transcript;
                }
            }

            const chatInput = document.getElementById('chat-input');
            if (chatInput) {
                if (finalTranscript) {
                    chatInput.value = finalTranscript;
                    // Auto-send when final sentence is clear
                    setTimeout(() => sendMessage(), 400);
                } else if (interimTranscript) {
                    chatInput.value = interimTranscript;
                }
            }
        };

        recognition.onerror = (e) => {
            console.error('Speech recognition error:', e.error);
            isListening = false;
            updateMicButton(false);
            if (e.error !== 'no-speech') {
                showToast(`Voice error: ${e.error}`, 'warning');
            }
        };

        recognition.onend = () => {
            isListening = false;
            updateMicButton(false);
        };
    } catch (e) {
        console.warn('Failed to initialize SpeechRecognition:', e);
    }
}

function toggleMic() {
    if (!window.currentSettings?.voiceEnabled) {
        showToast('Voice input is disabled in Settings', 'warning');
        return;
    }

    if (!recognition) {
        initSpeech();
        if (!recognition) {
            showToast('Voice recognition is not supported in this browser', 'error');
            return;
        }
    }

    if (isListening) {
        recognition.stop();
        isListening = false;
        updateMicButton(false);
    } else {
        try {
            recognition.lang = window.currentSettings?.voiceLang || 'en-US';
            recognition.start();
        } catch (e) {
            console.error('Recognition start error:', e);
            recognition.stop();
            isListening = false;
            updateMicButton(false);
        }
    }
}

function updateMicButton(active) {
    const micBtn = document.getElementById('btn-mic');
    if (!micBtn) return;

    if (active) {
        micBtn.classList.add('pulse');
        micBtn.style.color = '#ef4444';
        micBtn.style.borderColor = '#ef4444';
        micBtn.style.boxShadow = '0 0 15px rgba(239, 68, 68, 0.6)';
    } else {
        micBtn.classList.remove('pulse');
        micBtn.style.color = '';
        micBtn.style.borderColor = '';
        micBtn.style.boxShadow = '';
    }
}

// ============================================================================
// SPEECH SYNTHESIS (Text-to-Speech)
// ============================================================================
function speakText(text) {
    if (!synth) return;
    if (!window.currentSettings?.ttsEnabled) return;

    // Cancel current speech
    synth.cancel();

    // Clean markdown and symbols from text
    const cleanText = text
        .replace(/[*_#`~[\]]/g, '')
        .replace(/https?:\/\/\S+/g, '')
        .replace(/[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/gu, '')
        .trim();

    if (!cleanText) return;

    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.lang = window.currentSettings?.voiceLang || 'en-US';
    utterance.rate = 1.0;
    utterance.pitch = 1.0;

    // Try to pick an English / natural sounding voice
    const voices = synth.getVoices();
    if (voices.length > 0) {
        const langPref = utterance.lang.toLowerCase();
        const preferredVoice = voices.find(v => v.lang.toLowerCase().startsWith(langPref) && (v.name.includes('Natural') || v.name.includes('Google') || v.name.includes('David') || v.name.includes('Samantha')));
        if (preferredVoice) utterance.voice = preferredVoice;
    }

    utterance.onstart = () => { isSpeaking = true; };
    utterance.onend = () => { isSpeaking = false; };
    utterance.onerror = () => { isSpeaking = false; };

    synth.speak(utterance);
}

// ============================================================================
// CHAT MESSAGES RENDERING
// ============================================================================
function formatMessageText(text) {
    if (!text) return '';

    // Sanitize basic HTML first
    let escaped = text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');

    // Code blocks ```language ... ```
    escaped = escaped.replace(/```(?:[a-zA-Z0-9_-]+)?\n?([\s\S]*?)```/g, (match, p1) => {
        return `<pre class="chat-code-block"><code>${p1.trim()}</code></pre>`;
    });

    // Inline code `code`
    escaped = escaped.replace(/`([^`\n]+)`/g, '<code class="chat-inline-code">$1</code>');

    // Headings ### and ##
    escaped = escaped.replace(/^###\s+(.+)$/gm, '<h4 class="chat-heading">$1</h4>');
    escaped = escaped.replace(/^##\s+(.+)$/gm, '<h3 class="chat-heading">$1</h3>');

    // Bold **text**
    escaped = escaped.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

    // Italic *text* (if not inside bold)
    escaped = escaped.replace(/(?<!\*)\*([^*\n]+)\*(?!\*)/g, '<em>$1</em>');

    // Numbered lists 1. item
    escaped = escaped.replace(/^\s*(\d+)\.\s+(.+)$/gm, '<li class="chat-ordered-item" value="$1">$2</li>');

    // Bullet points - item or * item
    escaped = escaped.replace(/^\s*[-•]\s+(.+)$/gm, '<li class="chat-bullet">$1</li>');

    // Wrap consecutive list items
    escaped = escaped.replace(/(<li class="chat-bullet">[\s\S]*?<\/li>(?:\s*<li class="chat-bullet">[\s\S]*?<\/li>)*)/g, '<ul class="chat-list">$1</ul>');
    escaped = escaped.replace(/(<li class="chat-ordered-item"[\s\S]*?<\/li>(?:\s*<li class="chat-ordered-item"[\s\S]*?<\/li>)*)/g, '<ol class="chat-list-ordered">$1</ol>');

    // Blockquotes > quote
    escaped = escaped.replace(/^\s*&gt;\s+(.+)$/gm, '<blockquote class="chat-quote">$1</blockquote>');

    // Line breaks (convert remaining newlines to <br> if not preceded/followed by block tags)
    escaped = escaped.replace(/\n{2,}/g, '</p><p>');
    escaped = escaped.replace(/\n/g, '<br>');

    return `<p>${escaped}</p>`;
}

function addMessage(text, sender = 'jarvis', timestamp = null, data = null, llmPowered = false) {
    const chatMessages = document.getElementById('chat-messages');
    if (!chatMessages) return;

    const timeStr = timestamp || new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const isUser = sender === 'user';

    const msgContainer = document.createElement('div');
    msgContainer.className = `message ${isUser ? 'user-message' : 'jarvis-message'} fade-in`;

    let html = '';
    if (isUser) {
        html = `
            <div class="message-bubble">
                <div class="message-text-content">${formatMessageText(text)}</div>
                <div class="message-footer">
                    <span class="message-time">${timeStr}</span>
                </div>
            </div>
            <div class="message-avatar user-avatar">U</div>
        `;
    } else {
        const badgeHtml = llmPowered
            ? '<span class="llm-badge" title="Response generated by Google Gemini LLM"><span class="gemini-sparkle">✨</span> Gemini AI</span>'
            : '<span class="offline-badge" title="Response generated by deterministic local rule engine">⚙ Rule Engine</span>';

        html = `
            <div class="message-avatar">J</div>
            <div class="message-bubble">
                <div class="message-text-content">${formatMessageText(text)}</div>
                <div class="message-footer">
                    <div class="footer-left">
                        ${badgeHtml}
                        <span class="message-time">${timeStr}</span>
                    </div>
                    <button class="msg-copy-btn" title="Copy text" onclick="copyMessageText(this)">📋</button>
                </div>
            </div>
        `;
    }

    msgContainer.innerHTML = html;

    // Insert inline data visualizer if provided
    if (data && !isUser) {
        const bubble = msgContainer.querySelector('.message-bubble');
        const dataCard = renderAlgorithmDataCard(data);
        if (dataCard && bubble) {
            bubble.insertBefore(dataCard, bubble.querySelector('.message-footer'));
        }
    }

    chatMessages.appendChild(msgContainer);
    scrollToLatestMessage();
}

function scrollToLatestMessage() {
    const chatMessages = document.getElementById('chat-messages');
    if (chatMessages) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

function copyMessageText(btn) {
    const bubble = btn.closest('.message-bubble');
    if (!bubble) return;
    const textEl = bubble.querySelector('.message-text-content') || bubble.querySelector('p');
    if (!textEl) return;

    navigator.clipboard.writeText(textEl.innerText)
        .then(() => {
            btn.textContent = '✓';
            setTimeout(() => { btn.textContent = '📋'; }, 2000);
            showToast('Copied message to clipboard', 'info', 1500);
        })
        .catch(err => {
            showToast('Failed to copy: ' + err.message, 'error');
        });
}

function showTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
        indicator.style.display = 'flex';
        scrollToLatestMessage();
    }
}

function hideTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
        indicator.style.display = 'none';
    }
}

// ============================================================================
// SEND MESSAGE & API INTEGRATION
// ============================================================================
async function sendMessage(text = null) {
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('btn-send');
    const messageText = (text !== null ? text : chatInput ? chatInput.value : '').trim();

    if (!messageText) return;

    // Render user message immediately
    addMessage(messageText, 'user');
    if (chatInput) chatInput.value = '';

    conversationHistory.push({ role: 'user', content: messageText });
    showTypingIndicator();

    if (sendBtn) sendBtn.disabled = true;

    try {
        const res = await apiCall('/assistant/chat', 'POST', {
            message: messageText,
            conversation_history: conversationHistory
        });

        hideTypingIndicator();
        if (sendBtn) sendBtn.disabled = false;

        const reply = res.response || "I have received your request.";
        conversationHistory.push({ role: 'assistant', content: reply });

        addMessage(reply, 'jarvis', null, res.data, res.llm_powered);

        // Text-to-Speech
        speakText(reply);

        // Auto-navigation if returned by intent engine
        if (res.navigate_to) {
            showToast(`Navigating to ${res.navigate_to}...`, 'info', 2000);
            setTimeout(() => {
                showSection(res.navigate_to);
            }, 1200);
        }

        // Activity log
        logActivity('chat', `Chat: "${messageText.slice(0, 30)}${messageText.length > 30 ? '...' : ''}"`, `Intent: ${res.intent || 'general'}`, '💬');

    } catch (e) {
        hideTypingIndicator();
        if (sendBtn) sendBtn.disabled = false;

        console.error('Chat error:', e);
        const fallbackMsg = "I apologize, but I encountered an error connecting to my core reasoning engine. Please ensure the backend server is running.";
        addMessage(fallbackMsg, 'jarvis');
        showToast('Chat request failed: ' + e.message, 'error');
    }
}

function sendExamplePrompt(promptText) {
    const chatInput = document.getElementById('chat-input');
    if (chatInput) {
        chatInput.value = promptText;
        chatInput.focus();
    }
    sendMessage(promptText);
}

function clearConversation(promptConfirm = true) {
    if (promptConfirm && conversationHistory.length > 0) {
        if (!confirm('Are you sure you want to clear the conversation?')) return;
    }

    conversationHistory = [];
    const chatMessages = document.getElementById('chat-messages');
    if (chatMessages) {
        chatMessages.innerHTML = `
            <div class="message jarvis-message">
                <div class="message-avatar">J</div>
                <div class="message-bubble">
                    <p>Conversation cleared. How can I assist you with Artificial Intelligence concepts, search algorithms, or problem solving?</p>
                    <span class="message-time">Just now</span>
                </div>
            </div>
        `;
    }

    // Also call backend DELETE if supported
    apiCall('/assistant/conversation', 'DELETE').catch(() => {});
    showToast('Conversation cleared', 'info', 1500);
}

// ============================================================================
// INLINE ALGORITHM DATA CARD
// ============================================================================
function renderAlgorithmDataCard(data) {
    if (!data || typeof data !== 'object') return null;

    const card = document.createElement('div');
    card.className = 'chat-data-card card-glass';
    card.style.marginTop = '10px';
    card.style.padding = '10px 14px';
    card.style.borderRadius = '8px';
    card.style.background = 'rgba(0, 212, 255, 0.05)';
    card.style.border = '1px solid rgba(0, 212, 255, 0.2)';
    card.style.fontSize = '0.88rem';

    let content = '<div style="font-weight:600;color:var(--accent-cyan);margin-bottom:6px;">📊 Execution Data</div>';

    if (data.path && Array.isArray(data.path)) {
        content += `<div style="margin-bottom:4px;"><strong>Path:</strong> ${data.path.join(' → ')}</div>`;
    }
    if (data.traversal_order && Array.isArray(data.traversal_order)) {
        content += `<div style="margin-bottom:4px;"><strong>Order:</strong> ${data.traversal_order.join(', ')}</div>`;
    }
    if (data.cost !== undefined) {
        content += `<div style="margin-bottom:4px;"><strong>Cost:</strong> ${data.cost}</div>`;
    }
    if (data.moves !== undefined) {
        content += `<div style="margin-bottom:4px;"><strong>Moves:</strong> ${data.moves}</div>`;
    }
    if (data.viterbi_path && Array.isArray(data.viterbi_path)) {
        content += `<div style="margin-bottom:4px;"><strong>Viterbi Path:</strong> ${data.viterbi_path.join(' → ')}</div>`;
    }
    if (data.forward_prob !== undefined) {
        content += `<div style="margin-bottom:4px;"><strong>Forward Prob:</strong> ${Number(data.forward_prob).toFixed(4)}</div>`;
    }
    if (data.best_x !== undefined && data.best_value !== undefined) {
        content += `<div style="margin-bottom:4px;"><strong>Best X:</strong> ${Number(data.best_x).toFixed(4)}, <strong>Value:</strong> ${Number(data.best_value).toFixed(4)}</div>`;
    }

    card.innerHTML = content;
    return card;
}

// ============================================================================
// CHAT INITIALIZATION & EVENT LISTENERS
// ============================================================================
window.addEventListener('DOMContentLoaded', () => {
    initSpeech();

    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('btn-send');
    const micBtn = document.getElementById('btn-mic');
    const clearBtn = document.getElementById('btn-clear-chat');

    if (chatInput) {
        chatInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
    }

    if (sendBtn) {
        sendBtn.addEventListener('click', (e) => {
            e.preventDefault();
            sendMessage();
        });
    }

    if (micBtn) {
        micBtn.addEventListener('click', (e) => {
            e.preventDefault();
            toggleMic();
        });
    }

    if (clearBtn) {
        clearBtn.addEventListener('click', (e) => {
            e.preventDefault();
            clearConversation(true);
        });
    }
});

// Global exports
window.sendMessage = sendMessage;
window.sendExamplePrompt = sendExamplePrompt;
window.clearConversation = clearConversation;
window.copyMessageText = copyMessageText;
window.speakText = speakText;
window.toggleMic = toggleMic;
window.addMessage = addMessage;
