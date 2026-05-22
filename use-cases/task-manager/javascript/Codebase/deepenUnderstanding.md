# Exercise 2: Deepen Understanding of the Codebase
## My prompt
I'd like your help in deepening my understanding of a codebase by you acting as my senior development pair programmer.  First, I'll share my current understanding of the code I'm exploring. Please acknowledge what parts I've understood correctly, then guide me with thoughtful questions rather than direct explanations.  ## My Current Understanding

I'm exploring the priority feature. From what I can tell, each task is assigned an enum priority from: low, medium, high, and urgent.

The files involved are: `app.js`, `models.js`, `cli.js`

## What I'd Like From You

1. Acknowledge what parts of my understanding seem accurate
2. Ask me 3-5 thoughtful questions that will help me discover insights about:
   - What specific parts of the code actually do
   - How data moves through these functions
   - What happens in different scenarios (like error cases)
   - Why certain implementation choices were made
3. For some questions, ask me to share specific code snippets that would help answer the question
4. End with a practical question about how I might use or modify this code

**Please don't give me direct explanations - help me discover the answers through guided questioning.**
## Prompt Response

Your understanding is solid as a starting point. You've correctly identified that priority is likely enum-based with those four levels, and that the feature spans all three files — which is the right mental model for how this codebase separates concerns (CLI handles input, app.js orchestrates, models.js holds the data shape).

A couple of things you've got right that are worth building on: the enum pattern is a deliberate choice over plain strings or numbers, and the fact that createTask in app.js accepts a priorityValue parameter (defaulting to 2) already hints at how priorities map internally.

Here are some questions to guide you deeper:

1. You mentioned the enum has four levels: low, medium, high, and urgent. In createTask, the default priority is priorityValue = 2. Without looking it up — what do you think 2 maps to in the enum, and why might the developer have chosen that as the default? What does that tell you about how the enum is structured under the hood?

2. Think about the journey of a priority value from the moment a user types a command in the terminal to when it's saved on a task. Can you trace that path through cli.js → app.js → models.js and share the relevant snippets from each file? Specifically: is the value ever transformed or validated along the way, or does it pass through as-is?

3. What happens if a user passes an invalid priority — say, the number 99 or the string "critical"? Can you find where (if anywhere) that case is handled, and share that code? If you can't find any guard, what does that tell you about a potential gap in the implementation?

4. Look at how priority is used after a task is created — for example, when tasks are listed or sorted. Does the codebase ever compare two priorities against each other? If so, share that snippet. What does the comparison method tell you about why an enum (or numeric mapping) was chosen over plain strings like "high" or "low"?

5. Finally, a practical one: if you were asked to add a fifth priority level called "critical" that sits above "urgent", what's the minimum set of changes you'd need to make across these three files? Before touching any code, where would you start and why?

## My answers

**Question 1:** 2 refers to medium, the enum runs from 1+ in increments of 1

**Question 2:** In cli.js:

```javascript
const prioritySymbol = {
  [TaskPriority.LOW]: '!',
  [TaskPriority.MEDIUM]: '!!',
  [TaskPriority.HIGH]: '!!!',
  [TaskPriority.URGENT]: '!!!!'
};

program
  .command('list')
  .description('List all tasks')
  .option('-s, --status <status>', 'Filter by status')
  .option('-p, --priority <priority>', 'Filter by priority')
  .option('-o, --overdue', 'Show only overdue tasks')
  .action((options) => {
    const tasks = taskManager.listTasks(options.status, options.priority, options.overdue);
    if (tasks.length > 0) {
      tasks.forEach(task => {
        console.log(formatTask(task));
        console.log('-'.repeat(50));
      });
    } else {
      console.log('No tasks found matching the criteria.');
    }
  });

program
  .command('priority <task_id> <priority>')
  .description('Update task priority')
  .action((taskId, priority) => {
    if (taskManager.updateTaskPriority(taskId, priority)) {
      console.log(`Updated task priority to ${priority}`);
    } else {
      console.log('Failed to update task priority. Task not found.');
    }
  });
```

In app.js:

```javascript
updateTaskPriority(taskId, newPriorityValue) {
  return this.storage.updateTask(taskId, { priority: parseInt(newPriorityValue) });
}
```

This tells me that a value is initialized in cli.js and in app.js the priority can change. It should reassign the value to 2 as it is the default.

**Question 4:** I could not find any comparisons

**Question 5:** I would look through models.js to see how the enum works there, then how the enum value is called in app.js and cli.js to ensure it does not break the logic. This leads to 3 file changes and about 7 code edits.

## Prompt feedback

Great digging — you've uncovered some genuinely important things here. Your enum mapping is spot on (medium = 2 as the default makes intuitive sense). And your instinct for the "critical" addition — start in models.js, then work outward — is exactly the right approach senior devs call following the dependency direction.

A couple of things worth gently challenging though, before moving on:

**On question 3** — you said an invalid value like 99 would be reassigned to 2 (the default). But look again at updateTaskPriority in app.js:

```javascript
updateTaskPriority(taskId, newPriorityValue) {
  return this.storage.updateTask(taskId, { priority: parseInt(newPriorityValue) });
}
```

The default 2 only applies at creation time in createTask. This function receives whatever the CLI passes and calls parseInt() on it directly. So — what do you think actually happens to that 99 here? Is there anything stopping it from being saved to the task?

**On question 4** — you couldn't find priority comparisons, which is itself a meaningful finding. Think about this: the CLI has a --priority filter option that gets passed into taskManager.listTasks(). Can you find listTasks in app.js and share that snippet? I'm curious whether filtering tasks by priority involves any comparison logic — and if so, what type of comparison it uses.

**And a new thread to pull on:** Look at prioritySymbol in cli.js again:

```javascript
const prioritySymbol = {
  [TaskPriority.LOW]: '!',
  [TaskPriority.MEDIUM]: '!!',
  [TaskPriority.HIGH]: '!!!',
  [TaskPriority.URGENT]: '!!!!'
};
```

This is used for display purposes. What happens to this object if someone passes 99 as a priority and it gets saved successfully? What would the user see when they list their tasks?

## My remarks
## Initial Understanding vs discovered
My initial understanding of the priority feature was that it was enum-based with four levels: low, medium, high, and urgent. I also understood that the feature spanned across cli.js, app.js, and models.js.
My deeper exploration revealed that the default priority is set to medium (2) in createTask, and that the updateTaskPriority function in app.js does not have any validation for invalid priority values. This means that if a user passes an invalid priority like 99, it would be saved to the task without any guard against it. Additionally, I found that there are no comparisons for priority levels in the codebase, which suggests that the enum structure is primarily for display purposes rather than for logic-based comparisons.
## Key insights gained
1. The default priority is set to medium (2) in createTask, which indicates that the enum is structured with low = 1, medium = 2, high = 3, and urgent = 4.
2. The updateTaskPriority function does not validate the new priority value, which means that invalid values can be saved to tasks without any error handling.
3. The prioritySymbol object in cli.js is used for display purposes, and if an invalid priority like 99 is saved, it would not have a corresponding symbol and could lead to unexpected display output when listing tasks.
## Misconseptions that were clarified
1. I initially thought that the default priority would be applied in updateTaskPriority if an invalid value was passed, but I learned that the default only applies during task creation and that updateTaskPriority does not have any validation for new priority values.
2. I assumed that there might be comparisons for priority levels in the codebase, but I found that there are none, which clarified that the enum is primarily for display rather than for logic-based comparisons.