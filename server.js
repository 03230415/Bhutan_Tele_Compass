const express = require("express");
const cors    = require("cors");
const path    = require("path");
const fs      = require("fs");   // built-in Node.js — no install needed

const app = express();

// ── Middleware ──────────────────────────────────
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

// ── Path to your messages storage file ──────────
// messages.json will be created automatically on first submission
const MESSAGES_FILE = path.join(__dirname, "messages.json");

// Helper: read all saved messages from file
function readMessages() {
  if (!fs.existsSync(MESSAGES_FILE)) return [];
  const raw = fs.readFileSync(MESSAGES_FILE, "utf-8");
  return JSON.parse(raw);
}

// Helper: save messages array back to file
function saveMessages(messages) {
  fs.writeFileSync(MESSAGES_FILE, JSON.stringify(messages, null, 2));
}

// ── HOME route ───────────────────────────────────
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

// ── POST /message — receive and SAVE contact form ──
app.post("/message", (req, res) => {
  const { name, email, topic, message } = req.body;

  // Basic validation
  if (!name || !email || !message) {
    return res.status(400).json({ success: false, error: "Name, email and message are required." });
  }

  // Build the new message entry
  const newMessage = {
    id:         Date.now(),
    name:       name.trim(),
    email:      email.trim(),
    topic:      topic || "General",
    message:    message.trim(),
    receivedAt: new Date().toLocaleString("en-BT", { timeZone: "Asia/Thimphu" })
  };

  // Read existing → add new → save back
  const allMessages = readMessages();
  allMessages.push(newMessage);
  saveMessages(allMessages);

  console.log("📬 New message saved:", newMessage);

  res.status(200).json({ success: true, message: "✅ Message received! We will reply within 2 business days." });
});

// ── GET /messages — view all saved messages ──────
// Visit https://your-app.onrender.com/messages to see all submissions
app.get("/messages", (req, res) => {
  const all = readMessages();
  res.json({ total: all.length, messages: all });
});

// ── Fallback ─────────────────────────────────────
app.get("*", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

// ── Start ────────────────────────────────────────
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`✅ TeleCompass server running on port ${PORT}`);
});