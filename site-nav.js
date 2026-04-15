/* site-nav.js — Injects site header, dark mode toggle, prev/next nav, quiz interactivity, progress tracking */
(function () {
  'use strict';

  /* ---- Lesson order ---- */
  const lessons = [
    { file: 'russian_cyrillic_alphabet.html',          title: 'The Cyrillic Alphabet' },
    { file: 'russian_pronunciation_stress.html',       title: 'Pronunciation & Stress' },
    { file: 'russian_reading_writing.html',            title: 'Reading & Writing Practice' },
    { file: 'russian_greetings_essentials.html',       title: 'Greetings & Essentials' },
    { file: 'russian_numbers_time_dates.html',         title: 'Numbers, Time & Dates' },
    { file: 'russian_family_descriptions.html',        title: 'Family & Descriptions' },
    { file: 'russian_food_dining.html',                title: 'Food & Dining' },
    { file: 'russian_shopping_money.html',             title: 'Shopping & Money' },
    { file: 'russian_directions_transportation.html',  title: 'Directions & Transport' },
    { file: 'russian_health_body.html',                title: 'Health & Body' },
    { file: 'russian_hobbies_daily_life.html',         title: 'Hobbies & Daily Life' },
    { file: 'russian_work_education.html',             title: 'Work & Education' },
    { file: 'russian_technology_communication.html',   title: 'Technology & Communication' },
    { file: 'russian_weather_seasons.html',            title: 'Weather & Seasons' },
    { file: 'russian_emotions_relationships.html',     title: 'Emotions & Relationships' },
    { file: 'russian_travel_culture.html',             title: 'Travel & Russian Culture' },
  ];

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

  /* ---- Progress tracking ---- */
  const PROGRESS_KEY = 'russian-visited';

  function getVisited() {
    try { return JSON.parse(localStorage.getItem(PROGRESS_KEY)) || []; }
    catch { return []; }
  }

  function markVisited(file) {
    const visited = getVisited();
    if (!visited.includes(file)) {
      visited.push(file);
      localStorage.setItem(PROGRESS_KEY, JSON.stringify(visited));
    }
  }

  function updateProgressBar() {
    const bar = document.getElementById('progressBar');
    if (!bar) return;
    const visited = getVisited();
    const count = visited.length;
    const pct = Math.round((count / lessons.length) * 100);
    bar.textContent = `${count} / ${lessons.length}`;
    bar.style.width = Math.max(pct, count > 0 ? 8 : 0) + '%';
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

  /* ---- Mark current lesson as visited ---- */
  if (!isIndex) {
    const currentFile = location.pathname.split('/').pop();
    markVisited(currentFile);
  }

  /* ---- Prev / Next nav (lesson pages only) ---- */
  if (!isIndex) {
    const currentFile = location.pathname.split('/').pop();
    const idx = lessons.findIndex(l => l.file === currentFile);

    if (idx !== -1) {
      const nav = document.createElement('nav');
      nav.className = 'lesson-nav';

      if (idx > 0) {
        const prev = lessons[idx - 1];
        nav.innerHTML += `<a href="${prev.file}">← ${prev.title}</a>`;
      } else {
        nav.innerHTML += '<span class="spacer"></span>';
      }

      nav.innerHTML += `<a href="/index.html" style="background:var(--card-bg);color:var(--primary-color);border:1px solid var(--border-color);">All Lessons</a>`;

      if (idx < lessons.length - 1) {
        const next = lessons[idx + 1];
        nav.innerHTML += `<a href="${next.file}">${next.title} →</a>`;
      } else {
        nav.innerHTML += '<span class="spacer"></span>';
      }

      const wrap = document.querySelector('.content-wrap') || document.body;
      wrap.appendChild(nav);
    }
  }

  /* ---- Update progress on index ---- */
  if (isIndex) updateProgressBar();

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

  /* ---- Site footer ---- */
  const footer = document.createElement('footer');
  footer.className = 'site-footer';
  footer.innerHTML = `
    <p>© ${new Date().getFullYear()} <a href="https://rays-home.netlify.app/" target="_blank" rel="noopener">Ray's House of Fun</a> · 
    <a href="https://rays-home.netlify.app/contact" target="_blank" rel="noopener">Contact</a></p>
  `;
  document.body.appendChild(footer);
})();
