Code Documentation Report
Exercise: Code Documentation Challenge

Selected Code: Task Priority Scoring & Sorting (calculate_task_score & sort_tasks_by_importance)

Language: Python 3.11
1. Original Code Selected
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
    # Calculate scores once and sort by the score
    task_scores = [(calculate_task_score(task), task) for task in tasks]
    sorted_tasks = [task for _, task in sorted(task_scores, reverse=True)]
    return sorted_tasks

    2. Documentation Generated using Prompt 1 (Standard Docstring Format)
Below is the structured docstring generated following Google/PEP 257 Python conventions:
def calculate_task_score(task: Task) -> int:
    """Calculates a dynamic priority score for a given task based on priority level,
    due date proximity, status, tag keywords, and recent activity.

    Args:
        task (Task): The task entity instance to evaluate. Must contain attributes
            `priority`, `due_date`, `status`, `tags`, and `updated_at`.

    Returns:
        int: The calculated numerical priority score. Higher values indicate higher priority.

    Raises:
        AttributeError: If `task` is missing required attributes (e.g., `priority`, `tags`).
        TypeError: If `task.due_date` or `task.updated_at` is not a `datetime` object or None.

    Example:
        >>> task = Task(
        ...     priority=TaskPriority.HIGH,
        ...     due_date=datetime.now() + timedelta(days=1),
        ...     status=TaskStatus.TODO,
        ...     tags=["critical"],
        ...     updated_at=datetime.now()
        ... )
        >>> calculate_task_score(task)
        68  # Base: 40 + Due in 1-2 days: 15 + Tag: 8 + Recent: 5

    Notes:
        - Score calculation is relative to the system's current time (`datetime.now()`).
        - Tag matching is case-sensitive and strictly checks for 'blocker', 'critical', or 'urgent'.
        - Completed tasks (`DONE`) incur a heavy penalty (-50) to push them down list results.
    """
    3. Insights and Improvements Identified using Prompt 2 (Intent & Logic Analysis)
    High-Level Intent
The purpose of this code is to provide a multi-factor priority scoring engine. Rather than relying on static priority fields, it dynamically weights tasks so that overdue items, tasks with critical tags, and recently updated work naturally rise to the top of a user's task list.

Key Logic Breakdown & Assumptions
Priority Base Scaling: Scales priority levels exponentially (1, 2, 4, 6) multiplied by 10 to establish a clear baseline hierarchy.

Time Sensitivity: Rewards urgency by awarding up to 35 points for overdue tasks down to 10 points for tasks due within a week.

Status Penalties: Suppresses inactive tasks (DONE and REVIEW) by reducing their overall point values.
Keyword Sensitivity: Scans task.tags using string matching to boost critical tasks by 8 points.

Activity Recency: Grants a 5-point boost to tasks modified within the last 24 hours.
Identified Weaknesses & Edge Cases
Hardcoded datetime.now(): Makes testing difficult because scores change depending on when the function runs.

Case-Sensitive Tags: If a user tags a task as "Urgent" or "CRITICAL", the string check misses it because it only looks for lowercase "urgent".

Missing Null Check on task.updated_at: Unlike task.due_date, task.updated_at is assumed to always exist. If task.updated_at is None, the function raises an exception.
Sorting Tie-Breaker Error: In sort_tasks_by_importance, if two tasks have identical scores, Python attempts to compare the Task objects directly (task1 < task2), which raises a TypeError if Task doesn't implement comparison methods.

4. Final Combined Documentation Version
Here is the refactored, fully documented code incorporating comprehensive docstrings, inline comments, and safeguards against identified edge cases:

from datetime import datetime
from typing import List, Optional
from models import Task, TaskPriority, TaskStatus

def calculate_task_score(task: Task, current_time: Optional[datetime] = None) -> int:
    """Calculates a numerical priority score for a task to determine display order.

    Higher scores represent higher operational urgency.

    Args:
        task (Task): The task object to evaluate.
        current_time (Optional[datetime]): Reference time for date calculations.
            Defaults to `datetime.now()` if not provided.

    Returns:
        int: Total calculated score.

    Notes:
        - Penalizes completed (-50) and review (-15) tasks to demote them.
        - Case-insensitive matching is applied to tag keywords ('blocker', 'critical', 'urgent').
    """
    if current_time is None:
        current_time = datetime.now()

    # 1. Base Priority Score (10 to 60 points)
    priority_weights = {
        TaskPriority.LOW: 1,
        TaskPriority.MEDIUM: 2,
        TaskPriority.HIGH: 4,
        TaskPriority.URGENT: 6
    }
    score = priority_weights.get(task.priority, 0) * 10

    # 2. Due Date Proximity Bonus (Up to +35 points)
    if task.due_date:
        days_until_due = (task.due_date - current_time).days
        if days_until_due < 0:
            score += 35  # Overdue
        elif days_until_due == 0:
            score += 20  # Due today
        elif days_until_due <= 2:
            score += 15  # Due in 1-2 days
        elif days_until_due <= 7:
            score += 10  # Due in next week

    # 3. Task Lifecycle Penalties
    if task.status == TaskStatus.DONE:
        score -= 50
    elif task.status == TaskStatus.REVIEW:
        score -= 15

    # 4. Critical Keyword Tag Boost (+8 points)
    # Converted to lowercase to ensure case-insensitive matching
    task_tags_lower = {tag.lower() for tag in task.tags} if task.tags else set()
    critical_keywords = {"blocker", "critical", "urgent"}
    if any(keyword in task_tags_lower for keyword in critical_keywords):
        score += 8

    # 5. Activity Recency Boost (+5 points)
    if task.updated_at:
        days_since_update = (current_time - task.updated_at).days
        if days_since_update < 1:
            score += 5

    return score


def sort_tasks_by_importance(tasks: List[Task]) -> List[Task]:
    """Sorts a list of tasks in descending order by their calculated importance score.

    Args:
        tasks (List[Task]): A list of un-sorted Task objects.

    Returns:
        List[Task]: A new list of Task objects ordered from highest score to lowest score.
    """
    # Uses a secondary index key (i) to prevent comparison errors when two tasks have equal scores
    task_scores = [
        (calculate_task_score(task), i, task) 
        for i, task in enumerate(tasks)
    ]
    
    # Sort descending by score
    task_scores.sort(key=lambda item: item[0], reverse=True)
    
    return [task for _, _, task in task_scores]

    5. Reflection & Discussion
Which parts of the documentation were most challenging for the AI?
Unspoken Context: The AI initially could not tell what fields exist on Task (like task.updated_at vs task.due_date) without seeing models.py.

Testing Edge Cases: AI docstring generators often overlook practical testing issues, such as how direct calls to datetime.now() break deterministic unit test assertions.

What additional information was needed in prompts?
Specifying domain types (TaskPriority, TaskStatus, Task) helped generate precise parameter types and realistic code examples.

Prompting explicitly for "edge cases and potential bugs" forced the evaluation of case sensitivity and tuple comparison sorting bugs.

How would you use this approach in your own projects?
Documentation First: Use Prompt 1 to generate baseline PEP 257 docstrings whenever creating new module interfaces or shared utility methods.

Code Review Preparation: Use Prompt 2 prior to submitting pull requests to review legacy or complex functions, identifying missed inline comment opportunities and unhandled None types.
