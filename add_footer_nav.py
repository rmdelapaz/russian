#!/usr/bin/env python3
"""
add_footer_nav.py
-----------------
Apply the footer-nav fix to the Russian course in one pass:

  1. LESSON HTMLs - insert/refresh a static <nav class="lesson-nav"> +
     <footer class="site-footer"> block on every lesson page, just before
     <script src="site-nav.js">. Idempotent via BEGIN/END sentinels.

  2. styles/main.css - append/refresh a sentinel-wrapped block adding the
     .lesson-nav .home-link "ghost" variant, the .lesson-nav > span:empty
     placeholder rule, and the .footer-links styling. Idempotent via
     BEGIN/END sentinels.

  3. site-nav.js - replace with a slim version that only handles dark mode,
     header injection, content-wrap, and quiz interactivity. Prev/Next nav
     and site footer are no longer injected here (now static, see #1).
     Wholesale replace; no-op if already at target. NOTE: this drops the
     JS-side progress tracking (Latin's slimmed version also dropped it).
     The progressBar element on index.html will sit at "0 / 16".

Edge cases on #1:
  - First lesson: prev side becomes <span></span>.
  - Last  lesson: next link is omitted.

Usage:
    python3 add_footer_nav.py                # dry run (default)
    python3 add_footer_nav.py --apply        # write changes (.bak backups)
    python3 add_footer_nav.py --apply --no-backup
    python3 add_footer_nav.py --dir .        # explicit project dir
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Lesson order (from index.html .course-grid)
# Tuple: (filename, short_title_used_in_prev/next_link)
# ---------------------------------------------------------------------------
LESSONS: list[tuple[str, str]] = [
    ("russian_cyrillic_alphabet.html",          "The Cyrillic Alphabet"),
    ("russian_pronunciation_stress.html",       "Pronunciation & Stress"),
    ("russian_reading_writing.html",            "Reading & Writing Practice"),
    ("russian_greetings_essentials.html",       "Greetings & Essential Phrases"),
    ("russian_numbers_time_dates.html",         "Numbers, Time & Dates"),
    ("russian_family_descriptions.html",        "Family & Descriptions"),
    ("russian_food_dining.html",                "Food & Dining"),
    ("russian_shopping_money.html",             "Shopping & Money"),
    ("russian_directions_transportation.html",  "Directions & Transportation"),
    ("russian_health_body.html",                "Health & Body"),
    ("russian_hobbies_daily_life.html",         "Hobbies & Daily Life"),
    ("russian_work_education.html",             "Work & Education"),
    ("russian_technology_communication.html",   "Technology & Communication"),
    ("russian_weather_seasons.html",            "Weather & Seasons"),
    ("russian_emotions_relationships.html",     "Emotions & Relationships"),
    ("russian_travel_culture.html",             "Travel & Russian Culture"),
]

# ===========================================================================
# 1. LESSON HTML - footer-nav block
# ===========================================================================

BEGIN_HTML = "<!-- BEGIN footer-nav (managed by add_footer_nav.py) -->"
END_HTML   = "<!-- END footer-nav -->"

INSERT_BEFORE_RE = re.compile(
    r'(?P<lead>\s*)<script\s+src=["\']site-nav\.js["\']\s*>\s*</script>',
    re.IGNORECASE,
)
FALLBACK_BODY_RE = re.compile(r'\s*</body>', re.IGNORECASE)

EXISTING_HTML_BLOCK_RE = re.compile(
    re.escape(BEGIN_HTML) + r".*?" + re.escape(END_HTML),
    flags=re.DOTALL,
)


def build_footer(prev_file, prev_title, next_file, next_title):
    if prev_file:
        prev_html = (
            f'    <a href="{prev_file}" class="prev-lesson">'
            f'&larr; Previous: {prev_title}</a>'
        )
    else:
        prev_html = '    <span></span>'

    if next_file:
        next_html = (
            f'\n    <a href="{next_file}" class="next-lesson">'
            f'Next: {next_title} &rarr;</a>'
        )
    else:
        next_html = ''

    return (
        f"{BEGIN_HTML}\n"
        f'<nav class="lesson-nav" aria-label="Lesson Navigation">\n'
        f"{prev_html}\n"
        f'    <a href="index.html" class="home-link">&#127968; Course Home</a>'
        f"{next_html}\n"
        f"</nav>\n"
        f"\n"
        f'<footer class="site-footer">\n'
        f"    <p>&copy; 2026 All rights reserved.</p>\n"
        f'    <div class="footer-links">\n'
        f'        <a href="https://rays-home.netlify.app/">Ray\'s House of Fun</a>\n'
        f'        <a href="https://rays-home.netlify.app/contact">Contact</a>\n'
        f'        <a href="#" onclick="window.print(); return false;">Print Page</a>\n'
        f"    </div>\n"
        f"</footer>\n"
        f"{END_HTML}"
    )


def inject_html(html, footer):
    """Insert/refresh the footer block on a lesson HTML.

    Returns (new_html, status) where status is one of:
      'refreshed' | 'added' | 'unchanged' | 'skipped:no-anchor'
    """
    m = EXISTING_HTML_BLOCK_RE.search(html)
    if m:
        new = html[:m.start()] + footer + html[m.end():]
        return new, ("refreshed" if new != html else "unchanged")

    m = INSERT_BEFORE_RE.search(html)
    if m:
        start = m.start()
        new = html[:start].rstrip() + "\n\n" + footer + "\n\n" + html[start:].lstrip("\n")
        return new, "added"

    m = FALLBACK_BODY_RE.search(html)
    if m:
        new = html[:m.start()].rstrip() + "\n\n" + footer + "\n" + html[m.start():].lstrip("\n")
        return new, "added"

    return html, "skipped:no-anchor"


# ===========================================================================
# 2. styles/main.css - footer-nav rules (sentinel-wrapped block, append-at-end)
# ===========================================================================

BEGIN_CSS = "/* BEGIN footer-nav-styles (managed by add_footer_nav.py) */"
END_CSS   = "/* END footer-nav-styles */"

CSS_BLOCK = BEGIN_CSS + """
/* Home-link: outlined "ghost" variant to distinguish from prev/next */
.lesson-nav .home-link {
    background: transparent;
    color: var(--primary-color);
    border: 2px solid var(--primary-color);
}
.lesson-nav .home-link:hover {
    background: var(--primary-color);
    color: #fff;
    transform: translateY(-1px);
}

/* First lesson uses <span></span> as a prev placeholder; keep it inert */
.lesson-nav > span:empty { flex: 0 0 auto; }

.site-footer p { margin: .35rem 0; }

.footer-links {
    display: flex;
    justify-content: center;
    gap: 1rem;
    flex-wrap: wrap;
    margin-top: .5rem;
}
.site-footer .footer-links a { text-decoration: none; }
.site-footer .footer-links a:hover { text-decoration: underline; }
""" + END_CSS

EXISTING_CSS_BLOCK_RE = re.compile(
    re.escape(BEGIN_CSS) + r".*?" + re.escape(END_CSS),
    flags=re.DOTALL,
)


def inject_css(css):
    """Insert/refresh the sentinel-wrapped CSS block."""
    m = EXISTING_CSS_BLOCK_RE.search(css)
    if m:
        new = css[:m.start()] + CSS_BLOCK + css[m.end():]
        return new, ("refreshed" if new != css else "unchanged")
    new = css.rstrip() + "\n\n" + CSS_BLOCK + "\n"
    return new, "added"


# ===========================================================================
# 3. site-nav.js - slim replacement (wholesale; idempotent via content-equality)
# ===========================================================================

SITE_NAV_JS = """/* site-nav.js \u2014 Injects site header, dark mode toggle, content-wrap, and quiz interactivity.
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
    if (el) el.textContent = currentTheme() === 'dark' ? '\u2600\ufe0f' : '\U0001f319';
  }

  /* ---- Build header ---- */
  const header = document.createElement('header');
  header.className = 'site-header';
  header.innerHTML = `
    <a href="/index.html" class="site-brand">\U0001f1f7\U0001f1fa Russian Course</a>
    <nav class="nav-links">
      <a href="/index.html">Lessons</a>
      <a href="https://rays-home.netlify.app/" target="_blank" rel="noopener">Ray's House of Fun</a>
      <a href="https://rays-home.netlify.app/contact" target="_blank" rel="noopener">Contact</a>
      <label class="theme-toggle-label">
        <span class="theme-icon icon">${currentTheme() === 'dark' ? '\u2600\ufe0f' : '\U0001f319'}</span>
        <button class="theme-toggle" aria-label="Toggle dark mode"></button>
      </label>
    </nav>
  `;
  document.body.prepend(header);

  header.querySelector('.theme-toggle').addEventListener('click', toggleTheme);

  /* ---- Wrap existing content ---- */
  const isIndex = /index\\.html$/i.test(location.pathname) || location.pathname.endsWith('/');
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
"""


def inject_site_nav(current):
    if current == SITE_NAV_JS:
        return current, "unchanged"
    return SITE_NAV_JS, "replaced"


# ===========================================================================
# main
# ===========================================================================

def main() -> int:
    p = argparse.ArgumentParser(
        description="Apply the footer-nav fix to the Russian course (HTML + CSS + JS).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--apply", action="store_true",
                   help="Write changes (default: dry run only).")
    p.add_argument("--no-backup", action="store_true",
                   help="When applying, skip writing .bak files.")
    p.add_argument("--dir", default=".",
                   help="Project directory (default: current working dir).")
    args = p.parse_args()

    root = Path(args.dir).resolve()
    if not root.is_dir():
        print(f"ERROR: not a directory: {root}", file=sys.stderr)
        return 2

    mode = "APPLY (writing changes)" if args.apply else "DRY RUN (no writes)"
    print(f"Project root : {root}")
    print(f"Mode         : {mode}")
    if args.apply and not args.no_backup:
        print("Backups      : yes (.bak alongside each modified file)")
    print()

    def maybe_write(path: Path, original: str, new: str) -> None:
        if not args.apply or new == original:
            return
        if not args.no_backup:
            bak = path.with_suffix(path.suffix + ".bak")
            bak.write_text(original, encoding="utf-8")
        path.write_text(new, encoding="utf-8")

    total_pending = 0

    # ---- 1. Lesson HTMLs ----
    print("== 1. Lesson HTML files ==")
    total = len(LESSONS)
    missing: list[str] = []
    pending = 0
    for i, (fname, _title) in enumerate(LESSONS):
        path = root / fname
        if not path.is_file():
            missing.append(fname)
            print(f"  [missing  ] {fname}")
            continue

        prev = LESSONS[i - 1] if i > 0 else (None, None)
        nxt  = LESSONS[i + 1] if i < total - 1 else (None, None)
        footer = build_footer(prev[0], prev[1], nxt[0], nxt[1])

        original = path.read_text(encoding="utf-8")
        new_html, status = inject_html(original, footer)

        if status == "unchanged":
            print(f"  [ok       ] {fname}")
            continue
        print(f"  [{status:9}] {fname}")
        if new_html != original:
            pending += 1
            maybe_write(path, original, new_html)

    if missing:
        print(f"  Missing files: {len(missing)}  (check LESSONS table)")
    print(f"  HTML changes : {pending} / {total}")
    total_pending += pending
    print()

    # ---- 2. styles/main.css ----
    print("== 2. styles/main.css ==")
    css_path = root / "styles" / "main.css"
    if not css_path.is_file():
        print(f"  [missing  ] {css_path}")
    else:
        original = css_path.read_text(encoding="utf-8")
        new_css, status = inject_css(original)
        if status == "unchanged":
            print(f"  [ok       ] {css_path.name}")
        else:
            print(f"  [{status:9}] {css_path.name}")
            if new_css != original:
                total_pending += 1
                maybe_write(css_path, original, new_css)
    print()

    # ---- 3. site-nav.js ----
    print("== 3. site-nav.js ==")
    js_path = root / "site-nav.js"
    if not js_path.is_file():
        print(f"  [missing  ] {js_path}")
    else:
        original = js_path.read_text(encoding="utf-8")
        new_js, status = inject_site_nav(original)
        if status == "unchanged":
            print(f"  [ok       ] {js_path.name}")
        else:
            print(f"  [{status:9}] {js_path.name}")
            if new_js != original:
                total_pending += 1
                maybe_write(js_path, original, new_js)
    print()

    print(f"Total files needing changes: {total_pending}")
    if not args.apply and total_pending:
        print("Re-run with --apply to write changes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
