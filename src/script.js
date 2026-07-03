const chatWindow = document.getElementById('chat-window');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const loading = document.getElementById('loading');

const API_KEY = window.GEMINI_API_KEY || localStorage.getItem('GEMINI_API_KEY') || '';
const BACKEND_URL = '/api/exec';   // Relatif, aman dari CORS

// ---------- Matrix Effect ----------
const canvas = document.getElementById('matrix-bg');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
const letters = '01 БИН АГЕНТ КВАНТУМ'.split('');
const fontSize = 14;
const columns = Math.floor(canvas.width / fontSize);
const drops = Array(columns).fill(1);
function drawMatrix() {
  ctx.fillStyle = 'rgba(10, 10, 10, 0.05)';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = '#00ffcc';
  ctx.font = fontSize + 'px "Share Tech Mono", monospace';
  for (let i = 0; i < drops.length; i++) {
    const text = letters[Math.floor(Math.random() * letters.length)];
    ctx.fillText(text, i * fontSize, drops[i] * fontSize);
    if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
    drops[i]++;
  }
}
setInterval(drawMatrix, 33);

// ---------- Chat Functions ----------
function addMessage(text, sender) {
  const msgDiv = document.createElement('div');
  msgDiv.className = `message ${sender}`;
  const avatar = document.createElement('div');
  avatar.className = `avatar ${sender}-avatar`;
  avatar.textContent = sender === 'user' ? '💀' : '⚡';
  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = text;
  msgDiv.appendChild(avatar);
  msgDiv.appendChild(bubble);
  chatWindow.appendChild(msgDiv);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

async function sendToGemini(prompt) {
  const url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent';
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-goog-api-key': API_KEY },
    body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] })
  });
  const data = await response.json();
  if (data.candidates?.[0]?.content?.parts?.[0]?.text) {
    return data.candidates[0].content.parts[0].text;
  } else {
    throw new Error('Respons kosong.');
  }
}

async function executeToolCommand(tool, target, options = '') {
  const response = await fetch(BACKEND_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ tool, target, options })
  });
  const data = await response.json();
  return data.result || 'Tidak ada output.';
}

// Command info (termasuk track)
const COMMANDS_INFO = {
  recon: 'Auto recon (nmap + AI analisis)',
  vulnscan: 'Vulnerability scan + searchsploit + AI saran',
  exploit: 'Metasploit exploit (jika msfconsole ada)',
  hydrabrute: 'Bruteforce service (hydra)',
  osint: 'OSINT email/username (holehe + sherlock)',
  searchsploit: 'Cari exploit di database',
  socialeng: 'Generate skenario phishing AI',
  track: '🛰️ Lacak nomor HP/email/username + satelit maps'
};

// ---------- Send Handler ----------
async function handleSend() {
  const text = userInput.value.trim();
  if (!text) return;
  addMessage(text, 'user');
  userInput.value = '';
  loading.style.display = 'block';

  try {
    if (text.startsWith('/')) {
      const parts = text.slice(1).split(' ');
      const tool = parts[0].toLowerCase();
      const target = parts[1] || '';
      const options = parts.slice(2).join(' ');
      if (tool === 'help') {
        let helpText = '📜 DAFTAR SENJATA:\n';
        for (let cmd in COMMANDS_INFO) {
          helpText += `/${cmd} - ${COMMANDS_INFO[cmd]}\n`;
        }
        helpText += '\nContoh: /recon scanme.nmap.org';
        addMessage(helpText, 'bot');
      } else {
        const result = await executeToolCommand(tool, target, options);
        addMessage(result, 'bot');
      }
    } else {
      const reply = await sendToGemini(text);
      addMessage(reply, 'bot');
    }
  } catch (err) {
    addMessage('⚠️ Error: ' + err.message, 'bot');
  } finally {
    loading.style.display = 'none';
  }
}

// Event listeners
sendBtn.addEventListener('click', handleSend);
userInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') handleSend();
});

// Welcome message
window.addEventListener('DOMContentLoaded', () => {
  addMessage('🔥 BIN AI OFFENSIVE SUITE SIAP. KETIK /help UNTUK DAFTAR COMMAND.', 'bot');
});
