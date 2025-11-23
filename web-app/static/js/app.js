// API Base URL
const API_BASE = "/chats/api";
const MESSAGES_API = "/messages/api";

// State Management
let currentChatId = null;
let isRecording = false;
let mediaRecorder = null;
let audioChunks = [];

// DOM Elements
const welcomeScreen = document.getElementById("welcome-screen");
const chatArea = document.getElementById("chat-area");
const messagesContainer = document.getElementById("messages");
const recordBtn = document.getElementById("record-btn");
const recordingIndicator = document.getElementById("recording-indicator");
const textInput = document.getElementById("text-input");
const sendBtn = document.getElementById("send-btn");
const newChatBtn = document.getElementById("new-chat-btn");
const chatList = document.getElementById("chat-list");

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  loadChatHistory();
  setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
  // Record button - hold to record
  recordBtn.addEventListener("mousedown", startRecording);
  recordBtn.addEventListener("mouseup", stopRecording);
  recordBtn.addEventListener("mouseleave", () => {
    if (isRecording) stopRecording();
  });

  // Touch events for mobile
  recordBtn.addEventListener("touchstart", (e) => {
    e.preventDefault();
    startRecording();
  });
  recordBtn.addEventListener("touchend", (e) => {
    e.preventDefault();
    stopRecording();
  });

  // Send button
  sendBtn.addEventListener("click", sendTextMessage);
  textInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendTextMessage();
  });

  // New chat button
  newChatBtn.addEventListener("click", createNewChat);
}

// Chat Management
async function createNewChat() {
  try {
    const requestBody = {
      title: "New Conversation",
      created_at: new Date().toISOString(),
      messages: [],
    };

    const response = await fetch(API_BASE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestBody),
    });

    if (response.ok) {
      const data = await response.json();
      currentChatId = data.inserted_id;
      messagesContainer.innerHTML = ""; // clear messages for new chat
      showChatArea();
      loadChatHistory();
    } else {
      showNotification(
        `Failed to create new chat: ${response.status}`,
        "error"
      );
    }
  } catch (error) {
    console.error("Error creating chat:", error);
    showNotification(`Failed to create new chat: ${error.message}`, "error");
  }
}

function renderMarkdown(text) {
  // Convert markdown to HTML
  const html = marked.parse(text);
  // Sanitize for safety
  return DOMPurify.sanitize(html);
}

marked.setOptions({
  highlight: (code, lang) => {
    try {
      return hljs.highlight(code, { language: lang }).value;
    } catch {
      return hljs.highlightAuto(code).value;
    }
  },
});

async function loadChatHistory() {
  try {
    const response = await fetch(API_BASE + "/");
    if (response.ok) {
      const chats = await response.json();
      displayChatList(chats);
    }
  } catch (error) {
    console.error("Error loading chats:", error);
  }
}

function displayChatList(chats) {
  chatList.innerHTML = "";

  if (!chats || chats.length === 0) {
    chatList.innerHTML =
      '<p style="color: var(--text-secondary); text-align: center;">No conversations yet</p>';
    return;
  }

  chats.forEach((chat) => {
    const chatItem = document.createElement("div");
    chatItem.className = "chat-item";
    if (chat._id === currentChatId) {
      chatItem.classList.add("active");
    }

    const title = chat.title || "Conversation";
    const preview =
      chat.messages && chat.messages.length > 0
        ? chat.messages[chat.messages.length - 1].content.substring(0, 50) +
          "..."
        : "Start chatting...";

    chatItem.innerHTML = `
            <div class="chat-item-title">${title}</div>
            <div class="chat-item-preview">${preview}</div>
        `;

    chatItem.addEventListener("click", () => loadChat(chat._id));
    chatList.appendChild(chatItem);
  });
}

async function loadChat(chatId) {
  try {
    const response = await fetch(`${API_BASE}/${chatId}`);
    if (response.ok) {
      const chat = await response.json();
      currentChatId = chatId;
      displayMessages(chat.messages || []);
      showChatArea();
      loadChatHistory(); // Refresh to update active state
    }
  } catch (error) {
    console.error("Error loading chat:", error);
    showNotification("Failed to load chat", "error");
  }
}

// Message Display
function displayMessages(messages) {
  messagesContainer.innerHTML = "";
  messages.forEach((msg) => addMessageToUI(msg));
  scrollToBottom();
}

function addMessageToUI(message) {
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${message.role}`;

  const avatar = message.role === "user" ? "👤" : "🤖";
  const time = new Date(message.timestamp || Date.now()).toLocaleTimeString(
    [],
    {
      hour: "2-digit",
      minute: "2-digit",
    }
  );

  messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div>
           <div class="message-content">${renderMarkdown(message.content)}</div>
            <div class="message-time">${time}</div>
        </div>
    `;

  messagesContainer.appendChild(messageDiv);
  scrollToBottom();
}

// Recording Functions
async function startRecording() {
  if (isRecording) return;

  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      audio: true,
    });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.addEventListener("dataavailable", (event) => {
      audioChunks.push(event.data);
    });

    mediaRecorder.addEventListener("stop", processRecording);

    mediaRecorder.start();
    isRecording = true;
    recordBtn.classList.add("recording");
    recordingIndicator.classList.remove("hidden");
  } catch (error) {
    console.error("Error accessing microphone:", error);
    showNotification(
      "Could not access microphone. Please check permissions.",
      "error"
    );
  }
}

function stopRecording() {
  if (!isRecording || !mediaRecorder) return;

  mediaRecorder.stop();
  mediaRecorder.stream.getTracks().forEach((track) => track.stop());
  isRecording = false;
  recordBtn.classList.remove("recording");
  recordingIndicator.classList.add("hidden");
}

async function processRecording() {
  const audioBlob = new Blob(audioChunks, { type: "audio/webm" });

  // For now, we'll convert to text using a placeholder
  // In production, you'd use a speech-to-text API
  const transcript = await transcribeAudio(audioBlob);

  if (transcript) {
    await sendMessage(transcript);
  }
}

async function transcribeAudio(audioBlob) {
  const formData = new FormData();
  formData.append("audio", audioBlob, "recording.webm");

  showNotification("Transcribing audio...", "info");

  try {
    const res = await fetch("/speech/api/transcribe", {
      method: "POST",
      body: formData,
    });

    if (res.ok) {
      const data = await res.json();
      return data.transcript;
    } else {
      console.log("Transcription failed", await res.text());
      showNotification("Failed to transcribe audio", "error");
      return null;
    }
  } catch (error) {
    console.log("error cant transcribe : ", error);
    showNotification("Error sending audio for transcription", "error");
    return null;
  }
}

// Text Message Functions
async function sendTextMessage() {
  const message = textInput.value.trim();
  if (!message) return;

  textInput.value = "";
  await sendMessage(message);
}

async function sendMessage(content) {
  // Create chat if needed
  if (!currentChatId) {
    await createNewChat();
    if (!currentChatId) return;
  }

  showChatArea();

  // Display user message immediately
  const userMessage = {
    role: "user",
    content: content,
    timestamp: new Date().toISOString(),
  };
  addMessageToUI(userMessage);

  // Show typing indicator
  showTypingIndicator();

  try {
    // Send message to backend
    const response = await fetch(`${API_BASE}/${currentChatId}/message`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userMessage),
    });

    removeTypingIndicator();

    if (response.ok) {
      // the backend now reutrns ai message directly
      const assistantMessage = await response.json();
      addMessageToUI(assistantMessage);
    } else {
      throw new Error("Failed to send message");
    }
  } catch (error) {
    console.error("Error sending message:", error);
    removeTypingIndicator();
    showNotification("Failed to send message. Please try again.", "error");
  }
}

// UI Helper Functions
function showChatArea() {
  welcomeScreen.classList.add("hidden");
  chatArea.classList.remove("hidden");
}

function showTypingIndicator() {
  const indicator = document.createElement("div");
  indicator.className = "message assistant typing-indicator";
  indicator.id = "typing-indicator";
  indicator.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <span style="display: inline-block; animation: bounce 1.4s infinite;">.</span>
            <span style="display: inline-block; animation: bounce 1.4s 0.2s infinite;">.</span>
            <span style="display: inline-block; animation: bounce 1.4s 0.4s infinite;">.</span>
        </div>
    `;
  messagesContainer.appendChild(indicator);
  scrollToBottom();

  // Add animation
  const style = document.createElement("style");
  style.textContent = `
        @keyframes bounce {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-10px); }
        }
    `;
  document.head.appendChild(style);
}

function removeTypingIndicator() {
  const indicator = document.getElementById("typing-indicator");
  if (indicator) indicator.remove();
}

function scrollToBottom() {
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// info green, error red
function showNotification(message, type = "info") {
  // Simple notification system
  const notification = document.createElement("div");
  notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background: ${type === "error" ? "#E74C3C" : "#50C878"};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
    `;
  notification.textContent = message;
  document.body.appendChild(notification);

  setTimeout(() => {
    notification.style.animation = "slideOut 0.3s ease-out";
    setTimeout(() => notification.remove(), 300);
  }, 3000);

  // Add animations
  const style = document.createElement("style");
  style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(400px);
                opacity: 0;
            }
        }
    `;
  if (!document.querySelector("style[data-notification-style]")) {
    style.setAttribute("data-notification-style", "true");
    document.head.appendChild(style);
  }
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}
