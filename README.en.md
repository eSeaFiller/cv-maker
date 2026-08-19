# CV Maker

> A résumé typesetting tool that is one HTML file. Click the text to rewrite it, turn the sliders for density, fill the page in one click.
> No account, no backend, no build toolchain — double-click to use, works offline.

**[Use it online](https://cv-maker-amp.pages.dev)** · **[Download the single file](https://github.com/eSeaFiller/cv-maker/releases/latest/download/cv-maker.html)** · [中文说明](README.md)

![The CV Maker window: layout sliders on the left, a real A4 sheet on the right](docs/screenshot.png)

The interface ships in Chinese and English — the toggle sits at the top left of the panel, and a browser in an English locale gets English on first open. An illustrated walkthrough lives behind the *Guide* link inside the tool; `docs/guide.html` is the same thing as a standalone page (Chinese only — download it and open it in a browser).

## What it fixes

Résumé sites hand you a template but no control: leading and size are locked, a short résumé leaves a slab of white at the bottom, and one extra line spills onto page two. Word is the opposite — everything is editable, but one change moves three other things.

CV Maker separates the two:

- **Content** is edited straight on the sheet — click anywhere and type. No forms, no field dialogs.
- **Layout** lives in the sliders on the left — sections, entries, bullets and header space each have their own spacing and never fight each other.

Or skip the fiddling and press *Fill one page*: a binary search finds the loosest set of values that still fits, rather than squashing everything to the floor.

## Design premises

| | |
|---|---|
| **One file** | The whole tool is a 1.5 MB `.html` with pdf.js inlined. Mail it, AirDrop it, drop it in chat — the other person double-clicks and it runs |
| **Works offline** | No external service, so it keeps working on a plane, and it will still open years from now |
| **Your résumé never leaves the machine** | Text, photo and every saved version live in your own browser's localStorage (the one network request is described [below](#data-and-privacy)) |
| **What you edit is what prints** | Editing height must equal print height. Every "+" button is absolutely positioned and takes no space; empty fields vanish completely in preview and print |

## What it does

| Feature | Notes |
|---|---|
| Edit in place | Name, dates, city, every bullet. <kbd>Enter</kbd> adds one, <kbd>Tab</kbd> demotes it to a sub-bullet and <kbd>⇧Tab</kbd> promotes it back, <kbd>⌫</kbd> on an empty one deletes it, <kbd>⌘B</kbd> bolds |
| Import a résumé | Upload `.pdf` / `.docx` / `.txt` / `.md`, or paste text; it is split into sections, entries and bullets, with a preview first and an automatic backup version |
| Four spacing levels | Sliders for sections, entries, bullets and header space, plus size, leading, margins, name size and contact size |
| Fill N pages | Too much tightens, too little opens up, landing exactly on one page or two |
| Smart page breaks | An entry a page edge would cut is moved down whole, and pages keep a normal head and foot margin. The gap is drawn while you edit, so the gap on screen is the gap that prints |
| Drag to reorder | Hover to the left of a section or entry and hold the six-dot handle |
| Styling | Three heading treatments × CJK and Latin faces × four accent colours |
| Bilingual | English section names and dates like `Sep 2022 - Present` are recognised; an imported English résumé switches to Latin typography |
| Versions | Archive and name one per employer, switch back any time; a blue dot marks edits not yet written back |
| Backup & print | Draft and every version export into a single `.json`; A4 PDF in one click |

## Building it yourself

```
cv-maker.html          the build artifact — download and open
src/
  source.html          source (a body fragment: no doctype, <html> or <head>)
  build.py             inlines pdf.js, wraps the doctype, writes cv-maker.html
  pdfjs/               pdf.js 3.11.174 (Apache-2.0, Mozilla)
docs/
  guide.html           the illustrated manual (Chinese)
  screenshot.png
```

After editing `src/source.html`:

```bash
python3 src/build.py
```

Python 3 and nothing else — no npm, no bundler. `source.html` is plain HTML/CSS/JS: the logic sits in one IIFE, the styles in a single `<style>` block at the top.

## Read this before changing the code

Rules learned the hard way — break them and you only find out at print time:

1. **What you edit is what prints.** Editing height must equal print height, so every "+" button is `position:absolute` and never occupies layout.
2. **Nothing empty may paint in preview or print.** Empty fields, empty bullets and placeholder hints all have to disappear. <kbd>⌘P</kbd> can fire while still in edit mode, so the print stylesheet forces the preview state.
3. **Delete buttons must be siblings of the editable box**, never inside it — putting them in wrecks the `:empty` placeholder logic and typing destroys them.
4. **Do not rename the localStorage keys** (`resume-desk-blank-v1`, `resume-desk-blank-versions-v1`) — existing users' data would be orphaned.
5. **Never rely on background colour for print.** Readers routinely switch "background graphics" off, which is why the section-heading bar and the summary rule are drawn with `border`.
6. **UI language changes the UI only** — not one character of the résumé itself.

### Adding a new string

The Chinese original *is* the dictionary key; `UI_EN` holds only the English:

```js
T("删除板块")                     // returned as-is in Chinese, looked up in UI_EN in English
T("已载入「{0}」。", v.name)       // {0} is replaced positionally
```

Static HTML is tagged `data-i18n="key"`, with the Chinese left in the tag and swapped only when English is selected. Forgetting a dictionary entry never breaks anything — that one string just stays untranslated.

## Data and privacy

- Your text, photo and every version are written to this browser's `localStorage` and **never uploaded**. Clearing site data clears them too, so export a `.json` backup for anything you care about.
- On its **first open** the tool sends one **empty request** to the author's server, purely to count how many people use it — no id, no device information, not a byte of your résumé. It never sends anything again, and the switch is in the About card.
- **If you fork this, blank out `HIT_URL`** (search `var HIT_URL` in `src/source.html`), or your deployment will report into the author's counter. Blank means the feature does not exist at all.

## Licence

[MIT](LICENSE) © 2026 XuJianghao

The bundled PDF parser is [pdf.js](https://github.com/mozilla/pdf.js) 3.11.174, Apache License 2.0, © Mozilla Foundation — its licence notice travels inside the built file.
