# Russian Language Course — Project Status

**Project Path:** `\\wsl$\Ubuntu\home\practicalace\projects\russian`  
**Planned Netlify URL:** https://rays-russian.netlify.app  
**Last Updated:** April 14, 2026

---

## Site Structure

| File | Role | Status |
|------|------|--------|
| `index.html` | Homepage — card grid with 16 lesson links, progress tracker (localStorage-wired) | ✅ Complete |
| `site-nav.js` | Shared JS — injects header, dark mode toggle, prev/next nav, quiz interactivity, progress tracking, footer | ✅ Complete |
| `styles/main.css` | CSS — blue/red Russian-inspired theme, based on course_template + Mandarin-pattern index/nav styles | ✅ Complete |
| `favicon.png` | Site icon | ❌ **Needs copy:** `cp ~/projects/course_template/favicon.png ~/projects/russian/` |
| `favicon.ico` | Site icon (fallback) | ❌ **Needs copy:** `cp ~/projects/course_template/favicon.ico ~/projects/russian/` |
| `.git` | Git repo | ❌ **Needs init** |

---

## Lessons (16 total — all complete)

| # | File | Title |
|---|------|-------|
| 1 | `russian_cyrillic_alphabet.html` | The Cyrillic Alphabet |
| 2 | `russian_pronunciation_stress.html` | Pronunciation & Stress |
| 3 | `russian_reading_writing.html` | Reading & Writing Practice |
| 4 | `russian_greetings_essentials.html` | Greetings & Essential Phrases |
| 5 | `russian_numbers_time_dates.html` | Numbers, Time & Dates |
| 6 | `russian_family_descriptions.html` | Family & Personal Descriptions |
| 7 | `russian_food_dining.html` | Food & Dining |
| 8 | `russian_shopping_money.html` | Shopping & Money |
| 9 | `russian_directions_transportation.html` | Directions & Transportation |
| 10 | `russian_health_body.html` | Health & Body |
| 11 | `russian_hobbies_daily_life.html` | Hobbies & Daily Life |
| 12 | `russian_work_education.html` | Work & Education |
| 13 | `russian_technology_communication.html` | Technology & Communication |
| 14 | `russian_weather_seasons.html` | Weather & Seasons |
| 15 | `russian_emotions_relationships.html` | Emotions & Relationships |
| 16 | `russian_travel_culture.html` | Travel & Russian Culture |

Each lesson includes: vocabulary tables (Russian + Transliteration + English), grammar notes, cultural insights (blockquote callouts), practice dialogues, and interactive quizzes.

---

## Site Features

| Feature | Status |
|---------|--------|
| Light/Dark Mode Toggle | ✅ Via site-nav.js, localStorage persistence, prefers-color-scheme fallback |
| Sticky Nav Header | ✅ Injected by site-nav.js with Russian flag emoji 🇷🇺 |
| Prev/Next Lesson Navigation | ✅ Injected by site-nav.js on all lesson pages |
| Footer with Ray's House of Fun + Contact | ✅ Injected by site-nav.js |
| Card Grid Homepage | ✅ Responsive grid with lesson cards, numbers, descriptions, topic tags |
| Progress Tracker | ✅ On index.html — **wired to localStorage** (tracks visited lessons automatically) |
| Interactive Quizzes | ✅ Quiz interactivity handled by site-nav.js with hint/explanation feedback |
| Cultural Notes | ✅ Blockquote callouts in each lesson |
| Vocabulary Tables | ✅ Comprehensive Russian/Transliteration/English tables in every lesson |
| Practice Dialogues | ✅ In all lessons with transliteration and translation |
| Mobile Responsive | ✅ Via CSS media queries |
| Print Friendly | ✅ Print stylesheet hides nav/footer |
| Accessibility | ✅ prefers-reduced-motion support |

---

## Improvements Over Mandarin Template

1. **Progress tracker wired to localStorage** — automatically tracks visited lessons and updates the progress bar on index.html (Mandarin's was static "0/16")
2. **Richer quiz feedback** — hints for wrong answers AND explanations for correct answers (via data-hint and data-explanation attributes)
3. **Blue toggle for dark mode** — matches the Russian blue theme (Mandarin used red)

---

## Remaining Tasks

1. **Copy favicons from template:**
   ```bash
   cp ~/projects/course_template/favicon.png ~/projects/russian/
   cp ~/projects/course_template/favicon.ico ~/projects/russian/
   ```

2. **Initialize git repo and first commit:**
   ```bash
   cd ~/projects/russian
   git init
   git add .
   git commit -m "Initial commit: 16-lesson Russian language course"
   ```

3. **Deploy to Netlify:**
   - Create new site on Netlify
   - Set custom domain: `rays-russian.netlify.app`
   - Connect to git repo or drag-and-drop deploy

4. **Update rayhome files** ✅ (index.html, updates.html, search.html):
   - Add "Russian Language Course" link in Language Topics section
   - Add Russian entry to SITES array in updates.html
   - Add Russian entry to INDEX array in search.html with keyword tags
   - Update status.md with new site count and Recent Changes entry

---

## Future Enhancements

- Add audio pronunciation hints or IPA notation
- Add more practice dialogues and exercises to later lessons
- Create a review/flashcard lesson
- Add Mermaid diagrams for grammar concepts (case system overview, verb conjugation patterns)
- Add Cyrillic handwriting practice with stroke animations
- Add case declension reference tables
- Add verb conjugation practice interactive exercises

---

## Design Decisions

- **CSS:** Based on `course_template/styles/main.css` variable system with Mandarin-pattern additions for index page (card grid, hero, progress tracker, site-header injection)
- **Nav pattern:** Uses `site-nav.js` (like Mandarin, Korean, Spanish, Kapampangan) rather than course_template's inline nav — simpler per-page HTML, single file to maintain
- **Color scheme:** Deep blue primary (`#1e3a8a`) + red accent (`#dc2626`) — inspired by Russian flag. Cool white background (`#f0f4ff`) in light mode, deep navy (`#0f172a`) in dark mode
- **Content approach:** Each lesson has vocab tables, grammar notes, cultural insights, practice dialogues, and quizzes
- **Lesson order:** Cyrillic alphabet first (lessons 1-3), then practical conversation topics (4-16), building from basics to advanced
- **Cultural emphasis:** Strong focus on modern Russian digital life (VK, Telegram, Yandex), дача culture, toasting customs, emotional depth (русская душа), and superstitions alongside classic culture (literature, ballet, architecture)
- **Grammar integration:** Key cases (prepositional, genitive, dative, instrumental) introduced naturally within topical lessons rather than as standalone grammar lessons

---

## WSL Path Note
- **Works:** `\\wsl$\Ubuntu\home\practicalace\projects\russian`
- **Does NOT work:** `\\wsl.localhost\Ubuntu\...`
