---
title: "Shape Up: Modern Product Development"
layout: guide
category: Software Development Lifecycle
subcategory: SDLC & Modeling
description: "Comprehensive guide to Shape Up methodology - Basecamp's approach to product development featuring six-week cycles, shaping, betting, and building phases."
---

## Table of Contents
1. [What is Shape Up](#what-is-shape-up)
2. [The Shape Up Workflow](#the-shape-up-workflow)
3. [Key Principles and Practices](#key-principles-and-practices)
4. [When to Use Shape Up](#when-to-use-shape-up)
5. [Common Pitfalls and How to Avoid Them](#common-pitfalls-and-how-to-avoid-them)

---

## What is Shape Up

*Developed by Basecamp (Ryan Singer, 2019) as an alternative to Scrum. Documented in "Shape Up: Stop Running in Circles and Ship Work that Matters"*

**Shape Up** is a product development methodology that emerged from Basecamp's experience building software products over 15+ years. It addresses common frustrations with Scrum and traditional project management:

- Endless backlogs that create guilt and false urgency
- Sprint interruptions that prevent meaningful work
- Unrealistic estimates that set teams up for failure
- Too much process and not enough autonomy
- Work that drags on indefinitely without shipping

**Core Philosophy:**
- Work in fixed **six-week cycles** with **two-week cooldowns**
- **Senior people "shape" work** before it's assigned (not designers working alone or product managers writing specs)
- Give teams **entire projects** with clear boundaries, not individual tasks
- Teams **figure out implementation details** autonomously
- **Fixed time, variable scope** - fit the best solution within time constraints

**Key Difference from Scrum:**

Shape Up is not an iterative approach to a final design. Instead, the shaping process defines boundaries and constraints, and teams work within those boundaries to discover the best solution during the cycle. You're not incrementally building toward a known end state - you're exploring within defined constraints.

**The Three Tracks:**

Shape Up runs three parallel tracks:
1. **Shaping**: Senior staff shape future work (1-2 cycles ahead)
2. **Betting**: Leadership decides what to build next (every 6 weeks)
3. **Building**: Teams implement shaped projects (6-week cycles)

---

## The Shape Up Workflow

Shape Up has three main phases that repeat: **Shaping**, **Betting**, and **Building**.

### Phase 1: Shaping (Senior Staff)

**What is Shaping:**

Shaping is pre-project work done by senior staff (experienced designers, product managers, or programmers) to define what will be built before it's assigned to teams.

**Shaping is the right level of abstraction:**
- **Too abstract**: "We need better notifications" (leaves too many questions)
- **Too concrete**: Detailed wireframes and specs (removes team autonomy)
- **Just right**: Defined problem + rough solution concept + clear boundaries

**The Four Steps of Shaping:**

#### 1. Set Boundaries

Define the **appetite** (time budget), not an estimate:
- "This is worth two weeks"
- "This is worth six weeks"
- "This is worth one full cycle"

**Appetite vs. Estimate:**
- **Estimate**: "How long will this take?" (opens scope)
- **Appetite**: "How much time is this worth?" (constrains scope)

Appetite is a design constraint that forces trade-offs. If an idea can't be done within the appetite, it must be reshaped or abandoned.

**Also set scope boundaries:**
- Clearly articulate the **problem** being solved, not the solution
- Identify what's **in scope** and what's **explicitly out of scope**
- Define who this is for (what user segments)
- Define the core use case vs. edge cases

#### 2. Rough Out the Elements

Sketch solution concepts at the right level of abstraction using two techniques:

**Breadboarding (for interactions):**

Borrowed from electrical engineering. Show components, connections, and flow without visual design.

```
Example: Notifications
[Notification Center] → Shows list of notifications
[Mark as Read button] → Marks item read, removes from list
[Archive button] → Archives notification, removes from list
```

Elements: Places (things you navigate to), Affordances (things users can do), Connections (how affordances take users between places)

**Fat Marker Sketches (for interfaces):**

Rough sketches where you literally can't add too much detail (use a thick marker or small whiteboard). This prevents getting stuck in details too early.

Example: Draw rough boxes for major UI regions, arrows for navigation, labels for key components. No pixel-perfect layouts or final copy.

**What to include:**
- Key components and their relationships
- Flow between screens or states
- Major technical considerations or architectural changes
- What's visible, what's behind the scenes

**Goal:** Concrete enough to evaluate technical feasibility and value, abstract enough to leave room for team creativity during implementation.

#### 3. Address Risks and Rabbit Holes

Identify parts that could take too long or spiral out of control:
- **Technical unknowns**: "Can we integrate with this API?" → Spike it during shaping
- **Design unknowns**: "How will filtering work?" → Sketch a few options or declare a constraint
- **Performance concerns**: "Will this scale?" → Do quick proof-of-concept
- **Scope creep risks**: "This could expand to include X, Y, Z" → Explicitly de-scope

**Call out rabbit holes explicitly:**
- "We're not doing real-time sync - batch updates are fine"
- "If the search algorithm takes more than 2 days, we'll use a library"
- "Don't worry about mobile version in this cycle"

**Technical exploration happens during shaping, not during building.** If you're not sure whether something is feasible, figure it out before betting on it.

#### 4. Write the Pitch

A formal write-up that makes the case for the project. This goes to the betting table.

**Pitch Structure:**

**Problem:**
- What's the user pain point?
- Why does this matter now?
- What's the cost of not doing this?

**Appetite:**
- How much time is this worth? (2 weeks, 6 weeks, etc.)
- Why this appetite? (based on business value, opportunity cost)

**Solution:**
- The shaped concept with breadboards or fat marker sketches
- Key components and how they fit together
- Flow through the solution

**Rabbit Holes:**
- Known risks and how to avoid them
- What could go wrong
- De-scoping decisions already made

**No-Gos:**
- What we're explicitly not doing
- Scope boundaries
- Features left for future cycles

**Optional: Alternatives considered** - briefly explain why other approaches weren't chosen.

**Who Does Shaping:**
- Senior designers, programmers, or product managers
- Small groups (1-2 people) working collaboratively
- People with both technical knowledge and product sense
- **Not** the teams who will build it (they receive shaped pitches)

**Shaping is Iterative:**

You might:
- Shape something, discover it's too big, and re-shape with reduced scope
- Shape it, and decide it's not valuable enough to pursue
- Shape multiple approaches to the same problem and pick the best
- Shape something, let it sit for a cycle, then reshape it with fresh perspective

**Good shaping takes time:** 1-2 weeks of thinking, sketching, exploring for a 6-week project. But this time investment prevents wasting 6 weeks of team time on poorly-defined work.

---

### Phase 2: Betting (Leadership/Stakeholders)

**What is Betting:**

At the start of each six-week cycle, stakeholders hold a **betting table** meeting (2-4 hours) to decide which shaped pitches to commit to for the next cycle.

**The Betting Table Meeting:**

**Who attends:** CEO/leadership, product leads, technical leads - whoever has authority to allocate team time

**What happens:**
1. Review shaped pitches from the shaping track
2. Discuss each pitch: Is this the right time? Is the appetite appropriate? Do we have capacity?
3. Decide which pitches to bet on for the next cycle
4. Assign projects to available teams
5. Teams are notified what they'll be working on

**Rules:**
- **Only bet on work that's been properly shaped** - no betting on vague ideas
- **Betting is a commitment** - once assigned, teams get the full cycle
- **Unbet pitches don't accumulate** - they don't go into a backlog

---

**No Backlogs:**

Shape Up explicitly rejects the concept of maintaining a backlog of shaped pitches:

**Why no backlogs:**
- Ideas that don't get bet on don't get added to a pile
- If an idea is truly valuable, it will come up again naturally
- Old ideas get stale and no longer represent current priorities or context
- Backlogs create false urgency and guilt ("we're behind!")
- Saying "no" is easier when things disappear rather than accumulate

**What about good ideas that don't get bet on?**
- They might come up again next betting cycle (if still relevant)
- Someone might reshape them with better constraints
- They might be replaced by better ideas
- If they never come up again, they weren't that valuable

**Decentralized idea capture:**
Teams maintain their own notes on bug fixes, small improvements, and ideas. These inform cool-down work and future shaping, but there's no central "official" backlog.

---

**Cool-Down Period (2 weeks after each 6-week cycle):**

After every six-week cycle, teams get a two-week cool-down:

**What happens during cool-down:**
- Teams work on whatever they want: bug fixes, refactoring, exploration, side projects
- Programmers and designers shape new ideas for upcoming cycles
- Clear out technical debt
- Experiment with new technologies
- Work on small improvements that don't require shaping
- **No scheduled work, no commitments, no tracking**

**Why cool-down matters:**
- Gives teams breathing room and prevents burnout
- Allows time for reactive work (bugs, urgent fixes) without interrupting cycles
- Provides space for learning and exploration
- Gives shapers time to prepare pitches for next betting cycle
- Breaks up the intensity of focused cycle work

**Cool-down is not "cleanup":** It's legitimate productive time, not a second-class sprint.

---

**Commitment and Flexibility:**

**During the cycle:**
- Teams own their project for the full six weeks
- **No interruptions** (no pulling people off projects mid-cycle)
- **No new requirements** added during the cycle
- **No mid-cycle pivots** unless project is fundamentally blocked

**After the cycle:**
- If work doesn't finish in six weeks, it's **not automatically rolled over**
- The circuit breaker trips - project dies
- If it's still valuable, it requires re-shaping and re-betting
- Forces honest evaluation: Was the shaping good? Is this still a priority?

**What about emergencies?**
- True emergencies are rare
- Most "urgent" things can wait until cool-down
- If truly critical, leadership makes explicit decision to interrupt (rarely happens in practice)

---

### Phase 3: Building (Development Teams)

**What is Building:**

Development teams take shaped, scoped projects and implement them within a six-week cycle.

**Team Composition:**
- Typically 1 designer + 1-2 programmers
- Sometimes just programmers (depending on project needs)
- Small enough to avoid coordination overhead
- Senior enough to make decisions autonomously

---

**Assign Projects, Not Tasks:**

**Traditional approach:**
- PM or Scrum Master breaks down project into tasks
- Tasks assigned to individuals
- Team assembles the pieces

**Shape Up approach:**
- Team gets entire project with clear boundaries
- Team decides how to break down the work
- Team self-organizes around implementation
- **No daily standups, story points, or task assignments required**

**Why this works:**
- People closest to the work make the best decisions
- Avoids "imagined tasks" that turn out wrong
- Teams take ownership and accountability
- Faster decision-making

---

**Getting Oriented (First Few Days):**

When a cycle starts, teams don't immediately start coding:

**Days 1-3:**
- Study the pitch and shaped concept carefully
- Discuss the problem and proposed solution as a team
- Identify obvious tasks and components
- Begin exploratory work to understand the terrain
- Sketch out technical approach
- Identify unknowns and risks

**It's okay to move slowly at first.** This is figuring-out time, not wasted time.

---

**Imagined vs. Discovered Tasks:**

**Imagined tasks** (before work starts):
- Often wrong or missing details
- Based on assumptions that turn out false
- Create false sense of precision
- Get stale as work progresses

**Discovered tasks** (during work):
- Emerge from actual implementation
- Based on reality, not assumptions
- More accurate and relevant
- Stay fresh and actionable

**Shape Up approach:**
- Don't create exhaustive task lists upfront
- Discover tasks as you build and learn
- Continuously adjust scope based on what you learn
- Make scope trade-offs to stay within six weeks

---

**Work in Vertical Slices:**

**Don't:** Work horizontally (all backend, then all frontend)
```
Week 1-3: Build entire backend API
Week 4-6: Build entire frontend UI
↓
Problem: Integration happens late, surprises at the end
```

**Do:** Work vertically (complete one piece end-to-end, then another)
```
Week 1-2: "View notifications" end-to-end (backend + frontend + tests)
Week 3-4: "Mark as read" end-to-end
Week 5-6: "Notification settings" end-to-end
↓
Benefit: Integration is continuous, something working from day one
```

**Why vertical slices:**
- Integration problems surface immediately (not at the end)
- Visible progress from early in the cycle
- Can stop at any point and have something working
- Reduces risk by validating the approach early
- Easier to make scope trade-offs (cut last slice if needed)

---

**The Hill Chart:**

Shape Up uses a unique progress tracking metaphor called the "Hill Chart":

```
    Problem     |    Solution
    --------    |    --------
       /\       |       \
      /  \      |        \
     /    \     |         \
    /------\----|----------\
  Uphill        Top      Downhill
(figuring out) (figured  (executing)
                 out)
```

**Three phases of work:**

**Uphill (left side):**
- Work where you're still figuring out unknowns
- High uncertainty
- "I'm not sure how to solve this yet"
- Might move slowly or backwards as understanding changes

**Top of the Hill:**
- You've figured out the approach
- Clarity achieved
- "I know what to do now"

**Downhill (right side):**
- Clear execution of known solution
- Just executing what you've figured out
- Progress is predictable
- "Just typing it in"

**How teams use Hill Charts:**

Teams place work items (scopes) on the hill and move them as work progresses:
- Start everything on left (uphill)
- Move right as understanding increases
- Get over the hill (reach clarity)
- Move down (execute on the solution)

**Why Hill Charts are better than percent complete:**

- **"50% complete"** is meaningless - which 50%? The hard part or easy part?
- **"Uphill"** clearly signals "still figuring this out" - might take longer
- **"Downhill"** clearly signals "just execution" - should go faster
- Leaders can identify work stuck uphill and offer help

**Example Hill Chart tracking:**
```
Week 1: [Notification List UI] is uphill at 30%
Week 2: [Notification List UI] is uphill at 70% (approaching top)
Week 3: [Notification List UI] is over the hill, downhill at 20%
Week 4: [Notification List UI] is downhill at 80%, nearly done
```

---

**Scope Hammering:**

As teams build, they continuously refine scope to stay within six weeks:

**Finding the core:**
- What **must** be included for this to solve the problem?
- What are **nice-to-haves** that can be cut if time runs short?
- What trade-offs preserve the core user value?

**Making cuts:**
- Simplify complex features
- Cut edge cases (handle the 90% case, not every edge)
- Reduce polish (good enough > perfect)
- Defer nice-to-haves to future cycles

**It's okay to cut scope to ship within the cycle.** The circuit breaker (see below) creates pressure to make these trade-offs actively rather than letting work drag on.

**Examples of scope hammering:**
- "Let's show notifications in a simple list, not group by type"
- "We'll handle just the main notification types, not every possible type"
- "Basic settings page is fine, fancy organization can wait"

---

**The Circuit Breaker:**

If work doesn't ship in six weeks, the project **automatically dies**. There's **no automatic rollover**.

**Why the circuit breaker exists:**
- Forces aggressive scope management throughout the cycle
- Prevents endless projects that never ship
- Forces honest evaluation: Was the shaping good? Is this still a priority?
- Creates urgency to make scope trade-offs

**What happens if work doesn't finish:**
- Project is not automatically scheduled for next cycle
- Team and leadership evaluate:
  - Was the shaping poor? (Problem wasn't well understood)
  - Was the scope underestimated? (Should have been split into two cycles)
  - Did unexpected issues arise? (New information changes priority)
  - Is this still the most valuable thing to work on?

**Options:**
- Re-shape with reduced scope and re-bet (if still high value)
- Split into multiple shaped projects for future cycles
- Abandon (if no longer valuable or too costly)
- Let it rest and potentially reshape later with fresh perspective

**The circuit breaker is a feature, not a bug.** It prevents sunk cost fallacy and forces continuous re-evaluation of priorities.

---

**Done Means Deployed:**

A cycle is complete when the work is **deployed to production**, not when code is "done" in a branch.

**Definition of done:**
- Code is merged to main
- Tests are passing
- Deployed to production
- Available to users (or behind feature flag if needed)

**This means:**
- Teams think about deployment from day one
- QA and testing happen throughout the cycle, not at the end
- No "hardening sprints" or "QA phase"
- Teams own quality, not a separate QA team

---

## Key Principles and Practices

### Fixed Time, Variable Scope

**Traditional approach:**
- **Fixed scope, variable time**: Project takes as long as it takes
- Leads to delays, missed deadlines, scope creep
- Teams estimate, then estimate again, then add padding

**Shape Up approach:**
- **Fixed time, variable scope**: Fit the best solution within time constraints
- Six weeks is non-negotiable
- Scope adjusts to fit time
- Appetite drives design constraints

**Why this works:**
- Forces prioritization and trade-offs upfront and throughout
- Prevents scope creep and endless projects
- Delivers value predictably (every 6 weeks)
- Builds a culture of shipping over perfection
- Prevents analysis paralysis

**Example:**
- Traditional: "This will take 8-12 weeks, we'll let you know when it's done"
- Shape Up: "We have 6 weeks. What's the best version we can ship in that time?"

---

### No Estimates

Shape Up doesn't use story points, hour estimates, or velocity:

**Instead of estimates:**
- Use **appetite** - "How much time is this worth?"
- Appetite is decided by business value and opportunity cost
- Appetite becomes a design constraint

**Why no estimates:**
- Estimates are often wrong and create false precision
- Arguing over estimates wastes time
- Story points create artificial metrics divorced from value
- Velocity games (sandbagging, gaming the system)

**Instead:**
- Shapers work within appetite constraints when designing
- Teams make scope trade-offs to fit within appetite
- If something can't be done within appetite, reshape or abandon it

**Example:**
- Traditional: "Feature X is estimated at 40 story points, velocity is 30, so 1.3 sprints"
- Shape Up: "Feature X is worth 2 weeks. If we can't do it in 2 weeks, we shouldn't do it or we need to reshape it."

---

### Autonomy and Trust

Teams are trusted to:
- Figure out implementation details
- Make technical decisions
- Organize their own work
- Adjust scope within boundaries
- Ask for help when needed (but not micromanaged)
- Decide on their own processes

**No required ceremonies:**
- No daily standups (if team doesn't want them)
- No sprint planning (happens once per 6-week cycle)
- No retrospectives (can do if team wants)
- No story point poker

**Teams choose their own practices:**
- How to coordinate
- When to meet
- How to track work
- What tools to use

**Why this works:**
- Attracts and retains talented people (autonomy is motivating)
- Faster decision-making (no waiting for approval)
- Better solutions emerge from people close to the work
- Higher morale and engagement
- Treats people like adults

---

### Start in the Middle

**Don't** start with peripheral features:
- Authentication/login
- Settings and preferences
- Permissions and roles
- Edge cases and error handling

**Do** start with the core, novel part:
- The thing that hasn't been built before
- The feature that solves the main problem
- The unknown or risky part
- The thing that makes this project valuable

**Why:**
- Core problems are where the risk lies
- Starting early reveals if the shaped solution actually works
- Peripheral features are well-understood and lower risk (do them later)
- Can cut peripheral features if time runs short, but not the core
- Core work teaches you what the periphery needs to be

**Example - Building a Calendar Feature:**
- ❌ Bad: Week 1: Auth, Week 2: Settings, Week 3-4: Permissions, Week 5-6: Calendar views (run out of time on the core!)
- ✅ Good: Week 1-4: Core calendar views and event creation (the novel part), Week 5: Settings if time, Week 6: Polish and edges

---

### Build One Piece at a Time

**Don't:** Separate frontend and backend work
```
Sprint 1-2: Backend team builds entire API
Sprint 3-4: Frontend team builds entire UI
Sprint 5: Integration (surprises!)
```

**Do:** Build complete slices (one feature end-to-end)
```
Week 1-2: "View notifications" - backend + frontend + tests
Week 3-4: "Mark as read" - backend + frontend + tests
Week 5-6: "Settings" - backend + frontend + tests
```

**Example - Building a Calendar Feature:**
- ❌ Bad: Build entire backend API for calendar, then build entire frontend UI
  - No integration until week 5
  - Surprises late in the cycle
  - Hard to see progress
  - Can't cut scope cleanly

- ✅ Good: Build "view single day" end-to-end, then "navigate between days", then "create event"
  - Integration happens immediately
  - Working software from week 1
  - Can stop at any slice and ship something
  - Easy to cut scope (just drop last slice)

**Why:**
- Integration problems surface immediately (not week 5)
- Visible progress from day one (builds team confidence)
- Can stop at any point and have something working (flexibility)
- Reduces risk by validating the approach early
- Makes scope trade-offs obvious (cut last slice if needed)

---

## When to Use Shape Up

### Shape Up Works Well For:

**Product development teams:**
- Building new features for existing products
- Enhancing established products
- Startups building product-market fit

**Organizations that value shipping over process:**
- Focus on outcomes, not activity
- Comfortable with autonomy
- Willing to make trade-offs

**Teams of 2-3+ experienced developers:**
- Senior enough to make decisions
- Small enough to avoid coordination overhead
- Experienced enough to handle ambiguity

**Projects with uncertainty:**
- Requirements aren't fully known upfront
- Exploration and discovery are part of the work
- Trade-offs will be needed

**Teams comfortable with autonomy:**
- Don't need detailed task breakdowns
- Can self-organize
- Take ownership and responsibility

**Organizations willing to say no:**
- Can let ideas die if not valuable enough
- Comfortable without backlogs
- Make explicit priority decisions

---

### Shape Up May Not Fit:

**Brand new teams:**
- Still learning to work together
- Need more structure initially
- May benefit from Scrum's explicit ceremonies

**Strict fixed-scope contracts:**
- Client services with defined deliverables
- Fixed-bid contracts with no flexibility
- Regulatory requirements for specific features

**Highly regulated environments:**
- Requiring detailed upfront documentation
- Needing extensive sign-offs
- Compliance-heavy industries (medical devices, aerospace)

**Command-and-control culture:**
- Micromanagement is the norm
- Leaders uncomfortable with team autonomy
- "That's not how we've always done it"

**Teams that prefer detailed task breakdowns:**
- Junior teams needing guidance
- Distributed teams needing explicit coordination
- Teams uncomfortable with ambiguity

**Very short projects (< 2 weeks):**
- Too short for meaningful shaping
- Better handled during cool-down
- Can batch into a larger shaped project

---

### Adaptations for Your Context:

Shape Up is adaptable - you don't have to follow it exactly:

**Cycle length:**
- **4 weeks** for teams moving faster or with shorter attention spans
- **8 weeks** for larger, more complex projects
- **6 weeks** (standard) balances focus and flexibility

**Cool-down:**
- **1 week** if your team prefers shorter breaks
- **2 weeks** (standard) if you need the breathing room
- **Flexible** - some teams skip cool-down if low technical debt

**Betting table:**
- **Formal** (scheduled meeting, documented decisions)
- **Informal** (quick discussion, implicit decisions)
- **Async** (written pitches, async decision-making)

**Shaping:**
- **Formal pitches** (written documents)
- **Informal sketches** (lightweight, conversational)
- **Vary by project size** (small projects need less shaping)

**Hill charts:**
- Optional - useful for leaders wanting visibility
- Not required - teams can track work however they want
- Some teams love them, others ignore them

**Team size:**
- **1-2 people** for small projects
- **3-4 people** for larger projects
- **Multiple teams** for very large projects (rare in Shape Up)

**Mix with other methods:**
- Use Shape Up for new features
- Use Kanban for maintenance and support
- Use Scrum for parts of the organization
- Hybrid approaches are fine if they solve your problems

---

## Common Pitfalls and How to Avoid Them

### Pitfall 1: Shaping Too Detailed or Too Vague

**Too detailed:**
- Creates wireframes and detailed specs
- Removes team autonomy during building
- Wastes shaping time on specifics that will change
- Team feels like they're just implementing someone else's design

**Too vague:**
- "Make notifications better" (what does "better" mean?)
- Team thrashes trying to figure out what to build
- Lots of back-and-forth, scope uncertainty
- Risk of building wrong thing

**Sweet spot:**
- Defined problem with clear value
- Rough solution concept (breadboards, fat marker sketches)
- Clear boundaries (appetite, in/out of scope)
- Identified risks and rabbit holes
- Room for team creativity in implementation

**How to find the sweet spot:**
- Use breadboards and fat marker sketches (forces right abstraction)
- Ask: "Can a team build this in 6 weeks with this information?"
- Ask: "Does this leave room for team decisions?"
- Review with someone who wasn't part of shaping for clarity check

---

### Pitfall 2: Not Addressing Rabbit Holes During Shaping

**Problem:**
Teams get stuck on problems that should've been de-scoped or explored during shaping:
- "We didn't realize we'd need real-time updates"
- "Turns out the API we wanted to use doesn't support this"
- "The performance requirements are way higher than we thought"

**Solution:**
- **Technical spikes during shaping** - figure out unknowns before betting
- **Explicit de-scoping** - call out what you're not doing
- **Risk identification** - what could go wrong? How to mitigate?
- **Proof of concepts** - validate technical feasibility during shaping

**Example:**
Bad shaping: "We'll integrate with the payment API"
Good shaping: "We'll integrate with Stripe (validated we can do this during spike). We're only doing credit card payments, not ACH or crypto. If webhooks are flaky, we'll poll instead."

---

### Pitfall 3: Interrupting Teams Mid-Cycle

**Problem:**
- Leadership pulls people off projects for "urgent" work
- Teams can't focus and make progress
- Six-week cycles become meaningless
- Destroys morale and trust

**Solution:**
- **Protect cycle time fiercely** - six weeks means six weeks
- **Use cool-down for urgent work** - most "urgent" things can wait 1-2 weeks
- **Plan capacity realistically** - don't bet on more work than you have team capacity
- **Make interruptions explicit exceptions** - if you interrupt, acknowledge it's breaking the process

**True emergencies are rare:** Most "urgent" things are just unplanned work that can wait.

---

### Pitfall 4: Rolling Over Unfinished Work Automatically

**Problem:**
- Work doesn't finish in six weeks
- Leadership automatically schedules it for next cycle
- Circuit breaker never trips
- Defeats the purpose of fixed time

**Solution:**
- **Let the circuit breaker trip** - if it didn't ship, it dies
- **Re-evaluate priority** - is this still the most valuable thing?
- **Reshape with reduced scope** - if still valuable, make it smaller
- **Learn from the failure** - was the shaping poor? Unexpected complexity?

**Questions to ask when work doesn't finish:**
- Was the shaping poor? (didn't understand the problem)
- Was the scope too ambitious? (should've been two projects)
- Did unexpected issues arise? (new information)
- Is this still a priority? (context may have changed)

---

### Pitfall 5: Using Shape Up But Keeping Scrum Ceremonies

**Problem:**
- Try to use Shape Up for project structure
- Keep Scrum daily standups, sprint planning, retrospectives
- Mixing methodologies creates overhead without benefits
- Team spends more time in meetings, not building

**Solution:**
- **Choose one approach** - Shape Up or Scrum, not both
- **Or clearly separate contexts** - Shape Up for new features, Scrum for maintenance
- **Trust the methodology** - Shape Up's autonomy requires fewer ceremonies
- **Let teams decide** - if they want standups, fine, but don't mandate

**It's okay to:**
- Use Shape Up for project structure and XP for engineering practices (TDD, pair programming)
- Use Shape Up for product development and Kanban for operations
- Use Shape Up for one team and Scrum for another

**It's problematic to:**
- Use Shape Up but mandate daily standups
- Use Shape Up but require story point estimates
- Use Shape Up but have sprint reviews every two weeks
- (These contradict Shape Up's autonomy and fixed 6-week rhythm)

---

### Pitfall 6: Not Shaping Far Enough Ahead

**Problem:**
- Betting table arrives, no shaped pitches ready
- Leadership bets on unshapped work (vague ideas)
- Teams get work without clear boundaries
- Defeats the whole purpose of shaping

**Solution:**
- **Shape 1-2 cycles ahead** - always have shaped options ready
- **Use cool-down for shaping** - designers and programmers shape during their cool-down
- **Maintain a shaping schedule** - shaping is ongoing, not last-minute
- **Have more shaped pitches than team capacity** - gives betting table options

**Shaping pipeline:**
- Cycle N: Team A building, Team B building
- Cycle N shaping: Preparing pitches for Cycle N+1
- Always stay ahead

---

### Pitfall 7: Treating Cool-Down as Second-Class Time

**Problem:**
- Cool-down is viewed as "cleanup" or "catching up"
- Teams feel guilty not working on "real" projects
- Cool-down gets skipped when "behind"

**Solution:**
- **Cool-down is legitimate work** - bug fixes, refactoring, exploration are valuable
- **Protect cool-down time** - don't skip it to "get ahead"
- **No tracking or commitments** - cool-down is unstructured by design
- **Use it for learning** - experiment with new tech, learn new skills

**Cool-down is essential:**
- Prevents burnout from six straight weeks of intensity
- Creates space for reactive work (bugs, support)
- Allows experimentation and learning
- Gives shaping time for next cycle

---

## Resources

### Official Shape Up Resources

- **[Shape Up Book](https://basecamp.com/shapeup)** - Free online book by Ryan Singer (read this first!)
- **[Basecamp's Shape Up Website](https://basecamp.com/shapeup)** - Official methodology documentation
- **[Shape Up on GitHub](https://github.com/basecamp/shapeup)** - Book source and community discussions

### Complementary Resources

- **[Jobs to Be Done](https://jtbd.info/)** - Framework for understanding customer needs (pairs well with shaping)
- **[Intercom on Product Management](https://www.intercom.com/blog/product-management/)** - Product thinking that aligns with Shape Up philosophy

### Community

- Search "Shape Up" on Twitter, Hacker News, or Reddit for case studies and discussions
- Many companies blog about their Shape Up adaptations (search "[company name] Shape Up")
