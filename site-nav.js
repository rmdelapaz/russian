/* site-nav.js — Injects site header, dark mode toggle, content-wrap, and quiz interactivity.
   Prev/Next nav and site footer live as static HTML in each lesson (managed by add_footer_nav.py). */
(function () {
  'use strict';

  /* ---- Dark mode ---- */
  const saved = localStorage.getItem('theme');
  if (saved) {
    document.documentElement.setAttribute('data-theme', saved);
  } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
    document.documentElement.setAttribute('data-theme', 'dark');
  }

  function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    updateIcon();
  }

  function currentTheme() {
    return document.documentElement.getAttribute('data-theme') || 'light';
  }

  function updateIcon() {
    const el = document.querySelector('.theme-icon');
    if (el) el.textContent = currentTheme() === 'dark' ? '☀️' : '🌙';
  }

  /* ---- Build header ---- */
  const header = document.createElement('header');
  header.className = 'site-header';
  header.innerHTML = `
    <a href="/index.html" class="site-brand">🇷🇺 Russian Course</a>
    <nav class="nav-links">
      <a href="/index.html">Lessons</a>
      <a href="https://rays-home.netlify.app/" target="_blank" rel="noopener">Ray's House of Fun</a>
      <a href="https://rays-home.netlify.app/contact" target="_blank" rel="noopener">Contact</a>
      <label class="theme-toggle-label">
        <span class="theme-icon icon">${currentTheme() === 'dark' ? '☀️' : '🌙'}</span>
        <button class="theme-toggle" aria-label="Toggle dark mode"></button>
      </label>
    </nav>
  `;
  document.body.prepend(header);

  header.querySelector('.theme-toggle').addEventListener('click', toggleTheme);

  /* ---- Wrap existing content ---- */
  const isIndex = /index\.html$/i.test(location.pathname) || location.pathname.endsWith('/');
  if (!isIndex) {
    const existing = Array.from(document.body.children).filter(el => el !== header);
    const wrap = document.createElement('div');
    wrap.className = 'content-wrap';
    existing.forEach(el => wrap.appendChild(el));
    document.body.appendChild(wrap);
  }

  /* ---- Prev/Next nav and site footer are now static in each lesson's HTML
         (managed by add_footer_nav.py). Do not inject them here. ---- */

  /* ---- Quiz interactivity ---- */
  document.querySelectorAll('.quiz-question').forEach(q => {
    const options = q.querySelectorAll('.quiz-option');
    const feedback = q.querySelector('.quiz-feedback');
    options.forEach(opt => {
      opt.addEventListener('click', () => {
        options.forEach(o => o.classList.remove('selected', 'correct', 'incorrect'));
        opt.classList.add('selected');
        const ok = opt.dataset.correct === 'true';
        opt.classList.add(ok ? 'correct' : 'incorrect');
        if (feedback) {
          feedback.textContent = ok ? ('Correct! ' + (opt.dataset.explanation || '')) : ('Not quite. ' + (opt.dataset.hint || ''));
          feedback.className = 'quiz-feedback ' + (ok ? 'correct' : 'incorrect');
        }
      });
    });
  });
})();
