# Exercise 4: Practical Implementation Planning
## Scenario: Automatic Abandoned Task Rule

**Business Rule:** "Tasks that are overdue for more than 7 days should be automatically marked as abandoned unless they are marked as high priority."

---

## Planning

### 1. Files That Need Modification

#### **models.js** (HIGH PRIORITY)
- **Purpose:** Add new domain concept for "abandoned" state
- **Changes:**
  - Add new `TaskStatus.ABANDONED = 'abandoned'` constant
  - OR add `abandoned: boolean` property to Task class (decision needed)
  - Add helper method `canBeMarkedAsAbandoned()` to Task class that checks:
    - `isOverdue()` returns true (already exists)
    - Days overdue > 7
    - `priority !== TaskPriority.HIGH` (protects high-priority tasks)

#### **storage.js** (HIGH PRIORITY)
- **Purpose:** Retrieve tasks matching the abandonment criteria
- **Changes:**
  - Add `getTasksEligibleForAbandonment()` method that:
    - Returns all tasks where `isOverdue() === true`
    - Filters to those with dueDate older than 7 days
    - Excludes high-priority tasks
    - Excludes already-done or abandoned tasks
  - Add `markTaskAsAbandoned(taskId)` method to transition task to abandoned state

#### **app.js** (HIGH PRIORITY)
- **Purpose:** Implement business logic and orchestrate the abandonment process
- **Changes:**
  - Add `abandonOverdueHighRiskTasks()` public method that:
    - Calls `storage.getTasksEligibleForAbandonment()`
    - Iterates through results and calls `updateTaskStatus(taskId, TaskStatus.ABANDONED)`
    - Returns count of affected tasks for logging
  - Add `updateTaskStatus()` wrapper to handle ABANDONED state transitions
  - Consider: Should we log which tasks were abandoned?

#### **cli.js** (MEDIUM PRIORITY)
- **Purpose:** Expose the abandonment process to users
- **Changes Option A (On-Demand):**
  - Add new command: `program.command('cleanup-abandoned')`
  - Calls `taskManager.abandonOverdueHighRiskTasks()`
  - Displays count of tasks marked as abandoned
  
- **Changes Option B (Automatic Check):**
  - Call `taskManager.abandonOverdueHighRiskTasks()` on startup
  - Call in `listTasks()` before returning results (keeps data fresh)

---

### 2. Outline of Implementation Changes

#### **Step 1: Domain Model Extension (models.js)**
```javascript
// Add to TaskStatus enumeration
const TaskStatus = {
  TODO: 'todo',
  IN_PROGRESS: 'in_progress',
  REVIEW: 'review',
  DONE: 'done',
  ABANDONED: 'abandoned'  // NEW
};

// Add method to Task class
canBeMarkedAsAbandoned() {
  // Rule: overdue + not high priority
  if (!this.isOverdue()) return false;  // Not even overdue yet
  if (this.priority === TaskPriority.HIGH) return false;  // Protected by priority
  
  // Check if more than 7 days overdue
  const daysOverdue = Math.floor(
    (new Date() - this.dueDate) / (1000 * 60 * 60 * 24)
  );
  return daysOverdue > 7;
}
```

#### **Step 2: Data Layer (storage.js)**
```javascript
// Add to TaskStorage class
getTasksEligibleForAbandonment() {
  return Object.values(this.tasks).filter(task => 
    task.canBeMarkedAsAbandoned()
  );
}

// Enhanced updateTask to handle abandoned state
updateTask(taskId, updates) {
  const task = this.getTask(taskId);
  if (task) {
    if (updates.status === TaskStatus.ABANDONED) {
      task.abandonedAt = new Date();  // Track when abandoned
    }
    task.update(updates);
    this.save();
    return true;
  }
  return false;
}
```

#### **Step 3: Business Logic (app.js)**
```javascript
// Add to TaskManager class
abandonOverdueHighRiskTasks() {
  const tasksToAbandon = this.storage.getTasksEligibleForAbandonment();
  const count = tasksToAbandon.length;
  
  tasksToAbandon.forEach(task => {
    this.updateTaskStatus(task.id, TaskStatus.ABANDONED);
  });
  
  if (count > 0) {
    console.log(`[SYSTEM] Marked ${count} task(s) as abandoned`);
  }
  
  return count;
}
```

#### **Step 4: Presentation Layer (cli.js)**
```javascript
// Option A: On-demand command
program
  .command('cleanup')
  .description('Mark overdue tasks as abandoned (7+ days overdue, not high priority)')
  .action(() => {
    const count = taskManager.abandonOverdueHighRiskTasks();
    console.log(`Cleanup complete: ${count} task(s) marked as abandoned.`);
  });

// Option B: Call on startup
// In the taskManager initialization or at the start of main execution:
taskManager.abandonOverdueHighRiskTasks();
```

---

### 3. Questions for Your Team

#### **Architectural Decisions**

1. **When should this rule execute?**
   - [ ] On every startup (automatic hygiene)
   - [ ] On-demand via CLI command (user-triggered)
   - [ ] Both (check on startup AND provide manual command)
   - [ ] Periodically in the background (would need a scheduler)

2. **Should "abandoned" be a new status or a flag?**
   - Current approach: New status in TaskStatus enum
   - Alternative: Keep status as-is, add `abandoned: boolean` property
   - Why this matters: Abandoned affects filtering, reporting, and UI display

3. **What about reverting abandoned tasks?**
   - Can users manually change status back from ABANDONED → TODO?
   - Should there be an "unabandoned" reason/comment?
   - How do we prevent users from just re-abandoning the same task infinitely?

4. **Should high-priority threshold be different?**
   - Current rule: High priority tasks NEVER auto-abandon
   - Alternative: High priority gets extended grace period (14 days instead of 7)
   - What defines "high priority" in your business domain?

5. **How does this affect statistics and reporting?**
   - Should abandoned tasks be excluded from "overdue" counts?
   - Should we have an "abandoned" category in stats?
   - Impact on KPIs and dashboards?

6. **What's the user notification strategy?**
   - Should we email/notify users when their task is about to be abandoned?
   - Should there be a "7-day warning" before auto-abandon?
   - Or is this silent system maintenance?

7. **Audit trail requirements:**
   - Should we track WHO marked a task abandoned (system vs user)?
   - Do we need to log the reason?
   - Do we need `abandonedAt` timestamp (I assumed yes)?

---

## Reflection

### How Did the AI Prompts Help Understanding?

✅ **Understanding Architectural Layers:**
- The three-layer model (CLI → Business Logic → Storage) made it immediately clear where each piece belongs
- Without this, I might have put all logic in cli.js or scattered across files
- Recognizing that each layer has a specific responsibility made the decision obvious

✅ **Domain Model Thinking:**
- Framing this as a "business rule" rather than "code feature" helped identify that this is a new domain concept
- Understanding TaskStatus as a value object (restricted set) made it natural to add ABANDONED status
- Knowing that Task has behavior (isOverdue, markAsDone) made me think about adding a `canBeMarkedAsAbandoned()` method to the Task itself

✅ **Understanding Dependencies:**
- Seeing that TaskManager depends on TaskStorage (not the other way) showed me that TaskManager should orchestrate the abandonment, not TaskStorage
- This prevents the storage layer from making business decisions

✅ **Connection to Features:**
- Understanding how `listTasks()` works helped me see that I could hook abandonment logic there OR in a separate command
- Knowing existing commands helped me design the new CLI command consistently

---

### Aspects Still Uncertain

❓ **Uncertainty 1: State Transition Design**
- Should abandoned be a terminal state (like DONE)?
- Or can abandoned tasks transition back to TODO if user revives them?
- The current code seems to assume tasks flow: TODO → IN_PROGRESS → REVIEW → DONE
- Is abandonment a parallel state or part of this flow?

❓ **Uncertainty 2: When to Check**
- On-demand vs automatic affects system design significantly
- If automatic (on startup), we need to ensure it runs BEFORE CLI commands execute
- If automatic (periodic), we need scheduler infrastructure I haven't seen
- The code doesn't show any scheduler or background job system

❓ **Uncertainty 3: Data Migration**
- Do existing tasks that are already 8+ days overdue get retroactively abandoned?
- Or only new tasks going forward?
- This affects the implementation (might need a migration script)

❓ **Uncertainty 4: Testing Time-Based Logic**
- How do we test "more than 7 days" without manipulating system time?
- Should dueDate be injectable for testing?
- Should we have a `isOverdueByDays(days)` method to test the boundary?

❓ **Uncertainty 5: High Priority Definition**
- Is "high priority" always TaskPriority.HIGH?
- Or should we make it configurable (e.g., HIGH and URGENT never auto-abandon)?
- The business might want different rules later

---

### Next Steps to Deepen Understanding

**Step 1: Code Exploration (Review Complete Methods)**
- [ ] Read entire app.js to see all methods and how they use storage
- [ ] Read entire storage.js to understand all data retrieval patterns
- [ ] Look for any existing time-based or calculated methods (best practices)

**Step 2: Pattern Matching**
- [ ] Find similar business rules in the code (e.g., isOverdue implementation)
- [ ] See how existing statuses are handled in updates
- [ ] Check how statistics method aggregates by status (template for our changes)

**Step 3: Architecture Deep Dive**
- [ ] Trace a complete user command from CLI through all layers (e.g., `delete <id>`)
- [ ] Understand the exact flow of data and state changes
- [ ] Identify any hooks or patterns for system-level operations

**Step 4: Integration Points**
- [ ] Check if there's a main entry point or initialization pattern
- [ ] See if TaskManager is instantiated once or per command
- [ ] Understand when save() is called and how persistence works

**Step 5: Ask Clarifying Questions**
- [ ] Ask team: Is this rule immediate need or future feature?
- [ ] Ask team: What triggers this rule in real usage?
- [ ] Ask team: Are there other similar auto-maintenance rules planned?

**Step 6: Implementation Strategy**
- [ ] Start with models.js (add ABANDONED status and helper method)
- [ ] Add storage.js method to query eligible tasks
- [ ] Add app.js orchestration method
- [ ] Test in isolation with mock data
- [ ] Add CLI integration last (after business logic works)

---

## Key Insights from This Exercise

**1. Business Logic Belongs in the Domain:**
The `canBeMarkedAsAbandoned()` method belongs on the Task itself, not scattered in TaskManager. This keeps the rule close to the data it validates.

**2. Layers Enable Flexibility:**
Because we have separate layers, we can implement the abandonment check as on-demand CLI command OR automatic startup cleanup with minimal changes—just where the method is called.

**3. New Status = New Behavior:**
Adding ABANDONED to TaskStatus isn't just a naming thing—it affects filtering, sorting, reporting, and user experience. It's a first-class domain concept.

**4. Questions Drive Design:**
The unanswered questions above aren't blockers—they're design opportunities. Each answer shapes the implementation. This is why senior developers ask "why" before coding.

