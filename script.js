/* ==========================================
   1. GLOBAL SYSTEM SETUP & ROUTING
   ========================================== */
const pages = ['home', 'about', 'dashboard', 'company', 'insight', 'contact'];
const navToggle = document.getElementById('navToggle');
const navLinks  = document.getElementById('navLinks');

// Navigation (mobile menu toggle)
if (navToggle && navLinks) {
  navToggle.addEventListener('click', () => navLinks.classList.toggle('open'));
}

// Dynamic Greeting Engine
function getGreeting() {
  const hour = new Date().getHours();
  if (hour < 12) return "Good Morning 🌻";
  if (hour < 17) return "Good Afternoon 🌤️";
  return "Good Evening 🌙";
}

const greetingElement = document.getElementById("greeting");
if (greetingElement) {
  greetingElement.innerText = getGreeting();
}

// Page View Router
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


/* ==========================================
   2. STORY STEPPER & NAVIGATION
   ========================================== */
let currentStep = 1;
const totalSteps = 5; 

function enterSite() {
  const introEl = document.getElementById("intro");
  const mainEl  = document.getElementById("main");
  if (introEl) introEl.style.display = "none";
  if (mainEl)  mainEl.style.display  = "block";
  showPage('home');
}

function updateStepUI() {
  const prevBtn  = document.getElementById('btn-prev');
  const nextBtn  = document.getElementById('btn-next');
  const finalBtn = document.getElementById('btn-final-enter');

  if (prevBtn)  prevBtn.disabled = (currentStep === 1);

  if (currentStep === totalSteps) {
    if (nextBtn)  nextBtn.classList.add('hidden');
    if (finalBtn) finalBtn.classList.remove('hidden');
  } else {
    if (nextBtn)  nextBtn.classList.remove('hidden');
    if (finalBtn) finalBtn.classList.add('hidden');
  }
}

function changeStep(direction) {
  document.getElementById(`step-${currentStep}`).classList.remove('active-step');
  document.getElementById(`dot-${currentStep}`).classList.remove('active');
  currentStep += direction;
  document.getElementById(`step-${currentStep}`).classList.add('active-step');
  document.getElementById(`dot-${currentStep}`).classList.add('active');
  updateStepUI();
}

function goToStep(stepNumber) {
  document.getElementById(`step-${currentStep}`).classList.remove('active-step');
  document.getElementById(`dot-${currentStep}`).classList.remove('active');
  currentStep = stepNumber;
  document.getElementById(`step-${currentStep}`).classList.add('active-step');
  document.getElementById(`dot-${currentStep}`).classList.add('active');
  updateStepUI();
}

function goBackToStory() {
  document.getElementById(`step-${currentStep}`).classList.remove('active-step');
  document.getElementById(`dot-${currentStep}`).classList.remove('active');
  currentStep = 1;
  document.getElementById(`step-${currentStep}`).classList.add('active-step');
  document.getElementById(`dot-${currentStep}`).classList.add('active');
  updateStepUI();

  const mainEl  = document.getElementById("main");
  const introEl = document.getElementById("intro");
  if (mainEl)  mainEl.style.display  = "none";
  if (introEl) introEl.style.display = "block";
}


/* ==========================================
   3. TELECOM FINDER QUIZ
   ========================================== */
function submitQuiz() {
  const loc = document.querySelector('input[name="location"]:checked');
  const purp = document.querySelector('input[name="purpose"]:checked');
  const occ  = document.getElementById('occupation');

  if (!loc || !purp || !occ || occ.value === "") {
    showModal('error', 'Please answer all three questions first.');
    return;
  }

    const locationValue   = loc.value;
    const purposeValue    = purp.value;
    const occupationValue = occ.value;
    let rec = '';

    if (locationValue === 'urban' || locationValue === 'semi') {
      if (purposeValue === 'social' || purposeValue === 'gaming') {
        if (occupationValue === 'farmer' || occupationValue === 'student' || occupationValue === 'other') {
          rec = '📶 <strong>Tashi InfoComm (TashiCell)</strong> — A pricing competitive advantage, or 📡 <strong>Bhutan Telecom Limited</strong> — Good coverage for general daily usage.';
        } else {
          rec = '📶 <strong>Tashi InfoComm (Wi-Fi)</strong> & 📡 <strong>Bhutan Telecom (WiFi)</strong> — Great choice for high performance and stable professional connectivity.';
        }
      } else if (purposeValue === 'work' || purposeValue === 'business') {
        if (['digital', 'civil', 'private', 'entrepreneur'].includes(occupationValue)) {
          rec = '📡 <strong>Bhutan Telecom (Wi-Fi)</strong> & 📶 <strong>TashiCell (Wi-Fi)</strong> — Best for professional and work-from-home use.';
        } else {
          rec = '📡 <strong>Bhutan Telecom</strong> & 📶 <strong>TashiCell</strong> — Suitable options for general workspace needs.';
        }
      } else {
        rec = '📶 <strong>TashiCell</strong> — General recommendation for urban users prioritising cost efficiency.';
      }
    } else if (locationValue === 'rural') {
      if (occupationValue === 'farmer' || occupationValue === 'student' || occupationValue === 'other') {
        rec = '📡 <strong>Bhutan Telecom Limited</strong> — Stronger coverage across rural areas.';
      } else {
        rec = '📡 <strong>Bhutan Telecom (WiFi)</strong> — Stable coverage, & 📶 <strong>TashiCell</strong> — Good cost-effective alternative.';
      }
    } else if (locationValue === 'high-altitude') {
      rec = '🛸 <strong>Starlink</strong> — Best suited for high-altitude and remote areas with weak terrestrial signals. <br>📡 <strong>Bhutan Telecom (B-Mobile)</strong> — A good backup option for lighter usage and cost savings.';
    } else {
      rec = '📶 <strong>Bhutan Telecom & TashiCell</strong> — General recommendation.';
    }

  const el = document.getElementById('quizResult');
  if (el) {
    el.innerHTML = '✅ Based on your answers, we recommend: ' + rec;
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


/* ==========================================
   4. CONTACT FORM & EXTERNAL BACKENDS
   ========================================== */
function clearForm() {
  const nameEl  = document.getElementById("cname");
  const emailEl = document.getElementById("cemail");
  const topicEl = document.getElementById("ctopic");
  const msgEl   = document.getElementById("cmsg");
  if (nameEl)  nameEl.value  = "";
  if (emailEl) emailEl.value = "";
  if (topicEl) topicEl.value = "";
  if (msgEl)   msgEl.value   = "";
}

async function submitToGoogleSheets(name, email, topic, message) {
  const APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyZrGyh2Yx4AO0HynnLkpbvsuQe5jHfWbWXmEpurUc_juJPq7Uy0nR5apYpzr2WGZ-O/exec";
  try {
    await fetch(APPS_SCRIPT_URL, {
      method: "POST",
      mode: "no-cors",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, topic, message })
    });
  } catch (err) {
    console.warn("Google Sheets backup failed:", err);
  }
}

async function handleContact() {
  const name    = document.getElementById("cname").value.trim();
  const email   = document.getElementById("cemail").value.trim();
  const topic   = document.getElementById("ctopic").value;
  const message = document.getElementById("cmsg").value.trim();

  if (!name)                          { showModal('error', 'Please enter your full name.');         return; }
  if (!email || !email.includes('@')) { showModal('error', 'Please enter a valid email address.'); return; }
  if (!topic)                         { showModal('error', 'Please select a topic.');              return; }
  if (!message)                       { showModal('error', 'Please write your message.');          return; }

  const btn = document.querySelector('#contactForm .btn-gold');
  if (!btn) return;

  btn.textContent = 'Sending… ⏳';
  btn.disabled = true;

  try {
    const res  = await fetch('https://bhutan-tele-compass-derx.onrender.com', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ name, email, topic, message })
    });
    const data = await res.json();

    if (res.ok && data.success) {
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


/* ==========================================
   5. MODAL NOTIFICATION UI
   ========================================== */
function showModal(type, message) {
  const existing = document.getElementById('teleModal');
  if (existing) existing.remove();

  const isSuccess = type === 'success';
  const modal = document.createElement('div');
  modal.id = 'teleModal';
  modal.style.cssText = `
    position: fixed; inset: 0; z-index: 9999;
    display: flex; align-items: center; justify-content: center;
    background: rgba(0,0,0,0.55); backdrop-filter: blur(4px);
    animation: modalFadeIn 0.25s ease;
  `;

  modal.innerHTML = `
    <style>
      @keyframes modalFadeIn { from { opacity:0; transform:scale(0.92); } to { opacity:1; transform:scale(1); } }
    </style>
    <div style="
      background: ${isSuccess ? 'linear-gradient(135deg,#0d4f5c,#0c7576)' : 'linear-gradient(135deg,rgba(66,139,121,0.82),rgba(1,103,70,0.73))'};
      border: 1.5px solid ${isSuccess ? 'rgba(72,130,118,0.64)' : 'rgba(21,63,61,0.73)'};
      border-radius: 18px; padding: 2.2rem 2.5rem; max-width: 420px; width: 90%;
      text-align: center; box-shadow: 0 20px 60px rgba(0,0,0,0.4); position: relative;
    ">
      <div style="font-size:2.8rem; margin-bottom:0.75rem; line-height:1;">${isSuccess ? '✅' : '⚠️'}</div>
      <div style="font-family:'Playfair Display',serif; font-size:1.25rem; font-weight:900; color:#fff; margin-bottom:0.6rem; letter-spacing:0.03em;">
        ${isSuccess ? 'Message Sent!' : 'Error'}
      </div>
      <p style="color:rgba(255,251,251,0.94); font-size:0.97rem; font-weight:600; line-height:1.65; margin-bottom:1.5rem; font-family:'DM Sans',sans-serif;">
        ${message}
      </p>
      <button onclick="document.getElementById('teleModal').remove()" style="
        background: rgba(255,255,255,0.2); border: 1.5px solid rgba(255,255,255,0.4);
        border-radius: 50px; color: #fff; font-family: 'DM Sans', sans-serif;
        font-size: 0.92rem; font-weight: 600; padding: 0.55rem 2rem; cursor: pointer; transition: all 0.2s;
      "
      onmouseover="this.style.background='rgba(255,255,255,0.3)'"
      onmouseout="this.style.background='rgba(255,255,255,0.2)'">
        ${isSuccess ? 'Great, thanks! 🙏' : 'OK, got it'}
      </button>
      ${isSuccess ? `
      <div style="margin-top:1.2rem; height:3px; background:rgba(255,255,255,0.15); border-radius:2px; overflow:hidden;">
        <div id="modalTimer" style="height:100%; width:100%; background:#ffffff; border-radius:2px; transition:width 5s linear;"></div>
      </div>
      <p style="color:rgba(255,255,255,0.4); font-size:0.72rem; margin-top:0.4rem;">Closes automatically in 5 seconds</p>
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
      const activeModal = document.getElementById('teleModal');
      if (activeModal) activeModal.remove();
    }, 5000);
  }
}