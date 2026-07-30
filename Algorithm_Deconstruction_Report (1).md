Algorithm Deconstruction Report
Exercise: Algorithm Deconstruction Challenge

Selected Algorithm: Algorithm 1 — Task Priority Sorting Algorithm

Language: Python 3.11

Date: July 2026

1. Algorithm Breakdown
The algorithm measures how important a task is by calculating a dynamic numerical score. Higher scores mean higher priority, allowing tasks to be sorted from most urgent to least urgent.

Step-by-step Scoring Breakdown (calculate_task_score)
Base Priority Points

Converts enum priority levels into base scores multiplied by 10:

LOW = 10 points
MEDIUM = 20 points

HIGH = 40 points

URGENT = 60 points

Due Date Proximity

Compares the task's due date against the current time:

Overdue (< 0 days): +35 points

Due today (0 days): +20 points

Due in 1–2 days: +15 points

Due in 3–7 days: +10 points

Status Penalty

Deducts points to move non-active tasks down the list:

DONE: -50 points

REVIEW: -15 points

Tag Keyword Boost

Adds +8 points if any task tag matches "blocker", "critical", or "urgent".

Recency Boost

Adds +5 points if the task was updated in the last 24 hours (days_since_update < 1).

Sorting Logic (sort_tasks_by_importance & get_top_priority_tasks)
Decorate-Sort-Undecorate Pattern: sort_tasks_by_importance creates pairs of (score, task), sorts them in descending order (reverse=True), and then extracts just the sorted task objects. This ensures each task's score is calculated only once rather than repeatedly during comparison steps.

Top N Filtering: get_top_priority_tasks takes the sorted list and slices the top items using Python list slicing [:limit] (defaulting to 5).

Visual Scoring Flow
[ Task Input ]
      │
      ▼
┌──────────────────────────────────────────────┐
│ Base Score = Priority Weight × 10             │ (LOW: 10 | MED: 20 | HIGH: 40 | URGENT: 60)
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│ Due Date Adjustment                          │ (Overdue: +35 | Today: +20 | 1-2 days: +15 | 3-7 days: +10)
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│ Status Penalty                               │ (DONE: -50 | REVIEW: -15 | TODO/IN_PROGRESS: 0)
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│ Tag & Recency Boosts                         │ (Critical Tag: +8 | Updated < 24h: +5)
└──────────────────────┬───────────────────────┘
                       │
                       ▼
[ Final Task Score Output ]


Insights and Key Learning Points
Efficiency via Single-Pass Scoring: Calculating the score before sorting ([(calculate_task_score(t), t) for t in tasks]) keeps the operation fast and avoids running the scoring function multiple times for a single task during comparisons.
Deduction vs. Removal: Completed tasks aren't removed from the list entirely; they receive a large negative penalty (-50). This allows them to stay in the system while naturally sinking to the bottom.
Layered Scoring System: Combining several factors (priority level, deadline, status, tags, activity) creates a flexible sorting rule that reflects real-world work urgency better than sorting by due date alone.

Reflection Questions
How did the AI's explanation change your understanding of the algorithm?
It highlighted that task priority in this system isn't static. Even a LOW priority task can jump ahead of a MEDIUM priority task if it is overdue and tagged as a "blocker".
What aspects were still difficult to understand after the explanation?
Edge cases where penalties and boosts cancel each other out. For example, an URGENT task (+60) that is DONE (-50) ends up with a score of 10—matching a standard, non-due LOW priority task (+10).
How would you explain this algorithm to another junior developer?
"Think of it like a points leaderboard in a game. Every task starts with base points according to its priority level. It earns bonus points if it's due soon, tagged as critical, or recently edited. If a task is completed, it gets a heavy point penalty so it drops to the bottom of the board. Finally, we line up all tasks from highest score to lowest."
Did you test this understanding against AI?
Yes. I asked hypothetical questions such as: "What score would an URGENT task get if it was due today and marked DONE?"

Base: 60

Due Today: +20

Done: -50

Total Score: 30

Calculating this manually and checking against the logic confirmed how the mathematical weighting behaves.
How might you improve the algorithm based on your understanding?
Remove Dynamic Time Dependency (datetime.now()):

Calling datetime.now() directly inside calculate_task_score makes unit testing difficult because the score changes depending on when the test runs. Passing current_time as an optional parameter makes testing consistent.
Case-Insensitive Tag Matching:

Currently, tags are checked using exact string matching ("urgent"). If a user enters "Urgent" or "CRITICAL", the boost is missed. Converting tags to lowercase fixes this:
tag_set = {tag.lower() for tag in task.tags}
if any(keyword in tag_set for keyword in ["blocker", "critical", "urgent"]):
    score += 8
Deterministic Tie-Breaking:

If two tasks yield identical scores, Python falls back to comparing the task objects themselves, which can raise an error if comparison operators aren't defined. Adding creation date as a secondary sorting key ensures predictable ordering.
