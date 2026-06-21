---
name: agent-memory
version: "1.0.0"
updated: "2026-06-21"
description: Use when working with Agent Memory, memory/index.md, sessionStart registration, manual memory registration, session status updates, snapshot merge updates, continuing from a previous memory session, memory references, releasing references, organizing memory, cleaning memory, archiving memory sessions, cross-agent context, or finding previous agent sessions.
---

# Agent Memory

## Overview

Agent Memory is the working-memory layer for Cursor agents. It lives beside `raw/` and `wiki/`, not inside `wiki/`.

```text
G:\我的雲端硬碟\Obsidian\Agent\
  raw\
  wiki\
  memory\
```

Use `memory/` for session metadata, cross-agent lookup, and manual archive cleanup. Do not treat it as wiki content, and do not update `wiki/index.md` or `wiki/log.md` for ordinary Memory operations unless the user explicitly asks to document the process in the Wiki.

Default usage model: most chats only get an automatic `idle` placeholder. Promote to `active` only when there is real work to record. Users rarely close sessions one by one; say `整理 memory` to delete `idle` rows and mark overdue `active` sessions as `stale`, and explicitly archive finished sessions that have snapshots.

## Paths

```text
Memory root: G:\我的雲端硬碟\Obsidian\Agent\memory
Index:       G:\我的雲端硬碟\Obsidian\Agent\memory\index.md
Sessions:    G:\我的雲端硬碟\Obsidian\Agent\memory\sessions\<session-id>.md
Archive:     G:\我的雲端硬碟\Obsidian\Agent\memory\archive\<session-id>\
```

First version rules:

- `memory/index.md` is the working board.
- `memory/sessions/<session-id>.md` is the only supported session-file path if a session file exists.
- Keep V1 scoped to the Memory Index, optional single session files, and archive cleanup.

## Memory Index Schema

`memory/index.md` uses this table:

```markdown
| Session ID | Agent Name | Topic | Summary | Keywords | Status | Referenced By | Started At | Updated At |
|---|---|---|---|---|---|---|---|---|
```

`Referenced By` lists Memory Session IDs of agents currently continuing from this session.

- Use `-` when nobody references this session.
- Use one Session ID when a single agent references it.
- Use comma-separated Session IDs when multiple agents reference it, for example: `2026-05-25-1318-cursor-main-agent, 2026-05-26-0900-cursor-main-agent`.
- Store referencing Session IDs, not Agent Names. Agent Name is not unique across parallel chats.

Do not use `Referenced By` to mean ownership. The original session row still belongs to the session that created it.

Status values in the main index:

```text
idle
active
stale
```

Do not use `closed` or `archived` in the main index. Ending a session means archiving it and removing the row from `memory/index.md`. Archived metadata belongs in `memory/archive/<session-id>/index.md`.

## Status Lifecycle

Status describes the **work-memory lifecycle**, not whether a chat window is open.

| Status | Meaning | Typical case |
|---|---|---|
| `idle` | Registered, but no meaningful work yet | SessionStart auto registration; Topic still `未設定`; usually no session file |
| `active` | Real work in progress or recently updated | Manual registration, status update, or continuing from another memory session |
| `stale` | Had real content before, but not updated for a long time | Former `active` session with snapshot or meaningful Summary; candidate for review, not auto-delete |

### Transitions

```text
SessionStart auto registration  → idle
Manual registration             → active
Status update                   → active (promote from idle if needed)
Continue from source memory     → current session active; source may stay active or become stale
Long time without update        → active → stale (during Organize Memory)
Organize Memory                 → delete all idle rows; mark overdue active as stale
Archive                         → row removed from index; metadata kept under archive/ (sessions with snapshot only)
```

Promotion rules:

- **SessionStart** always writes `idle`.
- **Manual registration** and **status update** always set `active`.
- If a session is still `idle` when the user asks for a status update, promote it to `active` while writing the snapshot.
- Do not promote `idle` to `active` just because the chat is still open.

Stale rules (defaults; user may override when organizing):

- During **Organize Memory**, mark `active` as `stale` when `Updated At` is older than **14 days**, the session has a snapshot or non-default Summary, and `Referenced By` is `-`.
- Do **not** auto-mark `idle` sessions as `stale`; they are removed directly during organize instead.

There is no per-session `closed` step. When the user wants a session to end, archive it.

## Snapshot Merge Policy

Session snapshots are **integrated working summaries**, not transcript dumps and not blind overwrites.

When a snapshot file already exists:

1. **Read the existing snapshot first.** Never rewrite from conversation context alone.
2. **Merge, do not replace.** Integrate the existing snapshot with new information from the current conversation.
3. **Preserve still-valid facts** from the previous snapshot even if they no longer appear in the active chat context.
4. **Append or update by section** using the rules below.
5. **Do not silently delete** prior decisions, artifacts, questions, or context. If something is outdated, mark it explicitly instead of dropping it.

Section merge rules:

| Section | Merge rule |
|---|---|
| `Current Context` | Keep still-valid background from the old snapshot. Add or update with the latest progress. You may tighten wording, but do not drop key facts unless they are explicitly superseded. |
| `Decisions` | Keep prior decisions. Append new ones. If a decision is reversed, keep the old item and mark it `[superseded]` or move it to `Superseded / Resolved`. |
| `Files / Artifacts` | Union of old and new entries; deduplicate. |
| `Open Questions` | Keep unresolved items. Move resolved items to `Superseded / Resolved` or mark `[resolved]`. |
| `Next Actions` | Update freely, but keep still-relevant old actions unless they are done or replaced. Mark completed items `[done]` or move them to `Superseded / Resolved`. |
| `Continues From` | Preserve unless the user changes continuation or releases a reference. |
| `Superseded / Resolved` | Optional section for replaced decisions, resolved questions, and completed or abandoned actions. |

First-time snapshot creation (no existing file) still uses the template below and writes from the current conversation.

After a merge update, verify:

- Important items from the previous snapshot still appear, or are explicitly marked `[superseded]`, `[resolved]`, or `[done]`.
- New conversation progress is reflected.
- `Updated At` in Metadata matches the current update.

## Safe Index Writes

`memory/index.md` can be written by hooks and agents at nearly the same time. Treat it as append-sensitive shared state.

When adding a row:

1. Re-read the latest `memory/index.md` immediately before writing.
2. Append only the new row.
3. Do not use fixed-context patches to insert rows into the table.
4. Verify the new Session ID exists after writing.

When updating a row:

1. Re-read the latest `memory/index.md`.
2. Update only the matching row.
3. Verify the row still exists and reflects the intended values.

If a manual edit is unavoidable, preserve every existing row exactly. Never rewrite the whole table from an older read.

## SessionStart Registration

When registering a session:

1. Get the current timestamp.
2. Determine a stable `Agent Name`; default main-agent name is `cursor-main-agent`.
3. Generate a Memory Session ID using `YYYY-MM-DD-HHMM-agent-name`.
4. Prepare default metadata:
   - `Topic`: `未設定`
   - `Summary`: `sessionStart 自動註冊，尚未整理主題。`
   - `Keywords`: `sessionStart, cursor-agent`
   - `Status`: `idle`
   - `Referenced By`: `-`
   - `Started At` and `Updated At`: current timestamp
5. Append the row to `memory/index.md`.
6. Verify the row was written.
7. Only after successful write, report to the agent:

```text
Your Memory Session ID is: <session-id>
```

If writing `memory/index.md` fails, do not report a Memory Session ID. The agent must not believe it has registered when it has not.

SessionStart creates an index row only. It does **not** create `memory/sessions/<session-id>.md`.

## Manual Registration

Use this when the current agent is already running but does not have a Memory Session ID.

Trigger phrases:

```text
註冊 memory session
補註冊 memory
手動註冊 memory
```

Do not borrow or guess an existing row from `memory/index.md`. If the agent does not explicitly know its own Memory Session ID, create a new row.

Manual registration follows the same write-and-verify rule as `sessionStart` registration:

1. Get the current timestamp.
2. Determine a stable `Agent Name`; default main-agent name is `cursor-main-agent`.
3. Generate a Memory Session ID using `YYYY-MM-DD-HHMM-agent-name`.
4. Prepare default metadata:
   - `Topic`: infer from the current conversation, or `未設定` if unclear
   - `Summary`: one or two sentences summarizing what this session has done or decided so far
   - `Keywords`: `manual-registration, cursor-agent, session-snapshot`
   - `Status`: `active`
   - `Referenced By`: `-`
   - `Started At` and `Updated At`: current timestamp
5. Write a session snapshot to `memory/sessions/<session-id>.md`.
6. Re-read the latest `memory/index.md`, then append the row.
7. Verify both the session snapshot and index row were written.
8. Only after successful writes, report:

```text
Your Memory Session ID is: <session-id>
```

If either write fails, do not report a Memory Session ID.

The session snapshot should summarize the current conversation, not dump the full transcript. If `memory/sessions/<session-id>.md` already exists for this Session ID, use **Snapshot Merge Policy** instead of creating a fresh file.

Use this template:

```markdown
# Session: <session-id>

## Metadata

| Field | Value |
|---|---|
| Session ID | <session-id> |
| Agent Name | <agent-name> |
| Topic | <topic> |
| Status | active |
| Started At | <started-at> |
| Updated At | <updated-at> |

## Current Context

Summarize what has happened in this agent session so far.

## Decisions

- List decisions already made.

## Files / Artifacts

- List files, folders, hooks, skills, or wiki pages created or changed.

## Open Questions

- List unresolved questions, or write `None`.

## Next Actions

- List likely next steps, or write `None`.

## Continues From

- List source Memory Session IDs this session continues from, or write `None`.

## Superseded / Resolved

- List replaced decisions, resolved questions, or completed/abandoned actions, or write `None`.
```

When continuing from another session, always fill `Continues From` in the referencing session snapshot and update the source session's `Referenced By` in `memory/index.md`.

For manual registration, set:

```text
Summary: summarize the current session's actual topic, decisions, and outputs
Keywords: manual-registration, cursor-agent, session-snapshot
```

Use `手動補註冊，已建立 session snapshot。` only as a fallback when the current session content cannot be inferred. Prefer a useful content summary because other agents use `Summary` to decide whether this session is relevant.

## Continue Memory（接續記憶）

Use this when the current agent should pick up work from a previous memory session.

`引用 memory` here means **continue work** from a source session: update the referencing snapshot's `Continues From` and the source index row's `Referenced By`. It does not mean read-only lookup.

Trigger phrases:

```text
接續 memory <session-id>
接續 memory session <session-id>
引用 memory <session-id>
沿用 memory <session-id>
```

Workflow:

1. Read `memory/index.md` and locate the source session row.
2. Read `memory/sessions/<source-session-id>.md` when it exists; otherwise use index metadata only.
3. Ensure the **current** session has a Memory Session ID:
   - If the current agent already has one, use it.
   - If not, perform manual registration for the current session first.
4. Record continuation in the **current** session snapshot using **Snapshot Merge Policy**:
   - If the current agent already has a Memory Session ID, including an `idle` SessionStart row, use **Session Update** to merge-update the snapshot, promote to `active`, and fill or preserve `Continues From`.
   - If the current agent has no Memory Session ID, perform **Manual Registration** first, then ensure `Continues From` lists the source Session ID.
   - Add or update `## Continues From` with the source Session ID.
   - Summarize what the current agent is continuing under `## Current Context`.
   - Do not create a second index row when the current agent already has a Memory Session ID.
5. Update the **source** session row in `memory/index.md`:
   - Re-read the latest index.
   - Update only the source row's `Referenced By`.
   - If `Referenced By` is `-` or empty, set it to the current Session ID.
   - If it already lists other Session IDs, append the current Session ID with comma separation when it is not already present.
   - Do not change the source session's Topic, Summary, Keywords, or Status unless the user explicitly asks.
6. Verify:
   - The current session snapshot lists the source under `Continues From`.
   - The source index row lists the current Session ID under `Referenced By`.
7. Do **not** archive or close the source session automatically.

If either the current snapshot write or the source `Referenced By` update fails, report the continuation as incomplete. Do not claim the reference was established.

The source session remains in the index as historical context until the user archives it during organize.

## Release Reference（解除引用）

Use this when a referencing session no longer depends on a source session, or before archiving a referencing session.

Trigger phrases:

```text
解除引用 memory <source-session-id>
解除 memory 引用 <source-session-id>
release memory reference <source-session-id>
```

Workflow:

1. Confirm the current Session ID, or the Session ID the user names as the referencing session.
2. Read the latest `memory/index.md` and locate the source session row.
3. Remove the referencing Session ID from the source row's `Referenced By`.
4. If no referencing Session IDs remain, set `Referenced By` to `-`.
5. Update the referencing session snapshot:
   - Remove the source Session ID from `Continues From`, or set the section to `None` if empty.
6. Verify both writes succeeded.

When archiving a referencing session, release its references first:

1. Read the referencing session snapshot `Continues From` section when present.
2. For each source Session ID listed there, remove the referencing Session ID from that source row's `Referenced By`.
3. Then archive the referencing session normally.

If reference cleanup fails, do not archive the referencing session yet.

## Session Update（狀態更新）

Use this when the current agent already has a Memory Session ID and the user asks to update, merge, or record the session state.

Trigger phrases:

```text
狀態更新
memory session 狀態更新
更新 memory session
更新 memory 狀態
整理這個 session
```

`整理這個 session` means update the **current** session snapshot and index row. It is **not** batch organize/archive of `memory/`. If the user says `整理 memory` or `清理 memory`, use Organize Memory instead.

Requirements:

- The agent must know **its own** Memory Session ID for this conversation. Do not update a different session row unless the user explicitly names another Session ID.
- **Always update both** `memory/sessions/<session-id>.md` **and** the matching row in `memory/index.md`.
- **Never** update only `memory/index.md` and skip the session file.
- Set `Status` to `active`. Promote from `idle` when needed.
- If a snapshot already exists, follow **Snapshot Merge Policy**. Do not overwrite it from the current chat context alone.

Workflow:

1. Get the current timestamp for `Updated At`.
2. Confirm the Session ID (from hook context, prior report, or user).
3. Read the latest `memory/index.md` and locate the row for this Session ID.
4. Read `memory/sessions/<session-id>.md` if it exists.
5. Update or create the session snapshot:
   - If the file **exists**: apply **Snapshot Merge Policy**. Merge the existing snapshot with new information from the current conversation. Update `Updated At` in Metadata. Preserve `Started At` unless the user corrects it.
   - If the file **does not exist** (common after `sessionStart` only wrote the index): **create** it using the same template as Manual Registration, filled from the current conversation. Do not leave an index-only session after a status update.
6. Re-read the latest `memory/index.md`, then update **only** the matching row:
   - `Topic`, `Summary`, `Keywords`, `Status`, `Updated At` as needed
   - Set `Status` to `active`
   - Keep `Session ID`, `Agent Name`, `Started At`, and `Referenced By` unchanged unless the user corrects them or explicitly releases or adds a memory reference
7. Verify both writes succeeded:
   - The session file exists and reflects the merged latest context
   - Important items from the previous snapshot still appear, or are explicitly marked `[superseded]`, `[resolved]`, or `[done]`
   - The index row still exists and `Updated At` matches the intended timestamp
8. Only after verification, report completion to the user.

Index vs session file:

| Location | Purpose |
|---|---|
| `memory/index.md` | Short lookup: Topic, Summary, Keywords, Status, Referenced By |
| `memory/sessions/<session-id>.md` | Full merged snapshot: context, decisions, artifacts, open questions, next actions, continues from, superseded/resolved |

Keep `Summary` in the index aligned with `Current Context` in the session file (same facts, index shorter).

If either write fails, say the update is incomplete. Do not claim the session was updated.

## Reading Memory

When looking for previous context:

1. Read `memory/index.md`.
2. Prefer `active` and `stale` sessions with meaningful Topic, Summary, or Keywords.
3. Treat `idle` rows with `未設定` as low-priority placeholders unless the user names a specific Session ID.
4. Do not read full session files by default.
5. Only read `memory/sessions/<session-id>.md` when the user explicitly asks for the session content or when the index metadata is not enough.

## Organize Memory

Use this workflow when the user says "整理 memory", "清理 memory", or asks to organize/clean the memory index.

If the user says `整理這個 session`, use Session Update for the current session instead. Do not use Organize Memory for that phrase.

If the user says "封存 memory session" **with a specific Session ID**, use **Single-session archive** below instead of the default organize flow.

The user usually does **not** close sessions one by one. Default organize is automatic cleanup plus stale marking, not per-session archive.

Archive model:

```text
memory/
  index.md
  sessions/
    <session-id>.md
  archive/
    <session-id>/
      index.md
      session.md
```

### Default organize flow（整理 memory）

When the user asks to organize memory without naming a specific session to archive, apply both steps automatically. Do not ask for confirmation unless the user gave conflicting instructions.

**Step 1 — Delete all `idle` rows**

- Read `memory/index.md`.
- Remove every row whose `Status` is `idle` directly from the index.
- Do **not** create `memory/archive/<session-id>/` for deleted `idle` rows.
- An `idle` row should not have `memory/sessions/<session-id>.md`. If it does, stop and report the inconsistency; do not delete until the user resolves it.
- Do not delete rows whose `Referenced By` is not `-`, even if they are `idle`.

**Step 2 — Mark overdue `active` rows as `stale`**

- For each remaining row with `Status` `active`:
  - If `Updated At` is older than **14 days**
  - and the session has a snapshot or non-default Summary
  - and `Referenced By` is `-`
  - set `Status` to `stale`
  - keep `Updated At` unchanged so it still reflects the last meaningful work time
- Do **not** auto-archive `stale` rows during organize.
- Do **not** mark recent `active` rows as `stale`.

**Step 3 — Report results**

Report to the user:

- which `idle` Session IDs were deleted
- which `active` Session IDs were marked `stale`
- which rows were kept as `active`
- which rows are protected because `Referenced By` is not `-`

### Delete vs archive

| Case | Action |
|---|---|
| `idle` row during default organize | **Delete** from `memory/index.md`; no archive |
| `active` or `stale` row with snapshot when user explicitly archives | **Archive** under `memory/archive/<session-id>/` |
| Row with `Referenced By` not `-` | **Do not delete or archive** until references are released |

Never direct-delete `active` or `stale` rows that have a snapshot or meaningful Summary. End those sessions only through explicit archive.

Use index `Referenced By` as the primary protection signal. Treat `Continues From` in other snapshots as a fallback when continuation was recorded incompletely and the source row's `Referenced By` was not updated.

### Single-session archive

When the user names a specific Session ID to archive:

1. Read `memory/index.md`.
2. Identify the session row to archive.
3. If the row's `Status` is `idle` and no `memory/sessions/<session-id>.md` exists, **direct-delete** the row from the index instead of archiving. Report the deletion.
4. If the row's `Referenced By` is not `-`, stop and report which Session IDs still reference it. Do not archive unless the user explicitly forces archive after releasing those references.
5. Read `memory/sessions/<session-id>.md` when it exists and collect any source Session IDs from `Continues From`.
6. Create `memory/archive/<session-id>/`.
7. Convert the original row into `memory/archive/<session-id>/index.md`.
8. Check whether `memory/sessions/<session-id>.md` exists.
9. If it exists, move it to `memory/archive/<session-id>/session.md`.
10. If it does not exist, stop and direct-delete the row instead of creating an empty archive.
11. For each source Session ID collected from `Continues From`, remove this archived Session ID from that source row's `Referenced By`.
12. Confirm archive index exists, and the session file was moved when applicable.
13. Only then remove the row from `memory/index.md`.
14. Verify `memory/index.md` no longer contains the Session ID and the archive index exists when archive was used.

Archive only sessions with meaningful retained content. Do not create empty archive folders for placeholder rows.

If archive index creation fails, or a session file should move but fails to move, leave the original row in `memory/index.md`.

## Archive Index Template

```markdown
# Archived Session: <session-id>

## Metadata

| Field | Value |
|---|---|
| Session ID | <session-id> |
| Agent Name | <agent-name> |
| Topic | <topic> |
| Summary | <summary> |
| Keywords | <keywords> |
| Original Status | <status-before-archive> |
| Referenced By | <referenced-by-before-archive> |
| Started At | <started-at> |
| Updated At | <updated-at> |
| Archived At | <archived-at> |

## Files

- Session: ./session.md
```

Use this template only when a session snapshot exists or existed and was moved to `./session.md`. Do not create empty archive entries for `idle` placeholder rows.

## Common Mistakes

- Do not place Memory inside `wiki/`.
- Do not update Wiki index/log for ordinary Memory operations.
- Do not invent task-specific Agent Names; put task wording in `Topic` or `Keywords`.
- Do not report a Memory Session ID before confirming required Memory writes succeeded.
- Do not assume the latest `active` row is the current agent; manually register instead if unsure.
- Do not assume the latest row of any status is the current agent.
- Do not use fixed-context patches to add rows to `memory/index.md`; append to the latest file content.
- Do not remove a row with a snapshot or meaningful Summary without archiving it first, except during default organize deletion of `idle` rows.
- Do not archive placeholder `idle` rows; delete them during organize instead.
- Do not perform a session status update by editing only `memory/index.md`; always update or create `memory/sessions/<session-id>.md` as well.
- Do not overwrite an existing snapshot from the current chat context alone; read the old snapshot and merge using **Snapshot Merge Policy**.
- Do not silently delete prior decisions, artifacts, open questions, or context during a merge update; mark them `[superseded]`, `[resolved]`, or `[done]` instead.
- Do not clear `Referenced By` or `Continues From` during an ordinary status update unless the user explicitly releases or changes a memory reference.
- Do not assume `sessionStart` already created a session file; check `memory/sessions/` and create the snapshot on status update if missing.
- Do not set SessionStart registrations to `active`; they start as `idle`.
- Do not use `closed` in the main index; archive instead.
- Do not expect the user to close every session manually; use organize for idle cleanup and stale marking, and explicit archive for finished sessions with snapshots.
- Do not auto-archive `active` or `stale` sessions during default organize.
- Do not archive a source session while its `Referenced By` is not `-`.
- Do not update only the referencing session snapshot when continuing memory; also update the source row's `Referenced By`.
- Do not archive a referencing session before removing it from each source row's `Referenced By`.
- Do not store Agent Names in `Referenced By`; use Memory Session IDs only.

## Reference Model

Bidirectional linkage:

| Location | Field | Meaning |
|---|---|---|
| Source session index row | `Referenced By` | Which sessions are currently continuing from this source |
| Referencing session snapshot | `Continues From` | Which source sessions this session continues from |

Use the index column for archive protection and quick lookup. Use the snapshot section for full context inside the referencing session.
