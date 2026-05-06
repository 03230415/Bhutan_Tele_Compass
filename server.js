const express = require("express");
const cors    = require("cors");
const path    = require("path");

const app = express();

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

// ── Supabase config ───────────────────────────────
const SUPABASE_URL = process.env.SUPABASE_URL || "https://cdlimimarqcyvngnhuaw.supabase.co";
const SUPABASE_KEY = process.env.SUPABASE_KEY || "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNkbGltaW1hcnFjeXZuZ2hudWF3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzgwNTUwMTIsImV4cCI6MjA5MzYzMTAxMn0.EChGAPwRF28ecxUMLauTVtedcIE8JBeUwyMQIIopw6U";

// Helper: save message to Supabase
async function saveToSupabase(data) {
  const res = await fetch(`${SUPABASE_URL}/rest/v1/messages`, {
    method:  "POST",
    headers: {
      "Content-Type":  "application/json",
      "apikey":        SUPABASE_KEY,
      "Authorization": `Bearer ${SUPABASE_KEY}`,
      "Prefer":        "return=minimal"
    },
    body: JSON.stringify(data)
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(err);
  }
}

// Helper: read all messages from Supabase
async function getFromSupabase() {
  const res = await fetch(`${SUPABASE_URL}/rest/v1/messages?order=received_at.desc`, {
    headers: {
      "apikey":        SUPABASE_KEY,
      "Authorization": `Bearer ${SUPABASE_KEY}`
    }
  });
  if (!res.ok) throw new Error(await res.text());
  return await res.json();
}

// ── HOME ─────────────────────────────────────────
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

// ── ADMIN PAGE ────────────────────────────────────
app.get("/admin", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "admin.html"));
});

// ── POST /message ─────────────────────────────────
app.post("/message", async (req, res) => {
  const { name, email, topic, message } = req.body;

  if (!name || !email || !message) {
    return res.status(400).json({ success: false, error: "Name, email and message are required." });
  }

  try {
    await saveToSupabase({
      name:    name.trim(),
      email:   email.trim(),
      topic:   topic || "General",
      message: message.trim()
      // received_at is set automatically by Supabase
    });

    console.log("📬 Saved to Supabase:", name, email);

    res.status(200).json({
      success: true,
      message: "✅ Thank you! Your message has been received. We will reply within 2 business days."
    });

  } catch (err) {
    console.error("Supabase save error:", err.message);
    res.status(500).json({ success: false, error: "Failed to save message. Please try again." });
  }
});

// ── GET /messages ─────────────────────────────────
app.get("/messages", async (req, res) => {
  try {
    const messages = await getFromSupabase();
    res.json({ total: messages.length, messages });
  } catch (err) {
    res.status(500).json({ error: "Failed to fetch messages." });
  }
});

// ── Fallback ──────────────────────────────────────
app.get("*", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`✅ Server running on port ${PORT}`));