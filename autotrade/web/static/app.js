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
