bd5l08-codex/set-up-demo-auto-trade-application
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
main
