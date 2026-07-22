# AGENTS.md — Guidelines for AI Collaborators

This repository contains **Scuttle**, a multithreaded Python utility designed to bulk-delete repositories on Codeberg (Forgejo/Gitea) via REST API.

Because this tool performs **irreversible destructive operations**, any AI agent modifying or extending this codebase must strictly adhere to the guidelines below.

---

## 🛑 Critical Safety Directives

1. **`DRY_RUN` Default Must Remain `True`**
   * Never change the default value of `DRY_RUN` to `False` in committed code or default parameter signatures.
   * Any CLI flag or configuration enabling active deletion must require explicit user action (e.g., `--confirm` or `--force`).

2. **Whitelist Protection Logic**
   * Do not remove, bypass, or weaken the repository whitelist check (`WHITELIST`).
   * The whitelist check must execute **before** any network call that initiates a `DELETE` request.

3. **No Destructive API Testing against Live Accounts**
   * Automated tests must **mock HTTP calls** (`unittest.mock` / `responses` / `pytest-mock`).
   * Never issue real `DELETE` requests during unit or integration testing.

---

## 🛠️ Project Architecture & Stack

* **Language:** Python 3.8+ (Standard Library + `requests`)
* **Concurrency:** `concurrent.futures.ThreadPoolExecutor`
* **API Target:** Codeberg / Forgejo / Gitea API v1 (`/api/v1`)

### Key Operations
* **Pagination:** Handled by querying `page=N` and `limit=50` sequentially until an empty array is returned.
* **Deletion:** Handled concurrently across multiple worker threads using `DELETE /api/v1/repos/{owner}/{repo}`.

---

## 📐 Code Style & Conventions

* **Typing:** Use type hints (`from typing import List, Dict, Any`) for function arguments and return types.
* **Error Handling:** Gracefully catch network exceptions (`requests.RequestException`) and HTTP status errors. Never crash the main execution loop if a single repository fails to delete.
* **Logging & Output:** Use clean terminal output with emoji indicators (e.g., `✅`, `❌`, `🛡️`, `🔍`) to make operation statuses instantly recognizable to the user.
* **Formatting:** Follow PEP 8 standard formatting rules.

---

## 🧪 Testing Instructions

When writing or executing tests:

1. Ensure `requests.get` and `requests.delete` are fully mocked.
2. Verify pagination logic by mocking multi-page responses (e.g., Page 1 returning full array, Page 2 returning empty array).
3. Verify that whitelisted repos are never passed to the deletion worker.
4. Verify that when `DRY_RUN = True`, no `requests.delete` calls are invoked.

---

## 🚀 Common Tasks & Extensions

If instructed to add features, follow these patterns:
* **CLI Arguments:** Use `argparse` to allow overriding token, username, workers, and `--dry-run` state via terminal flags.
* **Configuration Files:** If adding YAML or JSON config loading, place schema validation before executing any network requests.
