# The History of Pyright

## Origins and Creator

**Eric Traut** — a Stanford-educated software engineer and emulation pioneer — created Pyright. Before Pyright, Traut had a storied career: he worked at Apple Computer on the Mac 68K emulator (enabling the Motorola 68000 → PowerPC transition), co-founded Connectix (creators of Virtual PC and Virtual Game Station), and joined Microsoft after the 2003 Connectix acquisition. At Microsoft he rose to **Technical Fellow** — one of the company's most distinguished engineering roles — and worked on Hyper-V, Windows Core OS, Skype, and AI for Autonomous Systems.

Pyright was born as a **side project** with no dedicated team. Despite that humble start, it would reshape the Python type-checking landscape.

---

## Timeline

### 2019 — Launch

- **March 12, 2019**: Eric Traut made the [initial commit](https://github.com/microsoft/pyright/commit/1d91744b1f268fd088be86df8f2afb205af7019b) to the `microsoft/pyright` repository on GitHub — a massive 604-file, 64,339-line checkin.
- **March 24, 2019**: The project was publicly announced and quickly gained attention on Hacker News and Reddit. The first external PR (a typo fix) was merged the same day.
- **Key selling points at launch**:
  - Written in **TypeScript**, running on **Node.js** — no Python runtime required.
  - Claimed to be **5× faster** than mypy and other Python-written type checkers.
  - Supported PEP 484 (type hints), PEP 526 (variable annotations), and PEP 544 (structural subtyping).
  - Designed for **large Python codebases** with fast incremental updates.
  - Offered a **VS Code extension** with live feedback (tooltips, go-to-definition, etc.).
- The initial reaction was enthusiastic but cautious — many noted it was "a side project with no dedicated team."

### 2020 — Pylance Is Born

- **June 30, 2020**: Microsoft announced **Pylance**, a new Python language server for VS Code. Pylance was built on top of Pyright's type-checking engine, adding:
  - Rich IntelliSense and auto-completions
  - Bundled type stubs for popular packages
  - Semantic highlighting
  - Inlay hints
- The name "Pylance" was a nod to **Monty Python's Lancelot** — the first knight to answer the bridgekeeper's questions in *The Holy Grail*.
- Pylance became the **default Python language server** in VS Code, giving Pyright's core engine massive reach. While Pylance itself was closed-source (with some proprietary features), the underlying Pyright type checker remained fully open source.
- This was a pivotal moment: Pyright went from a niche side project to powering the Python experience for millions of VS Code users.

### 2021 — Growing Adoption

- Pyright matured rapidly with weekly releases, each containing bug fixes, performance optimizations, and new PEP support.
- The community grew, with users adopting Pyright as a **standalone CLI type checker** in CI/CD pipelines alongside or instead of mypy.
- Eric Traut began conducting annual **Pyright surveys** to gather community feedback.
- The relationship between Pyright and Pylance was clarified: core type-checking issues went to the `microsoft/pyright` repo, while language server features went to `microsoft/pylance-release`.

### 2022 — PEP 695 and Rapid Evolution

- Pyright continued its aggressive release cadence — by mid-2022 it had surpassed **version 1.1.257** with hundreds of releases.
- **Provisional PEP 695 support** (Improved Syntax for Type Parameters) was implemented, anticipating Python 3.12 features before the Python release.
- Performance optimizations for overload evaluation, semantic highlights, and type guard logic were shipped.
- The project consistently tracked the latest Python typing PEPs, often implementing support before other type checkers.

### 2023 — Peak and Transition

- The **third annual Pyright survey** (May 2023) showed Pyright had the **highest NSAT (Net Satisfaction) score** — 160 out of 200 — among Microsoft open-source projects that participated.
- Eric Traut revealed in the survey results: **"As of last month, I am no longer working for Microsoft, but I am still contributing to pyright in my spare time."** Even while at Microsoft, pyright was largely a personal effort.
- Traut's departure from Microsoft didn't immediately slow development — he continued making ~30 commits per week, maintaining the weekly release cadence.
- Pyright had become the de facto **reference implementation** for Python type-checking semantics, with mypy_primer integration testing its changes against a corpus of open-source projects.

### 2024 — Continued Development

- Pyright continued receiving regular updates, with Eric Traut contributing as an external collaborator.
- The project crossed **13,000+ GitHub stars**.
- Code improvements included memory optimizations (shortened file IDs for symbol tracking), refactored utilities, and continued PEP support.
- The Pylance team at Microsoft (led by contributors like @rchiodo, @jakebailey, @bschnurr, @debonte) continued to merge Pylance-specific changes back to Pyright.

### 2025–2026 — A New Chapter

- **January 8, 2026**: Pyright **1.1.408** was released — the latest release as of early 2026, with 489 total releases.
- **January 2026**: A community discussion titled ["The state of Pyright"](https://github.com/microsoft/pyright/discussions/11250) revealed the project's new reality:
  - A Microsoft maintainer confirmed: *"Pyright is still being maintained, just with fewer people. @erictraut was the main contributor in the past, but he's no longer doing this full time."*
  - The Pylance team still depends on Pyright under the hood but is *"more interested in being a language server than a type checker"* — meaning type-checker bug fixes are lower priority.
  - The release cadence has slowed; community PRs are accepted for type-checking issues.
- By March 2026, Eric Traut's GitHub activity showed he was still contributing to `microsoft/pyright` and `python/typing`, primarily through code review and issue triage.
- The project has **15,300+ stars**, **1,780 forks**, and **140 contributors**.

---

## Technical Architecture

- **Language**: TypeScript (33.7%), Python (66.3% — mostly test files and stubs)
- **Runtime**: Node.js
- **Key design decisions**:
  - No Python dependency — runs entirely on Node.js
  - Incremental analysis with watch mode for fast feedback
  - Bundled typeshed fallback for standard library stubs
  - Configurable strictness levels (off, basic, standard, strict)
  - Supports multiple Python versions (3.x) and execution environments per project

## Relationship to Other Tools

| Tool | Relationship |
|------|-------------|
| **Pylance** | VS Code language server built on Pyright's engine; adds IntelliSense, auto-imports, semantic highlighting. Closed-source additions on top of open-source Pyright. |
| **mypy** | The original Python type checker (by Jukka Lehtosalo / Dropbox). Pyright is often 5×+ faster. Both are widely used; some projects run both. |
| **Pyre** | Facebook/Meta's type checker. Less widely adopted than mypy or Pyright. |
| **Pytype** | Google's type checker. Focuses on type inference with fewer annotations required. |
| **basedpyright** | A community fork of Pyright with additional features and stricter defaults. |

## Legacy

Pyright transformed Python type checking from a slow, optional afterthought into a fast, integrated part of the development experience. Through Pylance, it reaches millions of developers daily. Eric Traut's one-person effort — built on evenings and weekends, written in TypeScript rather than Python — proved that a single determined engineer could reshape the tooling landscape for one of the world's most popular programming languages.

As of 2026, with Traut stepping back and the Pylance team's priorities shifting, the project faces an uncertain but hopeful future — its open-source foundation and 140+ contributors provide a path forward for community stewardship.
