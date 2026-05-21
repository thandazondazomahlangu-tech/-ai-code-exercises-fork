# Reflection

## Review and Consolidated Understanding
I reviewed the journal and the code analysis related to task creation, prioritization, and completion. The application uses a CLI layer for user input, an app layer for business logic, a model layer for task domain behavior, and a storage layer for persistence. This separation helps the app handle commands, validate or transform data, apply domain rules, and persist changes independently.

## 3–5 Minute Presentation

### High-level Application Architecture
- `cli.js`: receives terminal commands and translates user input into app calls.
- `app.js`: orchestrates core features, validates inputs, and coordinates models and storage.
- `models.js`: defines the `Task` behavior and encapsulates domain logic like marking done or pending.
- `storage`: persists tasks and serves as the source of truth for task records.

### How the Three Key Features Work
- **Task creation**
  - `cli.js` parses a create command.
  - `app.js` validates fields like due date and constructs a `Task`.
  - `storage.addTask(task)` saves the task and returns its ID.
- **Prioritization**
  - `cli.js` accepts a priority update command.
  - `app.js` forwards the priority change to storage.
  - The priority is stored as a numeric enum-like value, and CLI display maps it to symbols.
- **Completion**
  - `cli.js` runs the complete command with a task ID.
  - `app.js` either updates storage directly or uses `Task.markAsDone()` for the done transition.
  - The status change is persisted through `storage.updateTask()` or `storage.save()`.

### One Interesting Design Pattern or Approach
The most interesting pattern is the layered separation between CLI, app logic, domain model, and persistence. This structure enables the model to own task behavior while the storage layer remains responsible for saving state, even though some paths currently bypass the model.

### What I Found Most Challenging
I found it challenging to determine whether the model methods were actually used during completion because the code shows both a direct storage update path and a model-driven path. The prompts helped by highlighting the discrepancy between `updateTaskStatus()` and the `markAsDone()` / `markAsPending()` methods, making it clearer that there may be an architectural mismatch or dead code.
