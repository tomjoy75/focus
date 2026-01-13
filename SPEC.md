# Focus — Specification V1

## Objective

Focus is a command-line tool designed to help a developer:
- sit down and start a work session,
- stay engaged without artificial interruptions,
- leave without guilt,

in a social and non-controllable environment (e.g. École 42), where interruptions are inevitable.

The tool prioritizes cognitive stability over productivity metrics.

---

## Core Principles

- The tool is **consultative**, never intrusive.
- It **does nothing automatically**.
- It only responds when the user explicitly calls it.
- It **never judges performance**.
- It produces **no alerts, alarms, or notifications**.
- External (human) interruptions are considered **neutral**.
- The user remains fully in control at all times.

---

## Commands — V1

### `focus start`

Starts a new focus session.

Behavior:
- Prompts the user for an explicit intention:
  ```
  🎯 What are you going to do now?
  > _
  ```
- The user may take as much time as needed to reflect before answering.
- **The session start timestamp is recorded when the user validates the intention (presses Enter), not when the prompt is displayed.**
- Records:
  - the intention,
  - the session start timestamp.
- Sets an internal **minimum session duration** of 25 minutes.
- No visible timer is started.
- The terminal may be closed immediately after.

---

### `focus status`

Checks whether the minimum session duration has been reached.

Behavior:
- Computes elapsed time since session start.

If elapsed time is **less than 25 minutes**:
```
❌ Not yet.
```

If elapsed time is **greater than or equal to 25 minutes**:
```
✅ You can take a break now.
End the session? (Enter = yes / n = continue)
```

- If the user enters `n`, the session continues unchanged.
- If the user presses Enter, the session is closed.

---

### Session Closure (automatic)

When a session is closed:
- The end timestamp is recorded.
- The actual session duration is computed.
- A single feedback question is asked:

```
🧠 The session was:
1) smooth
2) difficult
3) unclear
> _
```

Optional passive messages may be displayed:
- `difficult` → “Note: the task may have been too broad.”
- `unclear` → “Note: the objective may need clarification.”

No action is required from the user afterward.

---

### `focus help`

Displays:
- Available commands.
- The core rule:
  > “When you sit down, you stay until OK.”
- Storage configuration note:
  - Data is stored in the directory defined by the `FOCUS_DATA_DIR` environment variable.

This command does not modify any state.

---

## Data Storage

- One JSON file is created per day.
- Files contain factual session data only.
- Storage location is defined by the environment variable:
  ```
  FOCUS_DATA_DIR
  ```

### Error Handling

If `FOCUS_DATA_DIR` is:
- not defined,
- points to a non-existent directory,
- or is not accessible,

the program:
- displays a clear error message explaining how to fix the issue,
- exits cleanly,
- writes no data.

No automatic fallback directory is used (by design).

---

## Data Format (Example)

```json
{
  "date": "2026-01-15",
  "planned_sessions": 4,
  "sessions": [
    {
      "intent": "Understand select() timeout behavior",
      "start": "14:05",
      "end": "15:12",
      "planned_min_duration": 25,
      "actual_duration": 67,
      "feedback": "difficult"
    }
  ]
}
```

---

## Explicitly Out of Scope (V1)

- Configurable minimum duration
- Automatic adjustment of session counts
- Performance analytics or statistics
- Notifications or alarms
- Gamification (scores, streaks, achievements)
- Interruption tracking
- Active recommendations
- Parameter management commands

---

## Future Evolutions (Indicative)

These features are intentionally **not implemented in V1**.

### Potential V2
- Optional daily reflection question on first `focus start`
- Gentle suggestion to adjust planned session count
- Passive task decomposition hints
- `focus summary` (daily overview)

### Potential V3
- Advanced cloud synchronization
- Pattern visualization (non-real-time)
- TUI interface
- Compiled version (Go or Rust)

---

## Status

- Specification V1: **validated**
- Implementation: **pending**
