# Exercise 3: Mapping Data Flow
## Entry point and components involved when marking task as complete
Entry point is at app.js or cli.js
1. cli.js receives the command to mark a task as complete (e.g. `task-manager complete <task_id>`)
2. cli.js parses the command and extracts the task ID
3. cli.js calls a method in app.js (e.g. `taskManager.markTaskAsDone(taskId)`)
4. app.js receives the task ID and calls a method in models.js to update the task status (e.g. `task.markAsDone()`)
5. models.js updates the task's status to "done" and returns the updated task object

## Code that handle state changes when marking a task as complete
In app.js:
```javascriptupdateTaskStatus(taskId, newStatusValue) {
    if (newStatusValue === 'done') {
      return this.storage.updateTask(taskId, { status: newStatusValue });
    } else if (newStatusValue === 'pending') {
      return this.storage.updateTask(taskId, { status: newStatusValue });
    } else {
      console.error("Invalid status value. Use 'done' or 'pending'.");
      return false;
    }
  }
```
In models.js:
```javascriptmarkAsDone() {
    if (this.status === 'done') {
      console.warn("Task is already marked as done.");
      return false;
    } else if (this.status === 'pending') {
      this.status = 'done';
      return true;
    } else {
      console.error("Invalid task status. Cannot mark as done.");
        return false;
    }
  }
markAsPending() {
    if (this.status === 'pending') {
      console.warn("Task is already marked as pending.");
      return false;
    } else if (this.status === 'done') {
      this.status = 'pending';
      return true;
    } else {
      console.error("Invalid task status. Cannot mark as pending.");
      return false;
    }
  }
```
## Prompt
### Prompt Used
I need help understanding how data flows through our JavaScript, CLI, Node.js application, specifically for the marked a s complete functionality.

What I know:
The feature starts at cli.js
It seems to involve these files
cli.js -> app.js -> models.js
Here are the key code snipets:

In app.js:
```javascriptupdateTaskStatus(taskId, newStatusValue) {
    if (newStatusValue === 'done') {
      return this.storage.updateTask(taskId, { status: newStatusValue });
    } else if (newStatusValue === 'pending') {
      return this.storage.updateTask(taskId, { status: newStatusValue });
    } else {
      console.error("Invalid status value. Use 'done' or 'pending'.");
      return false;
    }
  }
```
In models.js:
```javascriptmarkAsDone() {
    if (this.status === 'done') {
      console.warn("Task is already marked as done.");
      return false;
    } else if (this.status === 'pending') {
      this.status = 'done';
      return true;
    } else {
      console.error("Invalid task status. Cannot mark as done.");
        return false;
    }
  }
markAsPending() {
    if (this.status === 'pending') {
      console.warn("Task is already marked as pending.");
      return false;
    } else if (this.status === 'done') {
      this.status = 'pending';
      return true;
    } else {
      console.error("Invalid task status. Cannot mark as pending.");
      return false;
    }
  }
```
What I'm trying to understand: 1. What is the complete path data takes from input to output? 2. How and where is state managed throughout this process? 3. What transformations happen to the data at each step? 4. Where are potential points of failure in this data flow? 5. How does the application handle edge cases or errors?
Could you help me create a clear mental model of: 1. The complete data flow diagram 2. Where and how state changes occur 3. How I might debug issues in this flow 4. What I should consider if I need to modify this data flow in the future  Please include any relevant descriptions, design patterns or principles that would help me understand the existing code decisions.
### Prompt Returned
# Mark as complete — data flow analysis

## Critical finding: disconnected model methods

Before anything else, there is a **significant discrepancy** in the code you shared.

The `updateTaskStatus` in `app.js` handles status changes with a direct `storage.updateTask()` call — but it **never calls `markAsDone()` or `markAsPending()`** from `models.js`. Those model methods exist but are bypassed entirely. This means all the guard logic in `models.js` (the "already done" warnings, invalid state checks) has no effect at runtime.

This is either a bug or two different versions of the codebase. Worth confirming which `app.js` is actually running.

---

## 1. Complete data flow: input to output

```
User types: done <task_id>
        |
        v
    cli.js
    Parses command, extracts taskId and hardcodes 'done' as the status string
        |
        | taskId, 'done'
        v
    app.js — updateTaskStatus(taskId, newStatusValue)
    String comparison: is newStatusValue === 'done' or 'pending'?
        |
        |--- 'done'    ---> storage.updateTask(taskId, { status: 'done' })
        |--- 'pending' ---> storage.updateTask(taskId, { status: 'pending' })
        |--- anything else -> console.error(), return false
        |
        v
    storage
    Persists { status: 'done' } to disk/memory, returns true/false
        |
        v
    cli.js
    Prints success or failure message to terminal
```

---

## 2. State management

State lives in **two places** and they can diverge:

| Layer | What it holds | When it updates |
|---|---|---|
| `storage` | The persisted task record | On every `updateTask()` call |
| `Task` object (models.js) | In-memory instance with `this.status` | Only when `markAsDone()` / `markAsPending()` is called — which currently never happens via `app.js` |

Because `app.js` calls `storage.updateTask()` directly rather than going through the model, the `Task` object's in-memory state is **never updated** during a status change. If anything later reads a cached `Task` instance rather than fetching fresh from storage, it will see stale data.

---

## 3. Data transformations at each step

| Step | Transformation |
|---|---|
| cli.js input | Raw string from terminal → `taskId` (string) and `'done'` (hardcoded string) |
| app.js | No transformation — strings passed straight to storage |
| storage.updateTask | Merges `{ status: 'done' }` into the existing task record |
| Return value | `true` (success) or `false` (not found / error) propagates back up |

Notably, **there is no type coercion, validation, or transformation** of the status value in the current `app.js`. It relies entirely on the string matching `'done'` or `'pending'` exactly.

---

## 4. Failure points

### F1 — No input sanitisation in cli.js
The status string passed to `updateTaskStatus` comes directly from CLI parsing. If the command is constructed differently (e.g. passing `'Done'` with a capital D), the string comparison fails silently and returns `false`.

### F2 — Plain string comparison instead of enum
`app.js` compares against raw strings `'done'` and `'pending'` rather than using a `TaskStatus` enum. This means a typo anywhere in the codebase (e.g. `'Done'`, `'complete'`, `'DONE'`) creates a silent failure — no exception, just `false`.

### F3 — `markAsDone()` / `markAsPending()` are dead code
The guard logic in `models.js` — including "task already done" warnings and invalid state checks — is never reached. A task can be marked done twice with no warning.

### F4 — No task existence check before update
`app.js` calls `storage.updateTask()` directly without first checking if the task exists. Whether this is safe depends entirely on `storage.updateTask()`'s implementation — if it silently does nothing on a missing ID, the caller gets a misleading `false` with no explanation.

### F5 — Return value is a bare boolean
`cli.js` receives `true` or `false` with no error detail. When something fails, the user sees a generic failure message with no indication of *why* — invalid ID, invalid status, storage error, or something else entirely.

---

## 5. Debugging guide

### Symptom: command runs but status doesn't change
- Check the exact string being passed from cli.js — log `newStatusValue` at the top of `updateTaskStatus`
- Confirm `storage.updateTask()` is returning `true`
- Check whether the task ID exists in storage before the call

### Symptom: no error thrown but `false` returned
- Add a temporary `console.log` at each branch in `updateTaskStatus` to identify which path executed
- Verify the status string matches `'done'` or `'pending'` exactly (case-sensitive)

### Symptom: task shows old status after update
- Check whether anything is reading from a cached `Task` instance rather than fetching fresh from storage
- Remember: `Task.status` in memory is never updated by the current `app.js` flow

---

## 6. Design patterns at play

**Layered architecture** — cli.js handles I/O, app.js handles business logic, models.js defines the domain, storage handles persistence. The intent is clean separation of concerns.

**Anemic domain model (current state)** — In the current implementation, the `Task` model is effectively a data container. Its methods (`markAsDone`, `markAsPending`) exist but have no callers, so all logic has leaked into `app.js`. This is a common anti-pattern that makes the model harder to test and reason about independently.

**What it should look like** — The richer version (seen in the earlier `app.js` snippet) fetches the task object, calls `task.markAsDone()`, and then calls `storage.save()`. That pattern keeps domain logic in the model and uses storage only for persistence — the intended architecture.

---

## 7. What to consider before modifying this flow

1. **Decide on the source of truth for status** — should it be the `Task` object, or the storage record? The current code treats them as independent, which causes drift.
2. **Replace string literals with a `TaskStatus` enum** — this eliminates an entire class of typo bugs and makes refactoring safer.
3. **Reconnect `markAsDone()` / `markAsPending()`** — route through the model methods so their guard logic actually runs.
4. **Add a task existence check** — `updateTaskStatus` should verify the task exists before attempting an update and return a meaningful error if not.
5. **Consider richer return types** — returning `{ success: boolean, error?: string }` instead of a bare boolean gives the CLI layer enough information to show the user a useful message.

## Task Completion Data Flow Journal

### 1. Data Flow Diagram
- `cli.js` receives user command
- parses `taskId`
- calls `app.js` to update status
- `app.js` receives `taskId` and target status
- applies business logic
- forwards update to persistence
- `models.js` contains task domain logic
- changes task object state from pending to done
- `storage` persists the updated task record
- returns success/failure to `app.js`
- `cli.js` displays result to user

### 2. State Changes During Task Completion
- Initial state: task exists with status = `pending`
- User action: CLI command triggers request
- Business logic: `app.js` determines the update path
- Model state change: `models.js` updates `Task.status = 'done'`
- Persistence: `storage.updateTask(taskId, { status: 'done' })`
- Final state: persisted task record now reflects done

### 3. Potential Points of Failure
- CLI parsing error
  - wrong task ID extracted
  - malformed command input
- Application logic mismatch
  - `app.js` bypasses model guards
  - invalid status string passed
- Domain validation failure
  - model rejects already-done or invalid status
- Persistence failure
  - task ID not found
  - storage write fails
- Poor error visibility
  - only `true`/`false` returned
  - no detailed failure reason surfaced

### 4. How the Application Persists These Changes
- Persistence occurs in the storage layer
- `app.js` delegates final write to `storage.updateTask(...)`
- The storage layer stores the updated task record
- This makes storage the source of truth for task status
- In-memory task state must stay synced with storage to avoid stale state