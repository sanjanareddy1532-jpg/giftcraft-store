/**
 * GiftCraft AI - Frontend Application Core
 * Manages State, Catalog, AI Sales Concierge, Checkout, Scratch Card, and Telugu/English Localization.
 */

// Global Application State
const AppState = {
  currentLang: 'te', // 'te' (Telugu) or 'en' (English)
  cards: [],
  selectedCategory: 'all',
  selectedSort: 'popular',
  searchQuery: '',
  activeCardForCheckout: null,
  selectedDenomination: 0,
  appliedCoupon: null,
  voiceEnabled: true,
  isRecording: false,
  speechSynth: window.speechSynthesis || null
};

// Telugu / English Translations Dictionary
const I18N = {
  en: {
    navSubtitle: "All Gift Cards & AI Sales Concierge",
    checkBalance: "Check Balance",
    adminAnalytics: "Sales Analytics",
    heroBadge: "100% Verified Digital Codes • Instant Scratch & Redeem",
    heroTitlePrefix: "Discover & Buy All Kinds of",
    heroTitleHighlight: "Gift Cards with AI Assistance",
    heroDesc: "Amazon, Steam, Flipkart, Netflix, Google Play, Zomato, PlayStation, Domino's, Apple & more! Let our AI Assistant pick the perfect card, apply discounts, and generate custom greeting messages.",
    tryAsking: "Try Asking:",
    instantDelivery: "Instant E-Delivery",
    instantDesc: "Code reveals in 5 seconds",
    discountsTitle: "Up to 15% Savings",
    discountsDesc: "Direct brand cashbacks",
    greetingsTitle: "AI Custom Wishes",
    greetingsDesc: "Heartfelt greeting cards",
    upiTitle: "UPI & QR Instant",
    upiDesc: "GPay, PhonePe, Cards",
    recentLabel: "Recent Purchases:",
    catAll: "All Cards",
    catGaming: "Gaming",
    catShopping: "Shopping",
    catEnt: "Entertainment",
    catFood: "Food & Dining",
    catTravel: "Travel",
    catSoftware: "Software",
    sortLabel: "Sort:",
    askGenieBtn: "Ask GiftGenie AI",
    aiWelcomeHead: "Hello! I am GiftGenie, your AI Gift Card Sales Concierge 🎁",
    aiWelcomeBody: "What type of gift card are you looking for? Gaming, shopping, movies, food or travel? Tell me who it is for and your budget—I will instantly find the best discount and delivery for you!"
  },
  te: {
    navSubtitle: "అన్ని రకాల గిఫ్ట్ కార్డ్‌లు & AI సేల్స్ అసిస్టెంట్",
    checkBalance: "బ్యాలెన్స్ చెక్",
    adminAnalytics: "సేల్స్ అనలిటిక్స్",
    heroBadge: "100% వెరిఫైడ్ డిజిటల్ కోడ్‌లు • తక్షణ స్క్రాచ్ & రిడీమ్",
    heroTitlePrefix: "అన్ని రకాల బ్రాండెడ్ గిఫ్ట్ కార్డ్‌లు",
    heroTitleHighlight: "AI సహాయంతో క్షణాల్లో కొనండి!",
    heroDesc: "అమెజాన్, స్టీమ్, ఫ్లిప్‌కార్ట్, నెట్‌ఫ్లిక్స్, గూగుల్ ప్లే, జొమాటో, ప్లేస్టేషన్, డొమినోస్ మరియు మరెన్నో! మా AI సేల్స్ అసిస్టెంట్ మీ బడ్జెట్‌కు సరిపోయే బెస్ట్ కార్డ్ సూచిస్తుంది మరియు స్పెషల్ గ్రీటింగ్స్ కూడా రాస్తుంది.",
    tryAsking: "ఇలా అడగండి:",
    instantDelivery: "తక్షణ ఇ-డెలివరీ",
    instantDesc: "5 సెకన్లలో కోడ్ రెడీ",
    discountsTitle: "15% వరకు ఆదా",
    discountsDesc: "డైరెక్ట్ క్యాష్‌బ్యాక్",
    greetingsTitle: "AI గ్రీటింగ్ విషెస్",
    greetingsDesc: "అందమైన శుభాకాంక్షలు",
    upiTitle: "UPI & QR పేమెంట్స్",
    upiDesc: "GPay, PhonePe, Paytm",
    recentLabel: "తాజా కొనుగోళ్లు:",
    catAll: "అన్ని కార్డ్‌లు",
    catGaming: "గేమింగ్",
    catShopping: "షాపింగ్",
    catEnt: "సినిమాలు & OTT",
    catFood: "ఫుడ్ & డైనింగ్",
    catTravel: "ట్రావెల్ & హోటల్స్",
    catSoftware: "సాఫ్ట్‌వేర్ & యాప్స్",
    sortLabel: "సార్ట్:",
    askGenieBtn: "GiftGenie AI అడగండి",
    aiWelcomeHead: "నమస్కారం! నేను మీ GiftGenie AI సేల్స్ అసిస్టెంట్‌ని. 🎁",
    aiWelcomeBody: "మీకు ఏ రకమైన గిఫ్ట్ కార్డ్ కావాలి? స్నేహితుల పుట్టినరోజు, గేమింగ్, ఫ్యామిలీ షాపింగ్ లేదా మూవీస్ ఏదైనా సరే - మీ బడ్జెట్ చెప్తే బెస్ట్ డిస్కౌంట్‌తో క్షణాల్లో సూచిస్తాను!"
  }
};

// Initialize Application on DOM Ready
document.addEventListener('DOMContentLoaded', () => {
  initLanguageToggle();
  fetchCards();
  initCategoryFilters();
  initSortAndSearch();
  initAIChat();
  initCheckoutFlow();
  initModals();
  fetchRecentOrders();
});

// ----------------- Language Localization -----------------
function initLanguageToggle() {
  const toggleBtn = document.getElementById('lang-toggle-btn');
  const btnText = document.getElementById('lang-btn-text');

  toggleBtn.addEventListener('click', () => {
    AppState.currentLang = AppState.currentLang === 'te' ? 'en' : 'te';
    btnText.textContent = AppState.currentLang === 'te' ? 'తెలుగు (TE)' : 'English (EN)';
    applyLanguage();
    renderCards(AppState.cards);
  });

  applyLanguage();
}

function applyLanguage() {
  const lang = I18N[AppState.currentLang];
  
  document.getElementById('nav-subtitle').textContent = lang.navSubtitle;
  document.getElementById('txt-check-balance').textContent = lang.checkBalance;
  document.getElementById('txt-admin-analytics').textContent = lang.adminAnalytics;
  document.getElementById('hero-badge').textContent = lang.heroBadge;
  document.getElementById('hero-title-prefix').textContent = lang.heroTitlePrefix;
  document.getElementById('hero-title-highlight').textContent = lang.heroTitleHighlight;
  document.getElementById('hero-desc').textContent = lang.heroDesc;
  document.getElementById('try-asking-txt').textContent = lang.tryAsking;

  document.getElementById('pillar-instant-title').textContent = lang.instantDelivery;
  document.getElementById('pillar-instant-desc').textContent = lang.instantDesc;
  document.getElementById('pillar-discounts-title').textContent = lang.discountsTitle;
  document.getElementById('pillar-discounts-desc').textContent = lang.discountsDesc;
  document.getElementById('pillar-greetings-title').textContent = lang.greetingsTitle;
  document.getElementById('pillar-greetings-desc').textContent = lang.greetingsDesc;
  document.getElementById('pillar-upi-title').textContent = lang.upiTitle;
  document.getElementById('pillar-upi-desc').textContent = lang.upiDesc;

  document.getElementById('recent-live-label').textContent = lang.recentLabel;
  document.getElementById('cat-all-txt').textContent = lang.catAll;
  document.getElementById('cat-gaming-txt').textContent = lang.catGaming;
  document.getElementById('cat-shopping-txt').textContent = lang.catShopping;
  document.getElementById('cat-ent-txt').textContent = lang.catEnt;
  document.getElementById('cat-food-txt').textContent = lang.catFood;
  document.getElementById('cat-travel-txt').textContent = lang.catTravel;
  document.getElementById('cat-soft-txt').textContent = lang.catSoftware;
  document.getElementById('sort-label').textContent = lang.sortLabel;
  document.getElementById('floating-ai-label').textContent = lang.askGenieBtn;

  document.getElementById('ai-welcome-heading').textContent = lang.aiWelcomeHead;
  document.getElementById('ai-welcome-body').textContent = lang.aiWelcomeBody;
}

// ----------------- Fetch & Render Gift Cards -----------------
async function fetchCards() {
  const container = document.getElementById('cards-grid');
  try {
    let url = `/api/cards?sort_by=${AppState.selectedSort}`;
    if (AppState.selectedCategory !== 'all') {
      url += `&category=${AppState.selectedCategory}`;
    }
    if (AppState.searchQuery.trim()) {
      url += `&search=${encodeURIComponent(AppState.searchQuery.trim())}`;
    }

    const res = await fetch(url);
    const data = await res.json();
    AppState.cards = data.cards || [];
    
    document.getElementById('card-count-display').textContent = AppState.cards.length;
    renderCards(AppState.cards);
  } catch (err) {
    console.error('Error fetching cards:', err);
    container.innerHTML = `
      <div class="col-span-full py-12 text-center text-red-400">
        <i class="fa-solid fa-triangle-exclamation text-2xl mb-2"></i>
        <p>Failed to load gift cards. Please check server connection.</p>
      </div>
    `;
  }
}

function renderCards(cards) {
  const container = document.getElementById('cards-grid');
  if (!cards || cards.length === 0) {
    container.innerHTML = `
      <div class="col-span-full py-16 text-center text-slate-400 glass-panel rounded-2xl">
        <i class="fa-solid fa-magnifying-glass text-3xl text-indigo-400 mb-3"></i>
        <h3 class="text-base font-bold text-white mb-1">No gift cards matched your search</h3>
        <p class="text-xs text-slate-500">Try searching for Amazon, Steam, Netflix, Zomato, or ask GiftGenie AI!</p>
      </div>
    `;
    return;
  }

  container.innerHTML = cards.map(card => {
    const isTe = AppState.currentLang === 'te';
    const desc = isTe ? card.description_te : card.description;
    const defaultDenom = card.denominations[0];
    const discountBadge = card.discount_pct > 0 
      ? `<span class="px-2 py-0.5 rounded-full text-[10px] font-extrabold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">SAVE ${card.discount_pct}%</span>`
      : '';

    return `
      <div class="glass-panel rounded-2xl border border-white/10 hover:border-indigo-500/40 p-4 flex flex-col justify-between transition-all duration-300 group hover:-translate-y-1 hover:shadow-xl hover:shadow-indigo-500/10" data-card-id="${card.id}">
        
        <!-- Virtual Card Graphic -->
        <div class="gift-card-visual mb-4 cursor-pointer" style="background: ${card.card_gradient};" onclick="openCheckoutModal('${card.id}')">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <i class="${card.logo_icon} text-xl text-white"></i>
              <span class="font-bold text-xs tracking-wide uppercase">${card.brand}</span>
            </div>
            ${discountBadge}
          </div>

          <div class="my-3 flex items-center justify-between">
            <div class="emv-chip"></div>
            <i class="fa-solid fa-wifi contactless-wave text-white/70"></i>
          </div>

          <div class="flex items-end justify-between">
            <div>
              <div class="text-[9px] text-white/60 tracking-widest font-mono">DIGITAL VOUCHER</div>
              <div class="text-xs font-bold tracking-wider">${card.name}</div>
            </div>
            <div class="text-right">
              <span class="text-[9px] text-white/70">STARTING</span>
              <div class="text-sm font-extrabold font-mono text-emerald-300">₹${defaultDenom}</div>
            </div>
          </div>
        </div>

        <!-- Details & Features -->
        <div class="space-y-3 flex-1 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between gap-2 mb-1.5">
              <h3 class="font-bold text-sm text-white group-hover:text-indigo-400 transition-colors">${card.name}</h3>
              <div class="flex items-center gap-1 text-[11px] text-amber-400 font-semibold shrink-0">
                <i class="fa-solid fa-star text-[10px]"></i>
                <span>${card.rating}</span>
                <span class="text-slate-500 text-[10px]">(${card.total_reviews})</span>
              </div>
            </div>
            <p class="text-xs text-slate-400 line-clamp-2 leading-relaxed mb-3">${desc}</p>
          </div>

          <!-- Denomination Selector Pills -->
          <div>
            <div class="text-[10px] uppercase tracking-wider text-slate-500 font-semibold mb-1.5">Available Values</div>
            <div class="flex flex-wrap gap-1.5 mb-3">
              ${card.denominations.slice(0, 4).map((d, idx) => `
                <button 
                  class="denom-btn text-[11px] font-mono px-2 py-0.5 rounded-md bg-slate-800 hover:bg-slate-700 text-slate-300 border border-white/10 ${idx === 0 ? 'active' : ''}"
                  onclick="selectCardDenomination(this, '${card.id}', ${d})"
                >
                  ₹${d}
                </button>
              `).join('')}
              ${card.denominations.length > 4 ? `<span class="text-[10px] text-slate-500 self-center">+more</span>` : ''}
            </div>

            <!-- Quick Action Buttons -->
            <div class="flex items-center gap-2 pt-2 border-t border-white/5">
              <button 
                onclick="openCheckoutModal('${card.id}')" 
                class="flex-1 py-2 px-3 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold text-xs flex items-center justify-center gap-1.5 shadow-md shadow-indigo-600/20 transition-all"
              >
                <i class="fa-solid fa-bolt text-xs text-amber-300"></i>
                <span>${isTe ? 'ఇప్పుడే కొనండి (Quick Buy)' : 'Quick Buy'}</span>
              </button>
              <button 
                onclick="askAIAboutCard('${card.name}')" 
                class="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-indigo-400 border border-white/10 transition-colors"
                title="Ask AI about this card"
              >
                <i class="fa-solid fa-wand-magic-sparkles text-xs"></i>
              </button>
            </div>

          </div>

        </div>

      </div>
    `;
  }).join('');
}

function selectCardDenomination(btn, cardId, value) {
  const parent = btn.parentElement;
  parent.querySelectorAll('.denom-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
}

// ----------------- Category & Search Filtering -----------------
function initCategoryFilters() {
  const container = document.getElementById('category-filter-container');
  container.addEventListener('click', (e) => {
    const btn = e.target.closest('.category-pill');
    if (!btn) return;

    container.querySelectorAll('.category-pill').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    
    AppState.selectedCategory = btn.dataset.category;
    fetchCards();
  });
}

function initSortAndSearch() {
  // Sort Dropdown
  const sortSelect = document.getElementById('sort-select');
  sortSelect.addEventListener('change', (e) => {
    AppState.selectedSort = e.target.value;
    fetchCards();
  });

  // Nav Search Input
  const navInput = document.getElementById('nav-search-input');
  const clearBtn = document.getElementById('clear-search-btn');

  let searchTimeout = null;
  navInput.addEventListener('input', (e) => {
    AppState.searchQuery = e.target.value;
    clearBtn.classList.toggle('hidden', !AppState.searchQuery);

    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      fetchCards();
    }, 250);
  });

  clearBtn.addEventListener('click', () => {
    navInput.value = '';
    AppState.searchQuery = '';
    clearBtn.classList.add('hidden');
    fetchCards();
  });
}

// ----------------- AI Sales Concierge (GiftGenie AI) -----------------
function initAIChat() {
  const drawer = document.getElementById('ai-chat-drawer');
  const openBtn = document.getElementById('floating-chat-toggle-btn');
  const navOpenBtn = document.getElementById('nav-open-ai-btn');
  const closeBtn = document.getElementById('close-chat-drawer-btn');
  const chatForm = document.getElementById('chat-form');
  const chatInput = document.getElementById('chat-input');
  const heroAiInput = document.getElementById('hero-ai-input');
  const heroAiBtn = document.getElementById('hero-ai-submit-btn');
  const micBtn = document.getElementById('mic-input-btn');
  const voiceToggleBtn = document.getElementById('ai-voice-toggle-btn');

  // Toggle Drawer
  const openDrawer = () => drawer.classList.remove('hidden');
  const closeDrawer = () => drawer.classList.add('hidden');

  openBtn.addEventListener('click', openDrawer);
  navOpenBtn.addEventListener('click', openDrawer);
  closeBtn.addEventListener('click', closeDrawer);

  // Hero AI Input submission
  const handleHeroSubmit = () => {
    const text = heroAiInput.value.trim();
    if (!text) return;
    openDrawer();
    sendChatMessage(text);
    heroAiInput.value = '';
  };

  heroAiBtn.addEventListener('click', handleHeroSubmit);
  heroAiInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleHeroSubmit();
  });

  // Quick Chips in Hero and Drawer
  document.querySelectorAll('.ai-chip, .drawer-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      const prompt = chip.dataset.prompt || chip.dataset.msg;
      openDrawer();
      sendChatMessage(prompt);
    });
  });

  // Chat Form submission
  chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const text = chatInput.value.trim();
    if (!text) return;
    sendChatMessage(text);
    chatInput.value = '';
  });

  // Voice Read Aloud Toggle
  voiceToggleBtn.addEventListener('click', () => {
    AppState.voiceEnabled = !AppState.voiceEnabled;
    voiceToggleBtn.classList.toggle('text-indigo-400', AppState.voiceEnabled);
    voiceToggleBtn.classList.toggle('text-slate-500', !AppState.voiceEnabled);
  });

  // Speech Recognition (Microphone)
  if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognizer = new SpeechRecognition();
    recognizer.continuous = false;
    recognizer.interimResults = false;
    recognizer.lang = AppState.currentLang === 'te' ? 'te-IN' : 'en-US';

    recognizer.onstart = () => {
      AppState.isRecording = true;
      micBtn.classList.add('text-red-400', 'animate-pulse');
    };

    recognizer.onresult = (e) => {
      const transcript = e.results[0][0].transcript;
      chatInput.value = transcript;
      sendChatMessage(transcript);
    };

    recognizer.onerror = () => {
      AppState.isRecording = false;
      micBtn.classList.remove('text-red-400', 'animate-pulse');
    };

    recognizer.onend = () => {
      AppState.isRecording = false;
      micBtn.classList.remove('text-red-400', 'animate-pulse');
    };

    micBtn.addEventListener('click', () => {
      if (AppState.isRecording) {
        recognizer.stop();
      } else {
        recognizer.lang = AppState.currentLang === 'te' ? 'te-IN' : 'en-US';
        recognizer.start();
      }
    });
  } else {
    micBtn.title = "Speech recognition not supported in this browser";
    micBtn.disabled = true;
  }
}

async function sendChatMessage(message) {
  const container = document.getElementById('chat-messages-container');
  
  // 1. Render User Message
  const userBubble = document.createElement('div');
  userBubble.className = 'flex items-start gap-2.5 justify-end';
  userBubble.innerHTML = `
    <div class="ai-chat-bubble user">
      <p>${escapeHtml(message)}</p>
    </div>
  `;
  container.appendChild(userBubble);
  container.scrollTop = container.scrollHeight;

  // 2. Render Loading Indicator
  const loadingBubble = document.createElement('div');
  loadingBubble.className = 'flex items-start gap-2.5';
  loadingBubble.id = 'ai-loading-bubble';
  loadingBubble.innerHTML = `
    <div class="w-7 h-7 rounded-lg bg-indigo-600/80 flex items-center justify-center text-white text-xs shrink-0 mt-1">
      <i class="fa-solid fa-robot"></i>
    </div>
    <div class="ai-chat-bubble bot flex items-center gap-2">
      <i class="fa-solid fa-circle-notch fa-spin text-indigo-400 text-xs"></i>
      <span class="text-xs text-slate-400">GiftGenie is curating cards...</span>
    </div>
  `;
  container.appendChild(loadingBubble);
  container.scrollTop = container.scrollHeight;

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: message })
    });
    const data = await res.json();

    // Remove loading
    const loader = document.getElementById('ai-loading-bubble');
    if (loader) loader.remove();

    // 3. Render AI Response
    renderAIBotMessage(data);

    // Speak response if voice enabled
    if (AppState.voiceEnabled && AppState.speechSynth) {
      speakAIText(data.reply);
    }

  } catch (err) {
    console.error('Chat error:', err);
    const loader = document.getElementById('ai-loading-bubble');
    if (loader) loader.remove();

    const errBubble = document.createElement('div');
    errBubble.className = 'flex items-start gap-2.5';
    errBubble.innerHTML = `
      <div class="w-7 h-7 rounded-lg bg-red-600/80 flex items-center justify-center text-white text-xs shrink-0 mt-1">
        <i class="fa-solid fa-circle-exclamation"></i>
      </div>
      <div class="ai-chat-bubble bot text-red-300 text-xs">
        Failed to connect to AI Sales Assistant. Please try again.
      </div>
    `;
    container.appendChild(errBubble);
    container.scrollTop = container.scrollHeight;
  }
}

function renderAIBotMessage(data) {
  const container = document.getElementById('chat-messages-container');
  const botWrapper = document.createElement('div');
  botWrapper.className = 'flex items-start gap-2.5';

  let cardsHtml = '';
  if (data.cards && data.cards.length > 0) {
    cardsHtml = `
      <div class="mt-3 space-y-2">
        <div class="text-[10px] font-bold uppercase tracking-wider text-indigo-400">Recommended Gift Cards:</div>
        <div class="grid grid-cols-1 gap-2">
          ${data.cards.slice(0, 3).map(c => `
            <div class="p-2.5 rounded-xl bg-slate-900/90 border border-white/10 flex items-center justify-between gap-3 hover:border-indigo-500/50 transition-colors">
              <div class="flex items-center gap-2.5">
                <div class="w-8 h-8 rounded-lg flex items-center justify-center text-white text-sm" style="background: ${c.card_gradient}">
                  <i class="${c.logo_icon}"></i>
                </div>
                <div>
                  <div class="text-xs font-bold text-white">${c.name}</div>
                  <div class="text-[10px] text-emerald-400 font-semibold">${c.discount_pct > 0 ? `Save ${c.discount_pct}% Instant` : 'Instant Delivery'}</div>
                </div>
              </div>
              <button 
                onclick="openCheckoutModal('${c.id}')" 
                class="px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-[11px] whitespace-nowrap shadow-sm shadow-indigo-600/30"
              >
                Buy ₹${c.denominations[0]}
              </button>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }

  // Format markdown bolding in reply text
  const formattedText = escapeHtml(data.reply).replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>');

  botWrapper.innerHTML = `
    <div class="w-7 h-7 rounded-lg bg-indigo-600/80 flex items-center justify-center text-white text-xs shrink-0 mt-1">
      <i class="fa-solid fa-robot"></i>
    </div>
    <div class="ai-chat-bubble bot">
      <div class="text-xs text-slate-200 leading-relaxed">${formattedText}</div>
      ${cardsHtml}
    </div>
  `;

  container.appendChild(botWrapper);
  container.scrollTop = container.scrollHeight;
}

function speakAIText(text) {
  if (!AppState.speechSynth) return;
  // Cancel previous speech
  AppState.speechSynth.cancel();
  
  // Clean markdown asterisks
  const clean = text.replace(/[*_#]/g, '');
  const utterance = new SpeechSynthesisUtterance(clean);
  utterance.rate = 1.0;
  AppState.speechSynth.speak(utterance);
}

function askAIAboutCard(cardName) {
  const drawer = document.getElementById('ai-chat-drawer');
  drawer.classList.remove('hidden');
  const prompt = AppState.currentLang === 'te' 
    ? `${cardName} గిఫ్ట్ కార్డ్ గురించి వివరాలు మరియు బెస్ట్ ఆఫర్ ఏమిటి?`
    : `Tell me more about ${cardName} and what denomination is best to gift?`;
  sendChatMessage(prompt);
}

// ----------------- Checkout & Payment Flow -----------------
function initCheckoutFlow() {
  const modal = document.getElementById('checkout-modal');
  const closeBtn = document.getElementById('close-checkout-btn');
  const couponBtn = document.getElementById('apply-coupon-btn');
  const confirmPayBtn = document.getElementById('confirm-pay-btn');
  const aiWishBtn = document.getElementById('btn-generate-ai-wish');

  closeBtn.addEventListener('click', () => modal.classList.add('hidden'));

  // Toggle gifting fields
  document.querySelectorAll('input[name="gift-target"]').forEach(radio => {
    radio.addEventListener('change', (e) => {
      const extra = document.getElementById('gift-extra-fields');
      extra.classList.toggle('hidden', e.target.value !== 'gift');
    });
  });

  // Apply Coupon Code
  couponBtn.addEventListener('click', applyCouponCode);

  // Copy UPI ID button
  const copyUpiBtn = document.getElementById('copy-upi-btn');
  if (copyUpiBtn) {
    copyUpiBtn.addEventListener('click', () => {
      navigator.clipboard.writeText('9059382131-2@ybl');
      copyUpiBtn.innerHTML = '<i class="fa-solid fa-check"></i> Copied!';
      setTimeout(() => { copyUpiBtn.innerHTML = '<i class="fa-solid fa-copy mr-1"></i> Copy'; }, 2000);
    });
  }

  // Payment method change toggle
  document.querySelectorAll('input[name="payment-method"]').forEach(radio => {
    radio.addEventListener('change', (e) => {
      const upiSection = document.getElementById('upi-qr-section');
      if (upiSection) upiSection.classList.toggle('hidden', e.target.value !== 'UPI');
    });
  });

  // AI Wish Generator
  aiWishBtn.addEventListener('click', async () => {
    const recName = document.getElementById('rec-name').value.trim() || 'My Dear';
    const recMessage = document.getElementById('rec-message');
    aiWishBtn.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin"></i> Writing...`;

    try {
      const res = await fetch('/api/generate-message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          recipient: recName,
          occasion: 'Birthday',
          lang: AppState.currentLang
        })
      });
      const data = await res.json();
      recMessage.value = data.message;
    } catch (err) {
      console.error(err);
    } finally {
      aiWishBtn.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> <span>Generate AI Wish</span>`;
    }
  });

  // Confirm and Execute Payment
  confirmPayBtn.addEventListener('click', executeOrderCheckout);
}

function openCheckoutModal(cardId) {
  const card = AppState.cards.find(c => c.id === cardId);
  if (!card) return;

  AppState.activeCardForCheckout = card;
  AppState.selectedDenomination = card.denominations[0];
  AppState.appliedCoupon = null;

  const modal = document.getElementById('checkout-modal');
  document.getElementById('checkout-card-name').textContent = card.name;
  document.getElementById('checkout-card-brand').textContent = `${card.brand} • Instant E-Delivery`;
  document.getElementById('checkout-card-icon').innerHTML = `<i class="${card.logo_icon}"></i>`;
  document.getElementById('coupon-input').value = '';
  document.getElementById('coupon-feedback').classList.add('hidden');
  document.getElementById('summary-coupon-row').classList.add('hidden');

  // Render Denomination Selector
  const denomContainer = document.getElementById('checkout-denom-pills');
  denomContainer.innerHTML = card.denominations.map((d, idx) => `
    <button 
      type="button" 
      class="denom-pill px-3 py-1.5 rounded-xl border border-white/10 text-xs font-mono font-bold ${idx === 0 ? 'bg-indigo-600 text-white border-indigo-500' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'}"
      onclick="setCheckoutDenomination(${d}, this)"
    >
      ₹${d}
    </button>
  `).join('');

  updateCheckoutSummary();
  modal.classList.remove('hidden');
}

function setCheckoutDenomination(value, btn) {
  AppState.selectedDenomination = value;
  const parent = btn.parentElement;
  parent.querySelectorAll('.denom-pill').forEach(b => {
    b.classList.remove('bg-indigo-600', 'text-white', 'border-indigo-500');
    b.classList.add('bg-slate-800', 'text-slate-300');
  });
  btn.classList.add('bg-indigo-600', 'text-white', 'border-indigo-500');
  btn.classList.remove('bg-slate-800', 'text-slate-300');

  // Re-validate coupon if present
  if (AppState.appliedCoupon) {
    applyCouponCode();
  } else {
    updateCheckoutSummary();
  }
}

async function applyCouponCode() {
  const code = document.getElementById('coupon-input').value.trim().toUpperCase();
  const feedback = document.getElementById('coupon-feedback');
  if (!code) return;

  try {
    const res = await fetch('/api/coupon/validate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        coupon_code: code,
        subtotal: AppState.selectedDenomination
      })
    });
    const data = await res.json();

    feedback.classList.remove('hidden');
    if (data.valid) {
      AppState.appliedCoupon = data;
      feedback.className = 'text-xs text-emerald-400 font-semibold';
      feedback.textContent = `✓ ${data.message}`;
    } else {
      AppState.appliedCoupon = null;
      feedback.className = 'text-xs text-red-400 font-semibold';
      feedback.textContent = `✗ ${data.message}`;
    }
    updateCheckoutSummary();
  } catch (err) {
    console.error(err);
  }
}

function updateCheckoutSummary() {
  const card = AppState.activeCardForCheckout;
  if (!card) return;

  const denom = AppState.selectedDenomination;
  const brandDiscAmount = denom * (card.discount_pct / 100.0);
  let couponDiscAmount = 0;

  if (AppState.appliedCoupon && AppState.appliedCoupon.valid) {
    couponDiscAmount = AppState.appliedCoupon.discount_amount;
    document.getElementById('summary-coupon-row').classList.remove('hidden');
    document.getElementById('summary-coupon-disc').textContent = `- ₹${couponDiscAmount.toFixed(2)}`;
  } else {
    document.getElementById('summary-coupon-row').classList.add('hidden');
  }

  const finalPrice = Math.max(1, denom - brandDiscAmount - couponDiscAmount);

  document.getElementById('summary-card-val').textContent = `₹${denom.toLocaleString('en-IN')}.00`;
  document.getElementById('summary-brand-disc').textContent = `- ₹${brandDiscAmount.toFixed(2)} (${card.discount_pct}%)`;
  document.getElementById('summary-final-price').textContent = `₹${finalPrice.toFixed(2)}`;
  document.getElementById('btn-pay-now-text').textContent = `Pay ₹${finalPrice.toFixed(2)} & Deliver 16-Digit Voucher`;

  // Update Dynamic Live UPI QR Code with Real Merchant UPI ID
  const merchantUpiId = '9059382131-2@ybl';
  const merchantName = 'GiftCraft Store';
  const upiLink = `upi://pay?pa=${encodeURIComponent(merchantUpiId)}&pn=${encodeURIComponent(merchantName)}&am=${finalPrice.toFixed(2)}&cu=INR&tn=${encodeURIComponent('GiftCard ' + card.name)}`;
  const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=${encodeURIComponent(upiLink)}`;

  const upiImg = document.getElementById('dynamic-upi-qr-img');
  if (upiImg) upiImg.src = qrUrl;

  const upiLinkBtn = document.getElementById('direct-upi-intent-link');
  if (upiLinkBtn) upiLinkBtn.href = upiLink;

  const upiAmtDisplay = document.getElementById('upi-amount-display');
  if (upiAmtDisplay) upiAmtDisplay.textContent = `₹${finalPrice.toFixed(2)}`;
}

async function executeOrderCheckout() {
  const card = AppState.activeCardForCheckout;
  if (!card) return;

  const payBtn = document.getElementById('confirm-pay-btn');
  const custName = document.getElementById('cust-name').value.trim() || 'Ravi Kumar';
  const custEmail = document.getElementById('cust-email').value.trim() || 'ravi.kumar@example.com';
  const giftTarget = document.querySelector('input[name="gift-target"]:checked').value;
  const recName = giftTarget === 'gift' ? document.getElementById('rec-name').value.trim() : custName;
  const recEmail = giftTarget === 'gift' ? document.getElementById('rec-email').value.trim() : custEmail;
  const giftMessage = giftTarget === 'gift' ? document.getElementById('rec-message').value.trim() : '';
  const payMethod = document.querySelector('input[name="payment-method"]:checked').value;

  payBtn.disabled = true;
  payBtn.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin"></i> Processing Secure Payment & Generating Code...`;

  try {
    const res = await fetch('/api/checkout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        card_id: card.id,
        denomination: AppState.selectedDenomination,
        customer_name: custName,
        customer_email: custEmail,
        recipient_name: recName,
        recipient_email: recEmail,
        gift_message: giftMessage,
        occasion: 'General',
        payment_method: payMethod,
        coupon_code: AppState.appliedCoupon ? AppState.appliedCoupon.code : null,
        upi_utr_ref: document.getElementById('upi-utr-input') ? document.getElementById('upi-utr-input').value.trim() : null
      })
    });

    const data = await res.json();
    if (!data.success) {
      alert(data.message || 'Payment processing failed');
      return;
    }

    // Close checkout modal
    document.getElementById('checkout-modal').classList.add('hidden');

    // Open Scratch & Delivery Modal
    openVoucherRevealModal(data.order);
    fetchRecentOrders();

  } catch (err) {
    console.error('Checkout error:', err);
    alert('Something went wrong during checkout. Please try again.');
  } finally {
    payBtn.disabled = false;
    updateCheckoutSummary();
  }
}

// ----------------- Scratch Card Canvas & Delivery Modal -----------------
function openVoucherRevealModal(order) {
  const modal = document.getElementById('voucher-modal');
  
  // Set details
  document.getElementById('voucher-card-title').textContent = order.card_name;
  document.getElementById('voucher-brand-icon').className = order.logo_icon;
  document.getElementById('voucher-denom-badge').textContent = `₹${order.denomination.toLocaleString('en-IN')}`;
  document.getElementById('voucher-order-id').textContent = order.order_id;
  document.getElementById('revealed-code').textContent = order.voucher_code;
  document.getElementById('revealed-pin').textContent = order.voucher_pin;
  document.getElementById('voucher-redemption-text').textContent = order.redemption_guide;
  document.getElementById('voucher-card-display').style.background = order.card_gradient;

  // Initialize Scratch Canvas
  initScratchCanvas();

  // Instant Reveal button
  document.getElementById('quick-reveal-btn').onclick = () => {
    const canvas = document.getElementById('scratch-canvas');
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  };

  // Copy Code button
  document.getElementById('copy-voucher-btn').onclick = () => {
    navigator.clipboard.writeText(`${order.voucher_code} (PIN: ${order.voucher_pin})`);
    const txt = document.getElementById('btn-copy-code-text');
    txt.textContent = 'Copied!';
    setTimeout(() => { txt.textContent = 'Copy Code'; }, 2000);
  };

  // Print Voucher button
  document.getElementById('print-voucher-btn').onclick = () => {
    window.print();
  };

  document.getElementById('close-voucher-modal-btn').onclick = () => {
    modal.classList.add('hidden');
  };

  modal.classList.remove('hidden');
}

function initScratchCanvas() {
  const canvas = document.getElementById('scratch-canvas');
  const box = document.getElementById('scratch-box');
  
  canvas.width = box.clientWidth || 360;
  canvas.height = box.clientHeight || 140;

  const ctx = canvas.getContext('2d');

  // Fill scratch metallic layer
  const grad = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
  grad.addColorStop(0, '#64748b');
  grad.addColorStop(0.5, '#94a3b8');
  grad.addColorStop(1, '#475569');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Scratch instructions overlay text
  ctx.fillStyle = '#ffffff';
  ctx.font = 'bold 14px Outfit, sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('✨ SCRATCH HERE TO REVEAL CODE ✨', canvas.width / 2, canvas.height / 2);

  // Scratch Interaction
  let isScratching = false;

  function scratch(e) {
    if (!isScratching) return;
    const rect = canvas.getBoundingClientRect();
    const x = (e.clientX || (e.touches && e.touches[0].clientX)) - rect.left;
    const y = (e.clientY || (e.touches && e.touches[0].clientY)) - rect.top;

    ctx.globalCompositeOperation = 'destination-out';
    ctx.beginPath();
    ctx.arc(x, y, 22, 0, Math.PI * 2, false);
    ctx.fill();
  }

  canvas.addEventListener('mousedown', () => isScratching = true);
  window.addEventListener('mouseup', () => isScratching = false);
  canvas.addEventListener('mousemove', scratch);

  canvas.addEventListener('touchstart', () => isScratching = true);
  window.addEventListener('touchend', () => isScratching = false);
  canvas.addEventListener('touchmove', scratch);
}

// ----------------- Other Modals: Balance & Admin -----------------
function initModals() {
  // Balance Modal
  const balModal = document.getElementById('balance-modal');
  const openBalBtn = document.getElementById('open-balance-modal-btn');
  const closeBalBtn = document.getElementById('close-balance-modal-btn');
  const submitBalBtn = document.getElementById('submit-balance-btn');

  openBalBtn.addEventListener('click', () => balModal.classList.remove('hidden'));
  closeBalBtn.addEventListener('click', () => balModal.classList.add('hidden'));

  submitBalBtn.addEventListener('click', async () => {
    const code = document.getElementById('balance-input').value.trim();
    const resultBox = document.getElementById('balance-result');
    if (!code) return;

    submitBalBtn.textContent = 'Verifying...';
    try {
      const res = await fetch('/api/check-balance', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ voucher_code: code })
      });
      const data = await res.json();
      resultBox.classList.remove('hidden');

      if (data.found) {
        resultBox.innerHTML = `
          <div class="text-emerald-400 font-bold mb-1">✓ Card Active & Valid</div>
          <div>Brand: <strong class="text-white">${data.brand} (${data.card_name})</strong></div>
          <div>Available Balance: <strong class="text-emerald-300 font-mono">₹${data.balance.toLocaleString('en-IN')}</strong></div>
          <div>Validity: <span class="text-slate-400">${data.expiry}</span></div>
        `;
      } else {
        resultBox.innerHTML = `
          <div class="text-red-400 font-bold mb-1">✗ Verification Failed</div>
          <p class="text-slate-400">${data.message}</p>
        `;
      }
    } catch (err) {
      console.error(err);
    } finally {
      submitBalBtn.textContent = 'Verify Balance';
    }
  });

  // Admin Modal
  const adminModal = document.getElementById('admin-modal');
  const openAdminBtn = document.getElementById('open-admin-modal-btn');
  const closeAdminBtn = document.getElementById('close-admin-modal-btn');
  const tabAnalyticsBtn = document.getElementById('admin-tab-analytics-btn');
  const tabPayoutBtn = document.getElementById('admin-tab-payout-btn');
  const viewAnalytics = document.getElementById('admin-view-analytics');
  const viewPayout = document.getElementById('admin-view-payout');
  const bankForm = document.getElementById('merchant-bank-form');

  // Tab switching inside Admin Modal
  tabAnalyticsBtn.addEventListener('click', () => {
    tabAnalyticsBtn.className = 'px-4 py-2 rounded-xl text-xs font-bold bg-indigo-600 text-white flex items-center gap-2';
    tabPayoutBtn.className = 'px-4 py-2 rounded-xl text-xs font-bold bg-slate-800 text-slate-300 hover:text-white flex items-center gap-2 border border-white/10';
    viewAnalytics.classList.remove('hidden');
    viewPayout.classList.add('hidden');
  });

  tabPayoutBtn.addEventListener('click', () => {
    tabPayoutBtn.className = 'px-4 py-2 rounded-xl text-xs font-bold bg-indigo-600 text-white flex items-center gap-2';
    tabAnalyticsBtn.className = 'px-4 py-2 rounded-xl text-xs font-bold bg-slate-800 text-slate-300 hover:text-white flex items-center gap-2 border border-white/10';
    viewPayout.classList.remove('hidden');
    viewAnalytics.classList.add('hidden');
    loadMerchantPayoutData();
  });

  // Save Merchant Bank Details
  bankForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const saveBtn = document.getElementById('save-bank-btn');
    saveBtn.textContent = 'Saving Details...';

    const payload = {
      merchant_name: document.getElementById('m-name').value.trim(),
      bank_name: document.getElementById('m-bank').value.trim(),
      account_number: document.getElementById('m-account').value.trim(),
      ifsc_code: document.getElementById('m-ifsc').value.trim(),
      merchant_upi_id: document.getElementById('m-upi').value.trim(),
      active_gateway: document.getElementById('m-gateway').value
    };

    try {
      const res = await fetch('/api/admin/payout-settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      alert('✓ ' + data.message);
    } catch (err) {
      console.error(err);
      alert('Failed to save bank settings.');
    } finally {
      saveBtn.textContent = 'Save & Update Bank Account';
    }
  });

  async function loadMerchantPayoutData() {
    try {
      const res = await fetch('/api/admin/payout-settings');
      const data = await res.json();
      const s = data.settings || {};

      document.getElementById('m-name').value = s.merchant_name || '';
      document.getElementById('m-bank').value = s.bank_name || '';
      document.getElementById('m-account').value = s.account_number || '';
      document.getElementById('m-ifsc').value = s.ifsc_code || '';
      document.getElementById('m-upi').value = s.merchant_upi_id || '';
      document.getElementById('m-gateway').value = s.active_gateway || 'Razorpay';

      const settlList = document.getElementById('adm-settlements-list');
      settlList.innerHTML = (data.settlements || []).map(st => `
        <div class="p-3 rounded-xl bg-slate-900 border border-white/5 flex items-center justify-between text-xs">
          <div>
            <div class="font-bold text-white flex items-center gap-2">
              <span class="text-emerald-400 font-mono">₹${st.amount.toLocaleString('en-IN')}</span>
              <span class="px-1.5 py-0.5 rounded text-[9px] bg-emerald-500/20 text-emerald-300 font-semibold">${st.status}</span>
            </div>
            <div class="text-[11px] text-slate-400">Deposited to: ${st.bank_account} • UTR: <span class="font-mono text-slate-300">${st.utr_ref}</span></div>
          </div>
          <div class="text-[10px] text-slate-500 text-right whitespace-nowrap">${st.settled_at}</div>
        </div>
      `).join('');

    } catch (err) {
      console.error('Error loading payout data:', err);
    }
  }

  openAdminBtn.addEventListener('click', async () => {
    adminModal.classList.remove('hidden');
    try {
      const res = await fetch('/api/admin/stats');
      const data = await res.json();

      document.getElementById('adm-revenue').textContent = `₹${data.total_revenue.toLocaleString('en-IN')}`;
      document.getElementById('adm-orders').textContent = data.total_orders;
      document.getElementById('adm-savings').textContent = `₹${data.total_savings.toLocaleString('en-IN')}`;
      document.getElementById('adm-cards').textContent = data.total_cards;

      const sellersBox = document.getElementById('adm-top-sellers');
      sellersBox.innerHTML = data.top_sellers.map((s, idx) => `
        <div class="flex items-center justify-between p-2.5 rounded-xl bg-slate-900 border border-white/5 text-xs">
          <div class="flex items-center gap-2">
            <span class="w-5 h-5 rounded-full bg-slate-800 text-slate-300 flex items-center justify-center font-bold text-[10px]">${idx + 1}</span>
            <span class="font-semibold text-white">${s.name}</span>
          </div>
          <div class="flex items-center gap-4">
            <span class="text-indigo-400 font-mono">${s.sales_count} sales</span>
            <span class="text-emerald-400 font-mono">${s.discount_pct}% off</span>
          </div>
        </div>
      `).join('');

    } catch (err) {
      console.error(err);
    }
  });

  closeAdminBtn.addEventListener('click', () => adminModal.classList.add('hidden'));
}

// ----------------- Live Purchases Feed -----------------
async function fetchRecentOrders() {
  try {
    const res = await fetch('/api/recent-orders');
    const orders = await res.json();
    if (!orders || orders.length === 0) return;

    const ticker = document.getElementById('ticker-content');
    ticker.innerHTML = orders.map(o => `
      <span>🎁 ${escapeHtml(o.customer_name)} bought <strong>${escapeHtml(o.card_name)} ₹${o.denomination}</strong> (Saved ₹${o.discount_amount})</span>
    `).join(' • ');

  } catch (err) {
    console.error('Ticker error:', err);
  }
}

// Utility: escape HTML
function escapeHtml(text) {
  if (!text) return '';
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}
