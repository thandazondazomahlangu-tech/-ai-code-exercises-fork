# Exercise One: Feature works, task creation and update

## Related files
- app.js
- cli.js
- models.js

## Propt
### Prompt used
I am trying to understand the task creation and status update of a project, it works with Javascript and a bit of Node.js and CLI.
The feature seems to allow the user to create a new task and update its completion status of the task manager app 

Here are the key feature:
app.js- Main entry point
cli.js- Handles terminal side
models.js- handles logic for the tasks

Here are the main code snipets:

```javascript
 updateTaskStatus(taskId, newStatusValue) {
    if (newStatusValue === TaskStatus.DONE) {
      const task = this.storage.getTask(taskId);
      if (task) {
        task.markAsDone();
        this.storage.save();
        return true;
      }
      return false;
    } else {
      return this.storage.updateTask(taskId, { status: newStatusValue });
    }
  }
```


```javascript
createTask(title, description = "", priorityValue = 2, dueDateStr = null, tags = []) {
    const priority = priorityValue;
    let dueDate = null;

    if (dueDateStr) {
      try {
        dueDate = new Date(dueDateStr);
        if (isNaN(dueDate.getTime())) {
          throw new Error("Invalid date");
        }
      } catch (error) {
        console.error("Invalid date format. Use YYYY-MM-DD");
        return null;
      }
    }

    const task = new Task(title, description, priority, dueDate, tags);
    const taskId = this.storage.addTask(task);
    return taskId;
  }
```

### Prompt response
# Task Creation and Status Update Flow

## Overview

The task manager splits responsibilities across three files:

- **`cli.js`** — parses terminal input and calls app-level functions
- **`app.js`** — contains `createTask()` and `updateTaskStatus()` business logic
- **`models.js`** — defines the `Task` model and its methods (e.g. `markAsDone()`)

---

## `createTask()`

```javascript
createTask(title, description = "", priorityValue = 2, dueDateStr = null, tags = []) {
  const priority = priorityValue;
  let dueDate = null;

  if (dueDateStr) {
    try {
      dueDate = new Date(dueDateStr);
      if (isNaN(dueDate.getTime())) {
        throw new Error("Invalid date");
      }
    } catch (error) {
      console.error("Invalid date format. Use YYYY-MM-DD");
      return null;
    }
  }

  const task = new Task(title, description, priority, dueDate, tags);
  const taskId = this.storage.addTask(task);
  return taskId;
}
```

### What it does

1. **Validates the due date** — wraps `new Date(dueDateStr)` in a try/catch and also checks `isNaN(dueDate.getTime())`. This catches both thrown errors and silently invalid dates (e.g. `new Date("banana")` returns an invalid Date object rather than throwing).
2. **Constructs a `Task` object** — passes the validated fields into the `Task` model constructor.
3. **Persists via storage** — calls `storage.addTask(task)` and returns the new `taskId`.

### Important edge case

If the date is invalid, `createTask` returns `null`. The caller in `cli.js` should check for this before confirming a task to the user.

---

## `updateTaskStatus()`

```javascript
updateTaskStatus(taskId, newStatusValue) {
  if (newStatusValue === TaskStatus.DONE) {
    const task = this.storage.getTask(taskId);
    if (task) {
      task.markAsDone();
      this.storage.save();
      return true;
    }
    return false;
  } else {
    return this.storage.updateTask(taskId, { status: newStatusValue });
  }
}
```

### What it does

The function splits into two paths depending on the incoming status:

| Status value | Path taken |
|---|---|
| `TaskStatus.DONE` | Fetch task → call `task.markAsDone()` → call `storage.save()` |
| Any other status | Call `storage.updateTask(taskId, { status: newStatusValue })` directly |

### Why `DONE` is handled differently

The `DONE` branch uses a three-step pattern — `getTask()` → `markAsDone()` → `save()` — rather than a simple field update. This suggests `markAsDone()` on the model does more than flip a status field. It likely:

- Sets a `completedAt` timestamp
- Runs pre-completion validations
- Triggers side effects that a plain `updateTask({ status: 'done' })` would bypass

---

## Flow Summary

```
cli.js
  │
  ├── create command ──► createTask()
  │                         │
  │                         ├── validate date
  │                         ├── new Task(...)
  │                         └── storage.addTask() ──► return taskId
  │
  └── update command ──► updateTaskStatus()
                            │
                            ├── status === DONE?
                            │     YES → storage.getTask()
                            │              └── task.markAsDone()
                            │                    └── storage.save()
                            │
                            └── NO → storage.updateTask({ status })
```

---

## Key Takeaways

- `createTask` is **defensive** — it handles both thrown errors and invalid Date objects.
- `updateTaskStatus` uses a **model method** (`markAsDone`) for the `DONE` transition, keeping domain logic in `models.js` rather than leaking it into `app.js`.
- The `storage.save()` call is **explicit** in the `DONE` path but delegated inside `storage.updateTask()` for all other statuses — worth confirming this symmetry is intentional.

## Main feature
### Main Components
- Task Creation
- Task Status Update    
### Execution Flow
1. User runs a CLI command to create or update a task.
2. `cli.js` parses the command and calls the appropriate function in `app.js`.
3. For task creation:
    - `createTask()` validates the due date, constructs a `Task` object, and saves it via `storage.addTask()`.
4. For status updates:
    - If marking as `DONE`, it retrieves the task, calls `markAsDone()`, and saves.
    - For other statuses, it directly updates the status via `storage.updateTask()`.
### How data is stored and retrieved
- Tasks are stored via the `storage` object, which likely interacts with a file or database.
- `getTask(taskId)` retrieves a specific task, while `addTask(task)` saves a new task and returns its ID. `updateTask(taskId, updates)` modifies existing tasks based on the provided fields.   
### Interesting Patterns
- The use of a model method (`markAsDone()`) for a specific status transition suggests encapsulation of domain logic within the `Task` class.
- The dual validation of the due date in `createTask()` (try/catch + `isNaN()`) is a robust pattern for handling user input that can fail in multiple ways.