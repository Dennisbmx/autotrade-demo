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
