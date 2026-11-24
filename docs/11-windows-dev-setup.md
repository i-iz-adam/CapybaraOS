# 11 — Windows Development Setup

**Owner:** design session 2 · **Status:** v0.1 · Primary dev machine is **Windows**; macOS/Linux notes are in the Tauri docs.

Commands are **PowerShell**. `winget` package IDs are the commonly used ones — if one fails, run `winget search <name>` or use the download link.

---

## 1. Prerequisites (one-off)

Tauri on Windows needs the **Microsoft C++ Build Tools** ("Desktop development with C++"), **WebView2**, **Rust** and **Node.js LTS** (<https://v2.tauri.app/start/prerequisites/>).

```powershell
# C++ build tools (Desktop development with C++ workload)
winget install Microsoft.VisualStudio.2022.BuildTools --override "--wait --passive --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"

# WebView2 runtime (already present on Windows 11 and current Windows 10 — skip if so)
winget install Microsoft.EdgeWebView2Runtime

# Rust (restart the terminal afterwards)
winget install --id Rustlang.Rustup
rustup default stable-msvc

# Node.js LTS + pnpm
winget install OpenJS.NodeJS.LTS
# restart the terminal, then:
corepack enable          # if this fails with a permissions error, use: npm install -g pnpm
pnpm --version
```

Verify:

```powershell
node -v; pnpm -v; rustc --version; cargo --version; git --version
```

Recommended Git settings:

```powershell
git config --global core.longpaths true
git config --global core.autocrlf true     # repo has .gitattributes; this keeps working copies CRLF on Windows
```

If PowerShell blocks scripts: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

## 2. Shell work does **not** need Rust

Phase S is built and previewed in a normal browser with Vite (fast hot reload, no Rust compile). Tauri is only needed for the native frame (custom titlebar, tray, keychain, PTY), so:

| You are doing | Run |
|---|---|
| Building/iterating shell screens | `pnpm dev` (Vite in the browser) |
| Checking the native window, titlebar, tray | `pnpm tauri dev` |
| UI smoke tests | `pnpm test:e2e` (Playwright) |

First `pnpm tauri dev` compiles Rust for several minutes; later runs are incremental. Excluding the repo's `target\` folder from Windows Defender real-time scanning speeds Rust builds noticeably (optional, your call).

## 3. Scaffolding the repo (done in shell session 3 — reference only)

The session that scaffolds follows `04-tech-stack.md` §4 but **only creates what the shell needs** (no empty crates):

```powershell
cd <your-repo-path>
# pnpm workspace root + apps/desktop (Vite + React + TypeScript) + packages/protocol + packages/ui
pnpm init
# apps/desktop: pnpm create vite apps/desktop --template react-ts
# then add Tauri 2 to apps/desktop:  pnpm add -D @tauri-apps/cli  &&  pnpm tauri init
```

Pin versions in lockfiles; add dependencies one at a time with a note in the PR (rule 5, `09-agent-workflow.md`).

## 4. Packaging this repo's docs for the next AI session

Reference images are **gitignored**, so they live only on your machine. When starting a new session, upload a zip that includes them. Use `tar` (built into Windows 10+) — **not** `Compress-Archive`, which in Windows PowerShell 5.1 writes backslash paths that break on Linux:

```powershell
cd <your-repo-path>
tar -a -c -f ..\capybaraos-context.zip 00-START-HERE.md README.md CONTRIBUTING.md docs research
```

## 5. Applying a session's returned zip

```powershell
cd <your-repo-path>
tar -xf $HOME\Downloads\capybaraos-session2-changes.zip      # overwrites changed files in place
git status
git add -A
git commit -m "docs: shell-first design specification (S-01..S-30), roadmap Phase S"
```

(`Expand-Archive -Path <zip> -DestinationPath . -Force` also works.)
