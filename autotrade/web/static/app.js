const $ = s => document.querySelector(s);
const $$ = s => document.querySelectorAll(s);

function applyTheme() {
  const th = localStorage.getItem('theme');
  if (th === 'dark') {
    document.documentElement.classList.add('dark');
    $('#iconSun').classList.remove('hidden');
    $('#iconMoon').classList.add('hidden');
  } else {
    document.documentElement.classList.remove('dark');
    $('#iconSun').classList.add('hidden');
    $('#iconMoon').classList.remove('hidden');
  }
}

applyTheme();
$('#themeToggle')?.addEventListener('click', () => {
  const dark = !document.documentElement.classList.contains('dark');
  localStorage.setItem('theme', dark ? 'dark' : 'light');
  applyTheme();
});

async function updateTicker() {
  try {
    const data = await fetch('/prices?syms=NVDA,AAPL,MSFT,TSLA').then(r=>r.json());
    const parts = [];
    for (const [s,p] of Object.entries(data)) parts.push(`${s} ${p.toFixed(2)}`);
    $('#ticker').textContent = parts.join('  ');
  } catch(err){console.error(err);}
}
setInterval(updateTicker,60000);
updateTicker();

$('#capRange')?.addEventListener('input',e=>{
  $('#capValue').textContent = e.target.value;
});

function selectOne(container){
  const buttons = $$(container+' .pill');
  buttons.forEach(b=>b.addEventListener('click',()=>{
    buttons.forEach(x=>x.classList.remove('selected'));
    b.classList.add('selected');
  }));
}
selectOne('#riskGroup');
selectOne('#levGroup');

$$('#indicators .pill').forEach(b=>{
  b.addEventListener('click',()=>b.classList.toggle('selected'));
});

$('#analyzeBtn')?.addEventListener('click',async()=>{
  const capital = +$('#capRange').value;
  const risk = $('#riskGroup .selected')?.dataset.val;
  const lev = +$('#levGroup .selected')?.dataset.val;
  const inds = Array.from($('#indicators .selected')).map(b=>b.textContent);
  const body = JSON.stringify({capital,risk,lev,inds});
  const res = await fetch('/analyze',{method:'POST',headers:{'Content-Type':'application/json'},body});
  const data = await res.json();
  $('#aiBrief').textContent = data.summary;
});

document.body.addEventListener('click',e=>{
  if(e.target.classList.contains('close-pos')){
    const sym = e.target.dataset.sym;
    fetch('/trade/close',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({symbol:sym})}).then(()=>{
      e.target.closest('tr').remove();
    });
  }
});

const av = localStorage.getItem('avatar');
if(av) $('#avatarImg')?.setAttribute('src',av);
$('#avatar')?.addEventListener('change',ev=>{
  const f = ev.target.files[0]; if(!f) return;
  const fr = new FileReader();
  fr.onload=()=>{ localStorage.setItem('avatar',fr.result); $('#avatarImg').src=fr.result; };
  fr.readAsDataURL(f);
});
const nick = localStorage.getItem('nick');
if(nick) $('#nickname').textContent=nick;
$('#nickname')?.addEventListener('input',()=>{
  localStorage.setItem('nick',$('#nickname').textContent);
});
async function loadSummary(){
  const d = await fetch('/hourly_summary').then(r=>r.json());
  if(d.summary) $('#aiBrief').textContent = d.summary;
}
loadSummary();

const $ = sel => document.querySelector(sel);
const $$ = sel => document.querySelectorAll(sel);
const api = p => fetch(p).then(r => r.json());

$('#capRange')?.addEventListener('input', e =>
  $('#capOut').textContent = `${e.target.value} $`);

$$('#indicators .pill').forEach(btn =>
  btn.addEventListener('click', () => btn.classList.toggle('active')));

$('#analyzeBtn')?.addEventListener('click', () =>
  alert('TODO POST /analyze'));

async function refresh() {
  const data = await api('/prices?syms=NVDA,AAPL,MSFT,TSLA');
  if ($('#gpt-status'))
    $('#gpt-status').textContent = `NVDA=${data.NVDA}$ …`;
}
setInterval(refresh, 30000);
refresh();

const toggle = () => document.documentElement.classList.toggle('dark');
$('#themeToggle')?.addEventListener('click', toggle);

document.addEventListener('DOMContentLoaded', () => {
  const priceBox = document.getElementById('price-box');
  const briefBox = document.getElementById('brief-box');
  const capital = document.getElementById('capital');
  const capitalValue = document.getElementById('capital-value');
  const themeToggle = document.getElementById('theme-toggle');

  function loadPrices() {
    fetch('/prices?syms=NVDA,AAPL,MSFT,TSLA')
      .then(r => r.json())
      .then(d => {
        if (priceBox) priceBox.textContent = JSON.stringify(d, null, 2);
      });
  }

  function loadBrief() {
    fetch('/hourly_summary')
      .then(r => r.json())
      .then(d => {
        if (briefBox) briefBox.textContent = d.summary;
      });
  }

  if (capital) {
    capital.addEventListener('input', () => {
      capitalValue.textContent = capital.value;
    });
  }

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      document.documentElement.classList.toggle('dark');
    });
  }

  loadPrices();
  loadBrief();
});
