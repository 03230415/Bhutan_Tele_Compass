// ── Navigation (mobile menu toggle) ──
const navToggle = document.getElementById('navToggle');
const navLinks  = document.getElementById('navLinks');
if (navToggle && navLinks) {
  navToggle.addEventListener('click', () => navLinks.classList.toggle('open'));
}

function getGreeting() {
  const hour = new Date().getHours();
  let greeting = '';
  if (hour < 12) {
    greeting = "Good Morning 🌻";
  } else if (hour < 17) {
    greeting = "Good Afternoon 🌤️";
  } else {
    greeting = "Good Evening 🌙";
  }
  return greeting;
}

document.getElementById("greeting").innerText = getGreeting();

// Clear Answers 🧹
function clearForm() {
  document.getElementById("cname").value  = "";
  document.getElementById("cemail").value = "";
  document.getElementById("ctopic").value = "";
  document.getElementById("cmsg").value   = "";
}

function enterSite() {
  document.getElementById("intro").style.display = "none";
  document.getElementById("main").style.display  = "block";
}

function goBackToStory() {
  document.getElementById("main").style.display  = "none";
  document.getElementById("intro").style.display = "block";
}

// ── Page Router ──
const pages = ['home','about','dashboard','company','contact'];

function showPage(id) {
  pages.forEach(p => {
    const pg  = document.getElementById('page-' + p);
    const btn = document.getElementById('nav-' + p);
    if (pg)  pg.classList.remove('active');
    if (btn) btn.classList.remove('active');
  });
  const target = document.getElementById('page-' + id);
  const navBtn = document.getElementById('nav-' + id);
  if (target) target.classList.add('active');
  if (navBtn) navBtn.classList.add('active');
  if (navLinks) navLinks.classList.remove('open');
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ── Modal helper ────────────────────────────────
function showModal(type, message) {
  const existing = document.getElementById('teleModal');
  if (existing) existing.remove();

  const isSuccess = type === 'success';

  const modal = document.createElement('div');
  modal.id = 'teleModal';
  modal.style.cssText = `
    position: fixed;
    inset: 0;
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(0,0,0,0.55);
    backdrop-filter: blur(4px);
    animation: modalFadeIn 0.25s ease;
  `;

  modal.innerHTML = `
    <style>
      @keyframes modalFadeIn  { from { opacity:0; transform:scale(0.92); } to { opacity:1; transform:scale(1); } }
      @keyframes modalFadeOut { from { opacity:1; transform:scale(1);    } to { opacity:0; transform:scale(0.92); } }
    </style>
    <div style="
      background: ${isSuccess ? 'linear-gradient(135deg,#0d4f5c,#0c7576)' : 'linear-gradient(135deg, rgba(66,139,121,0.82), rgba(1,103,70,0.73))'};
      border: 1.5px solid ${isSuccess ? 'rgba(72,130,118,0.64)' : 'rgba(21,63,61,0.73)'};
      border-radius: 18px;
      padding: 2.2rem 2.5rem;
      max-width: 420px;
      width: 90%;
      text-align: center;
      box-shadow: 0 20px 60px rgba(129,105,105,0.79);
      position: relative;
    ">
      <div style="font-size:2.8rem; margin-bottom:0.75rem; line-height:1;">
        ${isSuccess ? '✅' : '⚠️'}
      </div>
      <div style="
        font-family:'Playfair Display',serif;
        font-size:1.25rem;
        font-weight:900;
        color:#ffffff;
        margin-bottom:0.6rem;
        letter-spacing:0.03em;
      ">
        ${isSuccess ? 'Message Sent!' : 'Error❕'}
      </div>
      <p style="
        color: rgba(255,251,251,0.94);
        font-size: 0.97rem;
        font-weight: 600;
        line-height: 1.65;
        margin-bottom: 1.5rem;
        font-family: 'DM Sans', sans-serif;
      ">${message}</p>
      <button onclick="document.getElementById('teleModal').remove()" style="
        background: rgba(59,134,119,0.9);
        border: 1.5px solid rgba(30,74,66,0.79);
        border-radius: 50px;
        color: #342222;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.92rem;
        font-weight: 600;
        padding: 0.55rem 2rem;
        cursor: pointer;
        transition: background 0.2s;
      "
      onmouseover="this.style.background='rgba(159,138,138,0.58)'"
      onmouseout="this.style.background='rgba(149,132,132,0.54)'"
      >
        ${isSuccess ? 'Great, thanks! 🙏' : 'OK, got it'}
      </button>
      ${isSuccess ? `
      <div style="
        margin-top: 1.2rem;
        height: 3px;
        background: rgba(255,255,255,0.15);
        border-radius: 2px;
        overflow: hidden;
      ">
        <div id="modalTimer" style="
          height: 100%;
          width: 100%;
          background: rgba(115,163,153,0.7);
          border-radius: 2px;
          transition: width 5s linear;
        "></div>
      </div>
      <p style="color:rgba(255,255,255,0.4);font-size:0.72rem;margin-top:0.4rem;">Closes automatically in 5 seconds</p>
      ` : ''}
    </div>
  `;

  document.body.appendChild(modal);

  modal.addEventListener('click', (e) => {
    if (e.target === modal) modal.remove();
  });

  if (isSuccess) {
    requestAnimationFrame(() => {
      const bar = document.getElementById('modalTimer');
      if (bar) bar.style.width = '0%';
    });
    setTimeout(() => {
      if (document.getElementById('teleModal')) {
        document.getElementById('teleModal').remove();
      }
    }, 5000);
  }
}

// ── Google Sheets submission via Apps Script ──
async function submitToGoogleSheets(name, email, topic, message) {
  const APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyFgjwvFEW3J-cOkCeude7_ENzDDUG39X5oTLt0MMLHIRf4Ev4MuKo8Y0oCD_ATXhUA/exec";

  try {
    await fetch(APPS_SCRIPT_URL, {
      method: "POST",
      mode: "no-cors", // required for Apps Script — response will be opaque but data still saves
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, topic, message })
    });
  } catch (err) {
    // Silent fail — this is a backup, main submission already succeeded
    console.warn("Google Sheets backup failed:", err);
  }
}

// ── Contact Form ────────────────────────────────
async function handleContact() {
  const name    = document.getElementById("cname").value.trim();
  const email   = document.getElementById("cemail").value.trim();
  const topic   = document.getElementById("ctopic").value;
  const message = document.getElementById("cmsg").value.trim();

  // validation
  if (!name)                          { showModal('error', 'Please enter your full name.');         return; }
  if (!email || !email.includes('@')) { showModal('error', 'Please enter a valid email address.'); return; }
  if (!topic)                         { showModal('error', 'Please select a topic.');              return; }
  if (!message)                       { showModal('error', 'Please write your message.');          return; }

  const btn = document.querySelector('#contactForm .btn-gold');
  btn.textContent = 'Sending… ⏳';
  btn.disabled = true;

  try {
    // ── 1. Send to Flask backend (admin history) ──
    const res  = await fetch('/message', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ name, email, topic, message })
    });

    const data = await res.json();

    if (res.ok && data.success) {
      // ── 2. Also send to Google Sheets via Apps Script (silent backup) ──
      submitToGoogleSheets(name, email, topic, message);

      clearForm();
      showModal('success', data.message);
    } else {
      showModal('error', data.error || 'Something went wrong. Please try again.');
    }

  } catch (err) {
    showModal('error', 'Could not reach the server. Please try again.');
    console.error(err);

  } finally {
    btn.textContent = 'Send Message ✈️';
    btn.disabled = false;
  }
}

// ── Company Quiz ────────────────────────────────
function submitQuiz() {
  const loc  = document.querySelector('input[name="location"]:checked');
  const purp = document.querySelector('input[name="purpose"]:checked');
  const occ  = document.getElementById('occupation');

  if (!loc || !purp || !occ) {
    showModal('error', 'Please answer all three questions first.');
    return;
  }

  let rec = '';

  if (loc.value === 'urban' || loc.value === 'semi') {
    if (purp.value === 'social' || purp.value === 'gaming') {
      if (occ.value === 'farmer' || occ.value === 'student' || occ.value === 'other') {
        rec = '📶 <strong>Tashi InfoComm (TashiCell)</strong> — A good pricing competitive advantage and 📡 <strong>Bhutan Telecom Limited</strong> — Good coverage and for daily usage.';
      } else if (occ.value === 'digital' || occ.value === 'civil' || occ.value === 'private' || occ.value === 'entrepreneur') {
        rec = '📶 <strong>Tashi InfoComm (Wi-Fi)</strong> &amp; 📡 <strong>Bhutan Telecom (WiFi)</strong> — good for performance and stable connectivity.';
      }
    } else if (purp.value === 'work' || purp.value === 'business') {
      if (occ.value === 'digital' || occ.value === 'civil' || occ.value === 'private' || occ.value === 'entrepreneur') {
        rec = '📡 <strong>Bhutan Telecom (Wi-Fi)</strong> &amp; 📶 <strong>TashiCell</strong> (Wi-Fi) — best for professional use and stable connection.';
      } else {
        rec = '📡 <strong>Bhutan Telecom</strong> &amp; 📶 <strong>TashiCell</strong> — suitable for general work needs.';
      }
    } else {
      rec = '📶 <strong>TashiCell</strong> — general recommendation for urban and semi-urban users with pricing competitive advantage.';
    }
  } else if (loc.value === 'rural') {
    if (occ.value === 'farmer' || occ.value === 'student' || occ.value === 'other') {
      rec = '📡 <strong>Bhutan Telecom Limited</strong> — Better coverage in rural areas.';
    } else if (occ.value === 'digital' || occ.value === 'civil' || occ.value === 'private' || occ.value === 'entrepreneur') {
      rec = '📡 <strong>Bhutan Telecom (WiFi)</strong> — Better coverage &amp; 📶 <strong>TashiCell</strong> — Good for cost effectiveness.';
    } else {
      rec = '📡 <strong>Bhutan Telecom</strong> — reliable rural connectivity.';
    }
  } else if (loc.value === 'high altitude') {
    rec = '🛸 <strong>Starlink</strong> — best for high-altitude and remote areas having weak signal issues.';
  } else {
    rec = '📶 <strong>Bhutan Telecom &amp; TashiCell</strong> — general recommendation.';
  }

  const el = document.getElementById('quizResult');
  if (el) {
    el.innerHTML = '✅ Based on your answers, we suggest: ' + rec;
    el.style.display = 'block';
    el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
}

function resetQuiz() {
  document.querySelectorAll('input[name="location"]').forEach(r => r.checked = false);
  document.querySelectorAll('input[name="purpose"]').forEach(r => r.checked = false);
  const occ = document.getElementById('occupation');
  if (occ) occ.selectedIndex = 0;
  const el = document.getElementById('quizResult');
  if (el) {
    el.style.display = 'none';
    el.innerHTML = '';
  }
}