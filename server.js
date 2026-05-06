const express = require("express");
const cors    = require("cors");
const path    = require("path");
const fs      = require("fs");

const app = express();

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

const MESSAGES_FILE = path.join(__dirname, "messages.json");

function readMessages() {
  if (!fs.existsSync(MESSAGES_FILE)) return [];
  return JSON.parse(fs.readFileSync(MESSAGES_FILE, "utf-8"));
}

function saveMessages(messages) {
  fs.writeFileSync(MESSAGES_FILE, JSON.stringify(messages, null, 2));
}

// ── HOME ─────────────────────────────────────────
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

// ── ADMIN PAGE ───────────────────────────────────
app.get("/admin", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "admin.html"));
});

// ── POST /message ─────────────────────────────────
app.post("/message", (req, res) => {
  const { name, email, topic, message } = req.body;

  if (!name || !email || !message) {
    return res.status(400).json({ success: false, error: "Name, email and message are required." });
  }

  const newMessage = {
    id:         Date.now(),
    name:       name.trim(),
    email:      email.trim(),
    topic:      topic || "General",
    message:    message.trim(),
    receivedAt: new Date().toLocaleString("en-BT", { timeZone: "Asia/Thimphu" })
  };

  const all = readMessages();
  all.push(newMessage);
  saveMessages(all);

  console.log("📬 Saved:", newMessage);

  res.status(200).json({ success: true, message: "✅ Thank you! Your message has been received. We will reply within 2 business days." });
});

// ── GET /messages ─────────────────────────────────
app.get("/messages", (req, res) => {
  res.json({ total: readMessages().length, messages: readMessages() });
});

// ── Fallback ──────────────────────────────────────
app.get("*", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`✅ Server running on port ${PORT}`));