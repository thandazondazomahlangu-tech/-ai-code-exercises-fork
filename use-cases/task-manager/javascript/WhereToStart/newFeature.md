# Exercise 2
Add task: Export to CSV
## Initial Search
No similar feature was found to convert a file to export

## Hypothesis
I think the best place to use this feature would be in cli.js as it deals with the terminal mostly so it easily accessable to this applications and future implements. The terminal also has easy access to fiels so the conversion to csv would be easier to implement in this file.

**no files need adjustment**

### Search Terms
- "export to csv"
- "convert to csv"
- "exports"
- "csv"

## Feature Location Prompt

### Prompt Used
I need to work on adding a task: Convert to CSV in this codebase, but I'm not sure where the code for this feature lives.

My approach so far:
- I've searched for keywords like "export to csv", "convert to csv", "exports", "csv"
- I looked in cli.js which seemed relevant
Can you help me:
1. Evaluate my search approach and suggest improvements
2. Identify which files and directories most likely contain the implementation for this feature
3. Suggest specific search terms or patterns that would be more effective
4. Explain what parts of the feature might be located in different areas of the codebase
5. Recommend a step-by-step investigation process to understand the complete feature flow

Also, what questions could I ask myself as I'm exploring the code to ensure I'm on the right track? What specific patterns should I look for to confirm I've found all the relevant parts?

After your guidance, could you give me a small challenge to test my understanding of how to navigate this feature's code?

### Prompt Response
Comprehensive Navigation Guide for the CSV Feature
1. Evaluation of Your Search Approach ✓
What You Did Well:

Searched for direct keywords ("export to csv", "convert to csv")
Looked at cli.js (correct instinct—UI layer often reveals exposed features)
What Could Be Improved:

Your search was feature-focused rather than architecture-focused—CSV export doesn't exist yet
Better approach: First understand the code structure, then search strategically
You correctly hypothesized cli.js but didn't yet map where the CSV conversion logic belongs
2. Files & Directories Most Likely to Contain CSV Logic
File	Role	Expected Changes
cli.js	Command-line interface	Add export or export-csv command
storage.js	Persistence/file I/O	Add exportToCSV() method (follows existing pattern)
app.js	Business logic	Optional: add exportTasks() method
models.js	Data definitions	No changes needed (already has Task structure)
3. Better Search Terms & Patterns
Instead of searching for "csv", try these sequences:

4. How the Feature Flows Across the Codebase
5. Step-by-Step Investigation Process
Phase 1: Understand Data Structure

Read models.js → What fields does a Task have?
Read storage.js → How are tasks stored/retrieved? (Look for getAllTasks())
Trace: Where does task data originate and how is it accessed?
Phase 2: Identify Integration Points
4. Read cli.js → How are existing commands structured? (Look for program.command() patterns)
5. Compare: What do list, create, delete commands do?
6. Pattern Match: Find similar file-writing operations if any exist

Phase 3: Locate Persistence Patterns
7. In storage.js, find the save() method → This is the model for CSV export
8. Question: Does save() use fs.writeFileSync()? Yes → Use same approach

Phase 4: Determine Ownership
9. Is CSV logic belongs in storage.js (file I/O) or app.js (business logic)?
10. Check: Does app.js expose an getAllTasks() or similar public method?

6. Questions to Ask While Exploring
Ask yourself these during code exploration:

"Who calls this function?" → Trace backwards to see dependencies
"What data does this return?" → Understand the shape of data flowing through
"Where is file I/O happening?" → Look for fs. operations
"What's the pattern for similar features?" → Compare with list, stats, delete commands
"Which layer handles each responsibility?" → CLI? Business Logic? Storage?
"Is there a public API I should use?" → Via TaskManager or TaskStorage?
"What error cases exist?" → File permissions, invalid paths?
7. Patterns to Confirm You've Found Everything
✓ You've found it all when you can answer:

Data Source: "I can get all tasks via this.storage.getAllTasks()"
Transformation: "I can convert task objects to CSV using headers + rows"
Output: "I can write to file using fs.writeFileSync() like the save() method does"
Integration: "I can add a new CLI command in cli.js like the stats command"
End-to-End: "User runs export-tasks --output file.csv → triggers handler → converts tasks → writes file"
8. Your Challenge 🎯
Task: Without looking at any code, answer these:

Data Flow: Where would you retrieve the task data for CSV export—from TaskStorage.getAllTasks() or from TaskManager.listTasks()? Why?
File Writing: Which method in storage.js shows you the exact pattern for writing files? Find it and identify the 2-3 lines you'd need to adapt.
CLI Integration: In cli.js, find one existing command and describe what happens in its .action() callback.
Ownership: Should the CSV formatting logic live in storage.js or a new separate file like formatters.js? Justify your answer.
Completeness Check: What would need to change in app.js to support taskManager.exportToCSV(filename)?
Try these now: Read just storage.js carefully and answer questions 1-2. Then read just one command in cli.js and answer question 3. Post your answers and I'll validate your understanding!

## Findings
### Where to implement the feature
1. CLI Layer (cli.js) — Add a new command (e.g. export-tasks) that users can run from the terminal.
2. Storage Layer (storage.js) — Implement the actual logic to convert tasks to CSV format and write to a file. This keeps file I/O concerns separate from business logic.
3. Optional: Business Logic Layer (app.js) — If you want to keep CLI thin, you could add an exportTasks() method here that orchestrates the retrieval and formatting, but it's not strictly necessary.
### Related components to be affected
- cli.js — for the new command and its handler
- storage.js — for the CSV conversion and file writing logic
### Plan to implement export feature
1. In cli.js, define a new command (e.g. `export-tasks`) using Commander.
2. In the command's action handler, call a new method in storage.js (e.g. `exportToCSV(filename)`) that you will implement.
3. In storage.js, implement `exportToCSV(filename)`:
4. Retrieve all tasks (e.g. via `getAllTasks()`)
5. Convert tasks to CSV format (create headers, iterate over tasks to create rows)
