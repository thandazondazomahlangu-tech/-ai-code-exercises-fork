# Exercise 3
# Domain Model
## Extract domain model from codebase
### Core classes
- TaskStorage
- TaskManager
- TaskPriority (enum for task priority levels)
- TaskStatus (enum for task status)
- Task class


## Initial Understanding
### Simple Diagram
```mermaid
classDiagram
    TaskStorage <|-- TaskManager
    TaskManager o-- Task
    Task : +id
    Task : +title
    Task : +description
    Task : +priority
    Task : +status

    flowchart LR
       A[Task Class] --> B[TaskManager]
       B --> C[TaskStorage]
       C --> D(TaskPriority)
       D --> E(TaskStatus)
```
1. The main Class A is the starting point
2. Class A leads to B which is the TaskManager class that handles the logic of managing tasks
3. TaskManager interacts with C (TaskStorage) which is responsible for data persistence
4. Task C interacts with D and E which are enums for TaskPriority and TaskStatus respectively, defining the possible values for these properties in a task.

## Prompts
### Prompt Used
I'd like you to act as a senior developer who deeply understands our codebase's domain model. I'm a junior developer trying to make sense of the business logic and domain concepts in this application
Here's what I've found in the codebase:
### Core classes
- TaskStorage
- TaskManager
- TaskPriority (enum for task priority levels)
- TaskStatus (enum for task status)
- Task class
### Simple Diagram
```mermaid
classDiagram
    TaskStorage <|-- TaskManager
    TaskManager o-- Task
    Task : +id
    Task : +title
    Task : +description
    Task : +priority
    Task : +status

    flowchart LR
       A[Task Class] --> B[TaskManager]
       B --> C[TaskStorage]
       C --> D(TaskPriority)
       D --> E(TaskStatus)
```
1. The main Class A is the starting point
2. Class A leads to B which is the TaskManager class that handles the logic of managing tasks
3. TaskManager interacts with C (TaskStorage) which is responsible for data persistence
4. Task C interacts with D and E which are enums for TaskPriority and TaskStatus respectively, defining the possible values for these properties in a task.
Could you, as a senior developer:
1. Validate my current understanding, correcting any misconceptions
2. Help me recognize the core domain concepts represented in this code
3. Explain the relationships between these entities in business terms, not just technical relationships
4. Clarify any domain-specific terminology or patterns I might be missing
5. Help me connect these models to actual user-facing features or business processes

Then, please ask me 3-5 questions that would test my understanding of this domain model. These should be questions that make me think about the business logic, not just the code syntax.

Finally, suggest a simple diagram I could sketch to visualize these relationships that would help solidify my understanding.

### Prompt Response
1. Validation & Corrections ✅ / ⚠️
What You Got Right:

✅ Task is the core entity
✅ TaskManager orchestrates business logic
✅ TaskStorage handles persistence
✅ TaskPriority and TaskStatus are domain constraints
Critical Misconceptions to Fix:

⚠️ Relationship Direction: Your diagram shows TaskStorage <|-- TaskManager (inheritance with TaskStorage being the parent). This is backwards.

Reality: TaskManager depends on TaskStorage (composition, not inheritance)
Better notation: TaskManager --> TaskStorage (TaskManager uses TaskStorage)
Why it matters: This is about dependency flow, not class hierarchies. TaskManager is the high-level layer that delegates to TaskStorage.
⚠️ Missing Domain Concepts: You're missing critical attributes that represent business requirements:

tags - How users organize/categorize tasks
dueDate, createdAt, updatedAt, completedAt - Temporal tracking (when things happen)
isOverdue() - Business logic (a task is "overdue" when it's past due date AND not done)
markAsDone() - Explicit state transition with side effects (sets completedAt automatically)
2. Core Domain Concepts (Business Language)
Let me translate the code into real business/product thinking:

Code Concept	Business Concept	Why It Matters
Task	A unit of work	Everything revolves around this—it's what users care about
Priority (1-4)	Urgency signal	Helps teams decide what to tackle first
Status (TODO→IN_PROGRESS→REVIEW→DONE)	Workflow state	Models the journey of work through a team's process
Tags	Flexible categorization	Users can organize by project, team, feature, bug type, etc.
dueDate	Deadline	Creates accountability and urgency
isOverdue()	Business rule	A task is only "overdue" if it has a deadline AND hasn't been completed—this is critical logic
TaskManager	Task coordinator	The "brains" of the system—validates input, applies rules
TaskStorage	Record keeper	Like a filing cabinet—doesn't make decisions, just stores/retrieves
3. Relationships in Business Terms
Real example from the code:

This shows layered architecture:

Presentation Layer (cli.js): "What can the user do?"
Business Logic (app.js): "What are the rules?"
Data Layer (storage.js): "How do we remember?"
4. Domain-Specific Patterns You Should Know
Pattern 1: Value Objects (TaskPriority, TaskStatus)

Pattern 2: Domain Logic Living in the Entity

Pattern 3: State Transitions

Pattern 4: Lazy vs. Active Properties

5. Connecting to User-Facing Features
Here's how the domain model enables real features:

User Goal	Feature	Domain Concepts Used
"Show me what to do today"	list with filters	Task.status, Task.dueDate
"I'm working on this"	status <id> in_progress	TaskStatus enum, Task.update()
"This is urgent"	priority <id> 4	TaskPriority enum, Task.priority
"Mark it done when complete"	status <id> done	Task.markAsDone(), Task.completedAt
"Show stats"	stats	TaskStorage aggregations (getAllTasks, getTasksByStatus)
"Which tasks are late?"	list --overdue	Task.isOverdue() business logic

📊 Improved Domain Model Diagram
Here's a better visualization (corrects your relationship directions):

Key differences from your diagram:

TaskManager --> TaskStorage (dependency arrow, not inheritance)
Added temporal tracking (createdAt, updatedAt, completedAt)
Added tags and methods that represent business logic
TaskStatus and TaskPriority are shown as enumerations
Added method signatures so you see what each layer is responsible for
💡 Mental Model to Carry Forward
Think of it like a restaurant kitchen:

Task = A plate that needs to be prepared (the product)
TaskManager = Head chef (makes decisions, ensures quality, follows recipes)
TaskStorage = Pantry (remembers ingredients, keeps organized records)
TaskStatus = Stage of the order (ordered → cooking → plating → served)
Priority = How urgently the order should be cooked
Understanding these business concepts makes it much easier to extend the system—you'll know where logic belongs and what constraints you need to maintain.

### Prompt Questions
Q1: The "Overdue" Concept

A task with dueDate = May 20 and status = DONE (completed on May 18). Is it overdue? Check the isOverdue() method in the code. Why does the business logic check this.status !== TaskStatus.DONE?

Q2: Tags Design

Why do you think tags are stored as an array tags: [] rather than a single string? What business scenarios would multiple tags enable?

Q3: When Does completedAt Get Set?

In the code, completedAt only gets set when markAsDone() is called. What happens if someone calls updateTaskStatus(taskId, TaskStatus.DONE) directly instead? Is this a bug or intentional? (Hint: look at the code in app.js)

Q4: Data Flow for "Show Me Overdue Tasks"

If a user runs list --overdue, trace the path through all three layers. Where does each layer add value? What would break if you removed TaskManager and called TaskStorage directly from CLI?

Q5: Statistics Aggregation

The getStatistics() method in TaskManager counts tasks by status and priority. Why is this logic in TaskManager rather than in TaskStorage? What business decisions does this enable at the management level?

## Testing Knowledge
### Questions
**Q1**
No it is not overdue, the completed date is before due date and status is marked as done. The isOverdue() method checks if the status is not DONE because a task that is already completed cannot be overdue, regardless of its due date.
**Q2**
Tags are stored in a array to allow for multiple tags to be associated with a single task. This enables users to categorize and organize tasks in more flexible ways, such as by project, team, feature, or bug type.
**Q3**
This is likely intentional. The markAsDone() method not only sets the status to DONE but also records the completedAt timestamp. If someone calls updateTaskStatus(taskId, TaskStatus.DONE) directly, it would change the status but would not set the completedAt timestamp, which could lead to incomplete data about when tasks were actually completed.
**Q4**
When a user runs list --overdue, the CLI layer (cli.js) would parse the command and recognize the --overdue flag. It would then call a method in TaskManager (app.js) that retrieves all tasks from TaskStorage and applies the isOverdue() logic to filter out only those tasks that are overdue. If you removed TaskManager and called TaskStorage directly from CLI, you would lose the business logic encapsulated in TaskManager, such as filtering for overdue tasks, and you would have to implement that logic in the CLI layer, which is not ideal for separation of concerns.
**Q5**
The getStatistics() method is in TaskManager rather than TaskStorage because it involves business logic that aggregates and interprets the raw data of tasks. TaskStorage's responsibility is to store and retrieve data, while TaskManager's role is to apply business rules and provide meaningful insights. By keeping this logic in TaskManager, it allows for more complex calculations and decision-making based on the task data, which can inform management decisions about resource allocation, project progress, and areas that may need attention.