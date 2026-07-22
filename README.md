# codeberg-repo-reaper

Remove all your repos from Codeberg.

Vibe-coded with Google Gemini 3.6 Thinking.

A fast, multithreaded Python script designed to bulk delete repositories from [Codeberg](https://codeberg.org/) (or any Forgejo/Gitea instance) using the official REST API.

---

## ⚡ Features

* **Multithreaded Execution:** Deletes multiple repositories in parallel using `concurrent.futures.ThreadPoolExecutor`.
* **Automatic Pagination:** Fetches all repositories across all pages without hard limits.
* **Safety Dry-Run Mode:** Test and review the deletion queue before performing any actual destructive operations.
* **Whitelist Protection:** Prevent important repositories from being accidentally deleted.

---

## 📋 Prerequisites

* **Python 3.6+**
* `requests` package

Install the required dependency using `pip`:

```bash
pip install requests
```
