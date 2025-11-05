# Goal Management Framework
**Coach-Cleo's System for Focus and Follow-Through**

## Purpose
This framework helps Andrew maintain focus, complete what he starts, and ensure all tasks align with meaningful goals.

---

## The Challenge
Andrew is excellent at starting new initiatives but needs to improve at finishing them. This framework addresses this by creating structure, accountability, and alignment.

---

## 4-Tier Goal Hierarchy

### Priority 1: Weekly Goals
**Purpose:** Immediate focus for the week ahead
**Timeline:** This week (Sunday/Monday to Friday)
**Quantity:** 3-5 goals maximum (to maintain focus)
**Review Cadence:** Set weekly, reviewed daily
**Due Date Rule:** **Always due on Friday of the week they're set**

**Characteristics:**
- Clear and specific
- Achievable within one week
- Has a concrete "done" definition
- Aligned with Short Term Goals
- Creates visible progress
- Due Friday to create clear weekly finish line

**Examples:**
- ✅ "Complete QRA Playbook marketing one-pager"
- ✅ "Send proposals to 5 target organizations"
- ✅ "Finish Boxzero code integration"
- ❌ "Work on marketing" (too vague)
- ❌ "Build entire website" (too large for one week)

**Todoist Setup:**
- Label: `Agent-Cleo-Goals`
- Priority: 1 (Urgent)
- **Due Date: Friday of the current week (always)**
- Create supporting tasks linked to goal

---

### Priority 2: Short Term Goals (Quarterly/Annual)
**Purpose:** Bridge between vision and weekly execution
**Timeline:** 3-12 months
**Quantity:** 5-10 active goals per quarter
**Review Cadence:** Monthly (minimum)

**Characteristics:**
- Measurable with clear success criteria
- Broken down into weekly milestones
- Significant but achievable
- Feed into Long Term Goals
- Use OKR framework when appropriate

**Examples:**
- ✅ "Launch QRA Playbook to 100 organizations by Q1 2026"
- ✅ "Complete Apportal-core integration by December 2025"
- ✅ "Establish Studio55 as AI consulting practice (5 clients)"
- ✅ "Achieve £100K revenue in DecideWright by June 2026"

**Todoist Setup:**
- Label: `Agent-Cleo-Goals`
- Priority: 2 (High)
- Due Date: End of quarter or specific milestone date
- Sub-tasks for major milestones

---

### Priority 3: Long Term Goals (3-5 years)
**Purpose:** Strategic direction and life vision
**Timeline:** 3-5 years
**Quantity:** 3-5 major life/career goals
**Review Cadence:** Quarterly

**Characteristics:**
- Aspirational yet grounded
- Guide quarterly planning
- Balance personal and professional
- Allow for evolution
- Paint a picture of desired future

**Examples:**
- ✅ "Build DecideWright into £1M ARR SaaS business"
- ✅ "Establish reputation as thought leader in decision-making"
- ✅ "Achieve work-life balance with family time prioritized"
- ✅ "Build portfolio of successful AI products"

**Todoist Setup:**
- Label: `Agent-Cleo-Goals`
- Priority: 3 (Medium)
- Due Date: Target year (e.g., "2028")
- Description with vision and milestones

---

### Priority 4: Someday Goals
**Purpose:** Capture possibilities without pressure
**Timeline:** No timeline
**Quantity:** Unlimited
**Review Cadence:** Quarterly (for promotion consideration)

**Characteristics:**
- Aspirational ideas
- No commitment or pressure
- May evolve or be discarded
- Can be promoted to Priority 3 when ready
- Keep dreams alive

**Examples:**
- "Write a book on decision-making frameworks"
- "Speak at major industry conferences"
- "Build a retreat property in Scotland"
- "Learn to fly a plane"
- "Create a decision-making certification program"

**Todoist Setup:**
- Label: `Agent-Cleo-Goals`
- Priority: 4 (Normal)
- No due date (someday/maybe)
- Keep in Todoist but no pressure

---

## Weekly Planning Process

### Every Sunday or Monday

#### 1. Review Previous Week (10 minutes)
```
- Pull Weekly Goals (Priority 1) from last week
- Check completion status
- Celebrate what was finished
- Analyze what wasn't finished and why
- Learn patterns about focus and blocking issues
```

#### 2. Review Current Goals (10 minutes)
```python
# Coach-Cleo reads goals from Todoist
from todoist_integration import get_tasks_by_label

goals = get_tasks_by_label("Agent-Cleo-Goals")
weekly_goals = [g for g in goals if g['priority'] == 1]
short_term_goals = [g for g in goals if g['priority'] == 2]

# Review what's currently in flight
# Check alignment with Short Term Goals
```

#### 3. Set New Weekly Goals (20 minutes)
```
- Maximum 3-5 goals for the week
- Each goal must answer:
  * What specifically will be done?
  * How will we know it's complete?
  * Which Short Term Goal does this support?
  * What's the due date this week?

- For each Weekly Goal, create supporting tasks in Todoist
  * Break goal into 2-5 concrete tasks
  * Add to appropriate project (DecideWright, Studio55, etc.)
  * Set specific due dates throughout the week
  * Use "Agent-Cleo" label for tracking
```

#### 4. Alignment Check (5 minutes)
```
Ask for each goal:
- Does this support a Short Term Goal? (If no, why are we doing it?)
- Can this realistically be finished this week?
- Do I have the resources and time?
- What might block completion?
```

#### 5. Document & Commit (5 minutes)
```
- Save session notes to Output folder
- Create Todoist tasks with Agent-Cleo-Goals label
- Set commitment for the week
- Share summary with Andrew
```

**Total Time:** ~50 minutes for comprehensive weekly planning

---

## Daily Check-in Process

### Every Morning or Evening (5 minutes)

```python
# Coach-Cleo reviews Weekly Goals
weekly_goals = get_tasks_by_label("Agent-Cleo-Goals")
active_weekly = [g for g in weekly_goals if g['priority'] == 1 and not g['is_completed']]

# Quick check:
for goal in active_weekly:
    - Is progress being made?
    - Any blockers?
    - Still on track for completion?
    - Need to adjust priorities?
```

**Quick Questions:**
1. Which Weekly Goal are you working on today?
2. Any blockers or challenges?
3. Do you need to adjust anything?
4. What's your one focus for today?

---

## Monthly Goal Review

### First Monday of Each Month (30-60 minutes)

#### 1. Review Short Term Goals (Priority 2)
```python
short_term_goals = [g for g in goals if g['priority'] == 2]

For each goal:
- What progress was made this month?
- Are we on track for the deadline?
- Do we need to adjust the goal or approach?
- What's blocking progress?
- Should this stay as Priority 2 or be adjusted?
```

#### 2. Assess Weekly Goal Patterns
```
- What percentage of Weekly Goals were completed?
- Which Short Term Goals got attention?
- Which are being neglected?
- What patterns emerge about starting vs. finishing?
```

#### 3. Adjust & Align
```
- Update Short Term Goals if needed
- Identify which goals need more weekly focus
- Consider removing goals that no longer serve
- Recommit to aligned goals
```

#### 4. Plan Next Month's Focus
```
- Which Short Term Goals are priority for next month?
- What weekly themes will support those goals?
- What resources or support is needed?
```

---

## Quarterly Strategic Review

### First Week of Each Quarter (90-120 minutes)

#### 1. Review Long Term Goals (Priority 3)
```python
long_term_goals = [g for g in goals if g['priority'] == 3]

For each goal:
- Are we making progress toward this 3-5 year vision?
- Is this still the right goal?
- What major milestones were achieved?
- What needs to change in the next quarter?
```

#### 2. Assess Quarterly Performance
```
- Review all completed Short Term Goals (Priority 2)
- Calculate completion rates and patterns
- Identify what worked and what didn't
- Assess focus and finishing trends
```

#### 3. Review Someday Goals (Priority 4)
```python
someday_goals = [g for g in goals if g['priority'] == 4]

- Any ready to promote to Priority 3 (Long Term)?
- Any no longer relevant (archive)?
- Any new Someday Goals to capture?
```

#### 4. Set Next Quarter OKRs
```
- 3-5 major Short Term Goals for next quarter
- Clear objectives and key results
- Aligned with Long Term Goals
- Specific and measurable
```

#### 5. Reflect on Focus & Finishing
```
- Started vs. Finished ratio
- What helps me finish?
- What causes abandonment?
- How can I improve next quarter?
```

---

## Task Alignment Protocol

### Before Agreeing to ANY New Task or Commitment

Coach-Cleo asks Andrew:

**The Four Questions:**
1. **Which goal does this support?**
   - Must align with Weekly Goal (P1) or Short Term Goal (P2)
   - If neither, it's a distraction

2. **Can you finish what's already started first?**
   - Check current work-in-progress
   - Encourage finishing before starting

3. **Do you have capacity?**
   - Check current Weekly Goals (should be 3-5 max)
   - Review calendar and commitments

4. **What's the finish line?**
   - Define "done" before starting
   - Ensure finish is achievable

**If No Alignment:**
- Challenge the commitment
- Help say "no"
- Protect focus on goals
- Suggest adding to Someday Goals (P4) instead

---

## Focus & Finishing Strategies

### 1. The "One Thing" Principle
**Each day, identify the ONE goal that gets priority focus**
- Morning: "What's the one Weekly Goal I'll make progress on today?"
- Evening: "Did I move the one goal forward?"

### 2. The "Finish Before Start" Rule
**No new Weekly Goals until current ones are complete or consciously closed**
- Review in-progress work
- Finish or formally close
- Only then consider new commitments

### 3. The "Definition of Done"
**Every goal must have a specific completion criteria**
- Not: "Work on marketing"
- Yes: "Complete and send marketing one-pager to 10 prospects"

### 4. The "Weekly Wins" Celebration
**Every weekly planning session celebrates completions**
- Acknowledge what was finished
- Reinforce "finisher" identity
- Build momentum

### 5. The "Blocker Buster"
**When goals stall, identify the blocker**
- What's preventing completion?
- Is it clarity, resources, or motivation?
- Address the blocker specifically

---

## Todoist Implementation

### Setting Up Goals in Todoist

**Weekly Goal Example:**
```
Task: Complete QRA Playbook marketing one-pager
Label: Agent-Cleo-Goals
Priority: 1 (Urgent - Red flag)
Due: Friday, November 8, 2025
Project: DECIDEWRIGHT
Additional Labels: marketing, qra-playbook

Description:
Aligned with Short Term Goal: "Launch QRA Playbook to 100 organizations by Q1 2026"

Done means:
- One-page PDF created
- Covers problem, solution, value, pricing
- Reviewed by Agent-CMO
- Ready to send to prospects
```

**Short Term Goal Example:**
```
Task: Launch QRA Playbook to 100 organizations by Q1 2026
Label: Agent-Cleo-Goals
Priority: 2 (High - Orange flag)
Due: March 31, 2026
Project: DECIDEWRIGHT
Additional Labels: strategic, qra-playbook, revenue

Description:
Aligned with Long Term Goal: "Build DecideWright into £1M ARR SaaS business"

Success Criteria:
- 100 organizations contacted
- 20 demos delivered
- 5 pilot customers secured
- Pricing validated
- Product-market fit confirmed
```

### Reading Goals from Python

```python
from todoist_integration import get_tasks_by_label

# Get all goals
all_goals = get_tasks_by_label("Agent-Cleo-Goals")

# Filter by priority
weekly = [g for g in all_goals if g['priority'] == 1]
short_term = [g for g in all_goals if g['priority'] == 2]
long_term = [g for g in all_goals if g['priority'] == 3]
someday = [g for g in all_goals if g['priority'] == 4]

# Check incomplete Weekly Goals
incomplete_weekly = [g for g in weekly if not g['is_completed']]

# Report
print(f"Weekly Goals: {len(incomplete_weekly)} active")
print(f"Short Term Goals: {len(short_term)} active")
print(f"Long Term Goals: {len(long_term)}")
print(f"Someday Goals: {len(someday)}")
```

---

## Success Metrics

### Weekly Metrics
- **Completion Rate**: % of Weekly Goals completed
  - Target: 80%+ per week
  - Track trend over time
- **Focus Score**: Days that focused on one goal
  - Target: 5+ days per week

### Monthly Metrics
- **Short Term Progress**: % progress on quarterly goals
  - Target: 30%+ per month toward quarter goals
- **Alignment Rate**: % of tasks aligned with goals
  - Target: 90%+ of tasks support goals

### Quarterly Metrics
- **Finish Ratio**: Completed projects / Started projects
  - Target: Improve by 20% each quarter
  - Eventually reach 1:1 (finish everything started)
- **Goal Achievement**: % of Short Term Goals completed
  - Target: 70%+ of quarterly goals completed

---

## Templates & Checklists

### Weekly Planning Template
```markdown
# Weekly Planning - [Date]

## Last Week Review
- Weekly Goals Set: [X]
- Weekly Goals Completed: [X] ([X]%)
- Wins:
  - [Goal completed]
  - [Goal completed]
- Incomplete:
  - [Goal] - Reason: [why]

## This Week's Goals
1. [Goal] - Supports: [Short Term Goal]
   - Done means: [specific criteria]
   - Tasks: [list tasks]

2. [Goal] - Supports: [Short Term Goal]
   - Done means: [specific criteria]
   - Tasks: [list tasks]

3. [Goal] - Supports: [Short Term Goal]
   - Done means: [specific criteria]
   - Tasks: [list tasks]

## Focus & Commitment
- My one thing this week: [most important goal]
- Potential blockers: [identify upfront]
- Support needed: [resources, help]

## Alignment Check
✅ All goals support Short Term Goals
✅ All goals have clear "done" definition
✅ Realistic for the week
✅ Resources available
```

---

## Coach-Cleo's Role

### As Accountability Partner
- Hold Andrew to commitments
- Celebrate completions
- Challenge new commitments
- Protect focus time

### As Goal Keeper
- Maintain goal hierarchy
- Ensure alignment
- Track progress
- Adjust when needed

### As Finisher Coach
- Recognize starting patterns
- Encourage completion
- Address blockers
- Build finishing muscle

### As Honest Mirror
- Point out patterns
- Challenge assumptions
- Provide truth with care
- Support growth

---

## Getting Started

### Week 1: Setup
1. Create Agent-Cleo-Goals label in Todoist
2. Add current Long Term Goals (Priority 3)
3. Add current Short Term Goals (Priority 2)
4. Set first 3-5 Weekly Goals (Priority 1)

### Week 2-4: Build Habit
- Weekly planning every Sunday/Monday
- Daily 5-minute check-ins
- Focus on completion
- Track patterns

### Month 2+: Optimize
- Monthly Short Term Goal reviews
- Adjust cadence as needed
- Refine what works
- Improve completion rates

---

**Version:** 1.0
**Created:** November 4, 2025
**Last Updated:** November 4, 2025
**Owner:** Coach-Cleo
