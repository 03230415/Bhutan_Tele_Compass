  
//   <script>
    // ── Navigation (mobile menu toggle) ──
    // const - creates a variable navToggle and navLinks
    // getElementById - find element by its id
    // if - check if something is true
    // navToggle(☰ icon) && navLinks - both must exist
    const navToggle = document.getElementById('navToggle');
    const navLinks  = document.getElementById('navLinks');
    if (navToggle && navLinks) {
      // When you click the menu button (☰), it shows or hides the navigation menu.
      navToggle.addEventListener('click', () => navLinks.classList.toggle('open'));}
    // 👉 Click button → menu opens
  // 👉 Click again → menu closes

    // ////////// //
  // java script//
  // ////////// //

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
  document.getElementById("cname").value = "";
  document.getElementById("cemail").value = "";
  document.getElementById("ctopic").value = "";
  document.getElementById("cmsg").value = "";
}
 
  function enterSite() {
    document.getElementById("intro").style.display = "none";
    document.getElementById("main").style.display = "block";
  }

  function goBackToStory() {
    document.getElementById("main").style.display = "none";
    document.getElementById("intro").style.display = "block";
  }

  // ── Page Router ──
    // movement between section
    const pages = ['home','about','dashboard','company','contact'];

    function showPage(id) {      // you are trying to show one page at a time (id - which page to show?)
      pages.forEach(p => {       // goes through every page you have (p - each page name one by one)
        const pg  = document.getElementById('page-' + p);  // pg variable, get page by id, page-home(p)   -html
        const btn = document.getElementById('nav-' + p);    // btn variable, get page by id, nav-home(p)  - menu button
        if (pg)  pg.classList.remove('active');     //hide page (displays all at once)
        if (btn) btn.classList.remove('active');         //hide page  (highlight on nav-button)
      });
      const target = document.getElementById('page-' + id);
      const navBtn = document.getElementById('nav-' + id);
      if (target) target.classList.add('active');
      if (navBtn) navBtn.classList.add('active');
      if (navLinks) navLinks.classList.remove('open');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }



























    // ── Contact Form ──
    // Create a function called when user submits the form
 // ══════════════════════════════════════════════════
//  REPLACE your handleContact() function in script.js
//  with this one. Everything else in your script.js
//  stays exactly the same.
// ══════════════════════════════════════════════════
// ══════════════════════════════════════════════════
//  Drop-in replacement for handleContact() in script.js
//  Also adds showModal() helper — no HTML changes needed.
// ══════════════════════════════════════════════════

// ── Modal helper — inject once, reuse forever ────
function showModal(type, message) {
  // Remove any existing modal
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
      background: ${isSuccess ? 'linear-gradient(135deg,#0d4f5c,#0c7576)' : 'linear-gradient(135deg, rgba(66, 139, 121, 0.82),rgba(1, 103, 70, 0.73))'};
      border: 1.5px solid ${isSuccess ? 'rgba(72, 130, 118, 0.64)' : 'rgba(21, 63, 61, 0.73)'};
      border-radius: 18px;
      padding: 2.2rem 2.5rem;
      max-width: 420px;
      width: 90%;
      text-align: center;
      box-shadow: 0 20px 60px rgba(129, 105, 105, 0.79);
      position: relative;
    ">
      <!-- Icon -->
      <div style="font-size:2.8rem; margin-bottom:0.75rem; line-height:1;">
        ${isSuccess ? '✅' : '⚠️'}
      </div>

      <!-- Title -->
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

      <!-- Message -->
      <p style="
        color: rgba(255, 251, 251, 0.94);
        font-size: 0.97rem;
        font-weight: 600;
        line-height: 1.65;
        margin-bottom: 1.5rem;
        font-family: 'DM Sans', sans-serif;
      ">${message}</p>

      <!-- Close button -->
      <button onclick="document.getElementById('teleModal').remove()" style="
        background: rgba(59, 134, 119, 0.9);
        border: 1.5px solid rgba(30, 74, 66, 0.79);
        border-radius: 50px;
        color: #342222;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.92rem;
        font-weight: 600;
        padding: 0.55rem 2rem;
        cursor: pointer;
        transition: background 0.2s;
      "
      onmouseover="this.style.background='rgba(159, 138, 138, 0.58)'"
      onmouseout="this.style.background='rgba(149, 132, 132, 0.54)'"
      >
        ${isSuccess ? 'Great, thanks! 🙏' : 'OK, got it'}
      </button>

      <!-- Auto-close bar (success only) -->
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
          background: rgba(115, 163, 153, 0.7);
          border-radius: 2px;
          transition: width 5s linear;
        "></div>
      </div>
      <p style="color:rgba(255,255,255,0.4);font-size:0.72rem;margin-top:0.4rem;">Closes automatically in 5 seconds</p>
      ` : ''}
    </div>
  `;

  document.body.appendChild(modal);

  // Close on backdrop click
  modal.addEventListener('click', (e) => {
    if (e.target === modal) modal.remove();
  });

  // Auto-close + shrink bar for success
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


// ── handleContact — replaces your old one ────────
async function handleContact() {
  const name    = document.getElementById("cname").value.trim();
  const email   = document.getElementById("cemail").value.trim();
  const topic   = document.getElementById("ctopic").value;
  const message = document.getElementById("cmsg").value.trim();

  // ── Validation — styled modals instead of alert() ──
  if (!name)                         { showModal('error', 'Please enter your full name.');         return; }
  if (!email || !email.includes('@')) { showModal('error', 'Please enter a valid email address.'); return; }
  if (!topic)                         { showModal('error', 'Please select a topic.');              return; }
  if (!message)                       { showModal('error', 'Please write your message.');          return; }

  // ── Loading state on button ──
// ── GitHub Pages fallback ──
  if (window.location.hostname.includes('github.io')) {
    showModal('success', '✅ Thank you! Message received. Note: this is a GitHub Pages demo — contact form is fully functional on the live site.');
    clearForm();
    return;
  }

  // ── Loading state on button ──
  const btn = document.querySelector('#contactForm .btn-gold');
  
  btn.textContent = 'Sending… ⏳';
  btn.disabled = true;

  try {
    const res  = await fetch('/message', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ name, email, topic, message })
    });

    const data = await res.json();

    if (res.ok && data.success) {
      clearForm();
      showModal('success', data.message);   // AI reply shown here
    } 
    // else {
    //   showModal('error', data.error || 'Something went wrong. Please try again.');
    // }

  } catch (err) {
    showModal('error', 'Could not reach the server. Something went wrong. Please try again.');
    console.error(err);

  } finally {
    btn.textContent = 'Send Message ✈️';
    btn.disabled = false;
  }
}
      // ?. - safty check - continue only if element exists
      // const name  = document.getElementById('cname')?.value.trim();
      // const email = document.getElementById('cemail')?.value.trim();
      // const topic = document.getElementById('ctopic')?.value;
      // const msg   = document.getElementById('cmsg')?.value.trim();
      // warning for missing information
      















    // ── Company Quiz ──
    // recommendation box 
    // submit box
    function submitQuiz() {  
      ////// /* find the slected location option and store it in (loc)*/ //////
      // const - create a variable - storage box
      // loc - name of the box - short for location
      // document - whole webpage
      // querySelector - go find something on the page
      // input - radio button/checkbox 
      // name=location - group called location
      // :checked - only selected one
      const loc  = document.querySelector('input[name="location"]:checked');
      ////// /* find the slected purpose option and store it in (purp)*/ //////
      // purp - short for purpose
      const purp = document.querySelector('input[name="purpose"]:checked');
      ////// /* fget the text user typed in occupation box*/ //////
      // occ - occupation
      // value - get what user typed inside it
      // ?. - safty check - continue only if element exists
      const occ  = document.getElementById('occupation');

      // if any checkbox is missing
      //  || - or
      // if condition
      if (!loc || !purp || !occ) {
        // alert
        firstshowModal('error', 'Please answer all three questions first.');
        // stop the function - end with the warning
        return;
      }

      //find my provider button functioning
      // let - creates a variable
      // rec - recommendation
      // '' - empty box fo now
      let rec = '';    //this is the recommendation box             // create an empty box called rec
      /////// i will store the result here later/////////////
      if (loc.value === 'urban' || loc.value === 'semi') {
        if (purp.value === 'social' || purp.value === 'gaming') {
          if (  
            occ.value === 'farmer' || 
            occ.value === 'student' || 
            occ.value === 'other'
          ) {
            rec = '📶 <strong>Tashi InfoComm (TashiCell)</strong> - A good pricing competitive advantage and 📡 <strong>Bhutan Telecom Limited</strong> — Good coverage and for daily usage ';
          } 

          else if (
            occ.value === 'digital' ||
            occ.value === 'civil' ||
            occ.value === 'private' ||
            occ.value === 'entrepreneur'
          ) {
            rec = '📶 <strong>Tashi InfoComm (Wi-Fi)</strong> &amp; 📡 <strong>Bhutan Telecom (WiFi)</strong> — good for performance and stable connectivity.';
          }
        }

        // WORK OR BUSINESS
        else if (purp.value === 'work' || purp.value === 'business') {

          if (
            occ.value === 'digital' ||
            occ.value === 'civil' ||
            occ.value === 'private' ||
            occ.value === 'entrepreneur'
          ) {
            rec = '📡 <strong>Bhutan Telecom (Wi-Fi)</strong> &amp; 📶 <strong>TashiCell</strong>(Wi-Fi) — best for professional use and stable connection.';
          }

          else {
            rec = '📡 <strong>Bhutan Telecom</strong> &amp; 📶 <strong>TashiCell</strong> — suitable for general work needs.';
          }
        }

        // FALLBACK
        else {
          rec = '📶 <strong>TashiCell</strong> — general recommendation for urban and semi-urban users with pricing competitive advantage.';
        }
      }
    

      // ───── RURAL ─────
      else if (loc.value === 'rural') {

        if (
          occ.value === 'farmer' ||
          occ.value === 'student' ||
          occ.value === 'other'
        ) {
          rec = '📡 <strong>Bhutan Telecom Limited</strong> — Better coverage in rural areas.';
        }

        else if (
          occ.value === 'digital' ||
          occ.value === 'civil' ||
          occ.value === 'private' ||
          occ.value === 'entrepreneur'
        ) {
          rec = '📡 <strong>Bhutan Telecom (WiFi)</strong> - Better coverage &amp; 📶 <strong>TashiCell</strong> — Good for cost effectiveness.';
        }

        else {
          rec = '📡 <strong>Bhutan Telecom</strong> — reliable rural connectivity.';
        }
      }

      // ───── HIGH ALTITUDE ─────
      else if (loc.value === 'high altitude') {
        rec = '🛸 <strong>Starlink</strong> — best for high-altitude and plane remote areas having weak signal issues.';
      }

      // ───── DEFAULT FALLBACK ─────
      else {
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
      // r → each radio butto, .checked - whether selected or not, false - unselect it
      document.querySelectorAll('input[name="location"]').forEach(r => r.checked = false);
      document.querySelectorAll('input[name="purpose"]').forEach(r => r.checked = false);
      // find drop down box
      const occ = document.getElementById('occupation');
      // if dropdown exist, selected index, select the first option - reset by default
      if (occ) occ.selectedIndex = 0;
      // Find result message box
      const el = document.getElementById('quizResult');
      if (el) {
        // Hide the result box
        el.style.display = 'none';
        // Remove previous result text completely,-- innerHTML contains a result text
        el.innerHTML = '';
      }
    }
    
//   </script>
