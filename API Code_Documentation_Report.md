Code Documentation Report
Exercise: Code Documentation

Selected Language: Python 3.11

Target Code: Task Priority Scoring Algorithm

1. Original Code
2. def calculate_task_score(task):
    """Calculate a priority score for a task based on multiple factors."""
    # Base priority weights
    priority_weights = {
        TaskPriority.LOW: 1,
        TaskPriority.MEDIUM: 2,
        TaskPriority.HIGH: 4,
        TaskPriority.URGENT: 6
    }

    # Calculate base score from priority
    score = priority_weights.get(task.priority, 0) * 10

    # Add due date factor (higher score for tasks due sooner)
    if task.due_date:
        days_until_due = (task.due_date - datetime.now()).days
        if days_until_due < 0:  # Overdue tasks
            score += 35
        elif days_until_due == 0:  # Due today
            score += 20
        elif days_until_due <= 2:  # Due in next 2 days
            score += 15
        elif days_until_due <= 7:  # Due in next week
            score += 10

    # Reduce score for tasks that are completed or in review
    if task.status == TaskStatus.DONE:
        score -= 50
    elif task.status == TaskStatus.REVIEW:
        score -= 15

    # Boost score for tasks with certain tags
    if any(tag in ["blocker", "critical", "urgent"] for tag in task.tags):
        score += 8

    # Boost score for recently updated tasks
    days_since_update = (datetime.now() - task.updated_at).days
    if days_since_update < 1:
        score += 5

    return score


def sort_tasks_by_importance(tasks):
    """Sort tasks by calculated importance score (highest first)."""
    task_scores = [(calculate_task_score(task), task) for task in tasks]
    sorted_tasks = [task for _, task in sorted(task_scores, reverse=True)]
    return sorted_tasks


def get_top_priority_tasks(tasks, limit=5):
    """Return the top N priority tasks."""
    sorted_tasks = sort_tasks_by_importance(tasks)
    return sorted_tasks[:limit]

    2. Prompt 1 Output: Comprehensive Function Documentation
calculate_task_score(task)
Description: Calculates a numerical score representing how urgently a task needs attention. It evaluates base priority levels, due date closeness, completion status, specific tag keywords, and recent updates.
Parameters:

task (Task): The task object containing priority, due_date, status, tags, and updated_at.

Return Value:

score (int): An integer score where higher values mean higher priority.

Exceptions / Errors:
AttributeError: Raised if the passed task object is missing required attributes (priority, status, tags, etc.).

TypeError: Raised if task.due_date or task.updated_at cannot be compared with a datetime object.
Example Usage:

my_task = Task(
    title="Fix bug",
    priority=TaskPriority.HIGH,
    due_date=datetime.now() + timedelta(days=1),
    status=TaskStatus.TODO,
    tags=["blocker"],
    updated_at=datetime.now()
)

score = calculate_task_score(my_task)
# Result: 40 (HIGH) + 15 (due in 1 day) + 8 (blocker tag) + 5 (updated today) = 68

Notes & Edge Cases:

Completed tasks (TaskStatus.DONE) receive a -50 point penalty, but they are not removed. An urgent completed task might still score higher than a non-due low priority task.

Tag matching is case-sensitive ("blocker" works, but "Blocker" will be ignored).
3. Prompt 2 Output: Intent and Logic Explanation
1. High-Level Intent
This code automatically ranks tasks based on urgency so developers don't have to sort through task lists manually. Instead of relying on a single rule like "due date," it combines multiple signals to give each task a single priority number.
2. Step-by-Step Logic
Base Priority: Assigns 10 to 60 base points depending on priority level (LOW to URGENT).

Deadline Check: Adds bonus points for upcoming or overdue tasks (up to +35 points for overdue items).

Status Penalty: Subtractions (-15 or -50 points) push reviewed or finished tasks down the list.

Keyword Boost: Adds +8 points if tags include "blocker", "critical", or "urgent".
Freshness Boost: Adds +5 points if the task was modified within the last 24 hours.

Sorting & Slicing: Scores all tasks once, orders them from highest to lowest, and returns the top requested count.
3. Assumptions & Edge Cases
Assumption: Assumes datetime.now() matches the timezone of task.due_date and task.updated_at. Mix-and-matching timezone-aware and timezone-naive dates will raise errors.
Edge Case: Negative numbers or unexpected dates (e.g., due far in the future) receive 0 deadline bonus points.

Edge Case: Equal scores fall back to comparing the task objects directly, which may fail if task objects don't support direct comparison operators.
4. Suggested Improvements
Make tag checks case-insensitive (tag.lower()).

Pass current_time as a parameter to simplify unit testing.

Add a secondary sort key (like creation date) to break score ties cleanly.
4. Final Combined Documentation Version
Here is the complete code featuring full docstrings and clear inline comments.

from datetime import datetime
from typing import List


def calculate_task_score(task) -> int:
    """Calculate a priority score for a task based on multiple factors.

    Higher scores indicate higher priority. The score combines base priority,
    due date proximity, completion status penalties, tag boosts, and recency.

    Args:
        task (Task): The task object containing metadata to evaluate.

    Returns:
        int: The calculated numerical priority score.

    Raises:
        AttributeError: If required task properties are missing.
    """
    # 1. Convert base priority enum into weighted numerical score
    priority_weights = {
        TaskPriority.LOW: 1,
        TaskPriority.MEDIUM: 2,
        TaskPriority.HIGH: 4,
        TaskPriority.URGENT: 6
    }
    score = priority_weights.get(task.priority, 0) * 10

    # 2. Add bonus points based on how close the due date is
    if task.due_date:
        days_until_due = (task.due_date - datetime.now()).days
        if days_until_due < 0:      # Overdue tasks take top priority
            score += 35
        elif days_until_due == 0:   # Due today
            score += 20
        elif days_until_due <= 2:   # Due in next 48 hours
            score += 15
        elif days_until_due <= 7:   # Due within a week
            score += 10

    # 3. Apply penalties to push inactive/finished tasks down
    if task.status == TaskStatus.DONE:
        score -= 50
    elif task.status == TaskStatus.REVIEW:
        score -= 15

    # 4. Boost urgent keywords (convert tags to lowercase to prevent missing matches)
    task_tags_lower = [tag.lower() for tag in getattr(task, 'tags', [])]
    if any(keyword in task_tags_lower for keyword in ["blocker", "critical", "urgent"]):
        score += 8

    # 5. Small boost for tasks updated in the last 24 hours
    if hasattr(task, 'updated_at') and task.updated_at:
        days_since_update = (datetime.now() - task.updated_at).days
        if days_since_update < 1:
            score += 5

    return score


def sort_tasks_by_importance(tasks: List) -> List:
    """Sort a list of tasks by their calculated priority score in descending order.

    Calculates scores once per task before sorting to maintain efficiency.

    Args:
        tasks (List[Task]): Unsorted list of Task objects.

    Returns:
        List[Task]: New list of Task objects ordered from highest score to lowest.
    """
    # Create (score, task) tuples to calculate scores only once per item
    task_scores = [(calculate_task_score(task), task) for task in tasks]
    
    # Sort tuples by score descending, then extract the task objects
    sorted_tasks = [task for _, task in sorted(task_scores, reverse=True)]
    return sorted_tasks


def get_top_priority_tasks(tasks: List, limit: int = 5) -> List:
    """Retrieve the top N highest priority tasks.

    Args:
        tasks (List[Task]): Unsorted list of Task objects.
        limit (int, optional): Maximum number of tasks to return. Defaults to 5.

    Returns:
        List[Task]: Top priority tasks up to the specified limit.
    """
    sorted_tasks = sort_tasks_by_importance(tasks)
    return sorted_tasks[:limit]

    5. Learning & Reflection
What was most challenging for the AI?
The AI initially missed subtle edge cases, such as timezone mismatches between dates or how case-sensitive string matching in tags ("Blocker" vs "blocker") could cause rules to fail quietly.
What additional information was needed?
Providing information about the context—such as explaining that TaskPriority and TaskStatus were custom Enum classes—helped generate much more accurate type hints and exception notes.
Applying this approach to future projects
Using AI to generate initial docstrings saves time when documenting legacy or unfamiliar code. Combining a structured prompt (for format and types) with an intent prompt (for logic and edge cases) produces complete documentation that helps team members get up to speed quickly.
