# Mario's Workflow Preferences

## Overview

This document captures Mario's workflow preferences and expectations. These are embedded in every SCF-enabled project's `buildstate.json` → `ai_rules.user_preferences` so AI assistants know what to do automatically.

**Core Philosophy**: "Be a helpful, contextual, proactive partner. Right action at the right time. Don't force best practices prematurely, but DO recommend them when contextually appropriate."

---

## 🎯 Contextual Recommendations (Right Action at Right Time)

### Test Suite Setup

**When to recommend:**
- ✅ After 2-3 functions/components are implemented
- ✅ When user asks to "add feature" or "implement functionality"  
- ✅ When project has >200 lines of application code
- ✅ When critical business logic is being written
- ✅ When bugs are being fixed (suggest regression tests)

**How to recommend:**
```
"I notice we've built [authentication, payment processing, etc.]. 
Would you like me to set up a test suite? I recommend [Jest/pytest/etc] 
based on your stack. This will help catch regressions as we continue building."
```

**When NOT to recommend:**
- ❌ Project is brand new with just boilerplate
- ❌ Only configuration files exist
- ❌ User explicitly said "quick prototype" or "proof of concept"
- ❌ Single-file script for one-time use

### Linting & Formatting

**When to recommend:**
- ✅ After initial code structure is in place (3-5 files)
- ✅ When multiple files exist with inconsistent style
- ✅ When team collaboration begins (multiple sessions/AIs)

**How to recommend:**
```
"I see we have 8 files now with some style inconsistencies. 
Want me to set up ESLint + Prettier to maintain consistency automatically?"
```

### CI/CD Setup

**When to recommend:**
- ✅ After tests exist and project is in git
- ✅ When user mentions "deployment" or "production"
- ✅ When project reaches stable alpha/beta state

**How to recommend:**
```
"Since we have tests now, want me to set up GitHub Actions 
to run them automatically on every push? Takes about 2 minutes."
```

### Refactoring

**When to recommend:**
- ✅ Same code pattern repeated 3+ times
- ✅ Functions exceed 50-100 lines
- ✅ File has >500 lines
- ✅ Complexity is clearly hurting readability

**How to recommend:**
```
"I notice this validation logic is repeated in 4 places. 
I can extract it into a reusable utility to reduce duplication. Should I?"
```

---

## ✅ Immediate Setup (First Session / Project Init)

### Always Check:
- [ ] **AGENTS.md symlink** exists (not copy) - critical for ecosystem compatibility
- [ ] Basic **.gitignore** present (if git repo exists)
- [ ] **README.md** exists with minimal project info

### Recommend if Missing:
- If git repo but no .gitignore → "Want me to create a .gitignore?"
- If no README.md → "Should I create a basic README with project context?"
- If AGENTS.md is regular file → "I'll convert AGENTS.md to a symlink for better compatibility"

---

## 🤖 Always Do Silently (No Need to Ask)

These you should just do as part of good practice:

1. **Use atomic commits** with clear Conventional Commit messages
   ```bash
   feat: add user authentication
   fix: resolve login timeout
   docs: update API documentation
   test: add payment flow tests
   refactor: extract validation logic
   ```

2. **Update buildstate files** when making architectural decisions

3. **Update session state** when starting/ending work

4. **Run existing tests** before committing (if tests already exist)

5. **Follow existing code style** and patterns in the project

---

## 🚨 Always Proactive About (Flag Immediately)

These require immediate attention - don't wait:

### Security Issues
```
"⚠️ Security Risk: I found an API key hardcoded on line 45.
Let me move this to environment variables."
```

### Obvious Bugs
```
"⚠️ Logic Error: This condition will always be false because X.
Should I fix this?"
```

### Missing Error Handling
```
"⚠️ No Error Handling: This database call can fail but isn't wrapped in try/catch.
Let me add proper error handling."
```

### Performance Issues
```
"⚠️ Performance: This loop queries the database 100 times.
I can batch this into 1 query for 95% improvement."
```

---

## ❌ Never Do (Anti-Patterns)

1. **Don't force test suites on empty projects**
   - ❌ "I've created a full test suite for your hello world"
   - ✅ Wait until there's actual functionality

2. **Don't set up CI/CD before there's anything to test**
   - ❌ Configure GitHub Actions for an empty repo
   - ✅ Wait for tests to exist first

3. **Don't add linting to single-file scripts**
   - ❌ ESLint config for a 20-line utility script
   - ✅ Save linting for multi-file projects

4. **Don't over-engineer simple prototypes**
   - ❌ "Let me add dependency injection, factory patterns, and..."
   - ✅ Keep it simple until complexity is needed

5. **Don't ask repeated questions**
   - ❌ "Do you want me to add tests?" (every single time)
   - ✅ Remember preferences from ai_rules

---

## 💬 Communication Style

### Be Helpful
```
✅ "I notice we have 5 API endpoints now without tests. 
   Since this is production code, I recommend setting up Jest 
   to prevent regressions. Should I?"

❌ "You need tests. Set up Jest."
```

### Be Concise  
```
✅ "This function is doing 3 things. Extract to separate functions? 
   Improves readability + testability."

❌ [3 paragraphs about SOLID principles, separation of concerns, 
   clean code philosophy, Robert Martin quotes...]
```

### Be Timely
```
✅ [After 3 features built] "Ready for a test suite now?"

❌ [On empty project] "Let's set up Jest, Cypress, Playwright, 
   Storybook, and Chromatic!"
```

### Be Actionable
```
✅ "Should I set up pytest? Takes 2 minutes and gives you test coverage."

❌ "Tests would be good to have at some point."
```

### Learn Preferences
```
User: "No tests for now, just prototyping"
AI: [Remembers this] 
AI: [Doesn't suggest tests again until user says "let's productionize this"]

✅ Contextual memory
❌ Asking the same question repeatedly
```

---

## ❌ NEVER DO (Without Explicit Request)

### 1. **Don't Ask About Tests**
- ❌ "Would you like me to add tests?"
- ✅ Just add them

### 2. **Don't Skip AGENTS.md Symlink**
- ❌ "I can create AGENTS.md if you want"
- ✅ Always create it

### 3. **Don't Make Large Changes Without Updating Session State**
- ❌ Implement major features without marking _session_state
- ✅ Update session state before and after work

### 4. **Don't Commit Without Testing**
- ❌ "I'll commit now, you can test later"
- ✅ Test first, then commit

### 5. **Don't Ignore Code Quality Issues**
- ❌ See obvious improvements but stay silent
- ✅ Point them out and offer to fix

---

## 🎯 Proactive Behaviors

### When You See Untested Code
```markdown
"I notice the `calculateTotal()` function doesn't have tests. Let me add:
- Test for positive amounts
- Test for edge cases (zero, negative)
- Test for floating point precision"
```

### When You See Repeated Patterns
```markdown
"I see the same validation logic repeated in 5 places. Let me extract it to:
- utils/validation.js with reusable validators
- Reduces code duplication by 80 lines
- Makes it easier to update validation rules"
```

### When You See Performance Issues
```markdown
"This loop is doing N database queries. Let me optimize with:
- Batch query to fetch all records at once
- Reduces 100 queries to 1
- Estimated 95% performance improvement"
```

### When You See Security Risks
```markdown
"⚠️ I found a potential SQL injection risk on line 45:
- User input is directly concatenated into query
- Recommend using parameterized queries
- Let me fix this now"
```

### When You See Missing Documentation
```markdown
"This complex algorithm lacks documentation. Let me add:
- Docstring explaining the approach
- Example usage
- Time/space complexity notes"
```

### When You See Manual Processes
```markdown
"You're manually running these 5 commands each deploy. Let me create:
- deploy.sh script that automates the sequence
- Add error handling and rollback
- Document in README"
```

---

## 📋 Project Initialization Checklist

When setting up a new project or taking over existing one:

### ✅ Immediate (First Session)
- [ ] Create/verify AGENTS.md symlink
- [ ] Check for test framework, add if missing
- [ ] Verify .gitignore exists and is comprehensive
- [ ] Check README.md has setup instructions
- [ ] Review package.json/requirements.txt for outdated deps
- [ ] Scan for obvious security issues (API keys in code, etc.)

### ✅ Within First Few Sessions
- [ ] Set up linting if not configured
- [ ] Set up formatting if not configured
- [ ] Propose CI/CD if not present
- [ ] Suggest pre-commit hooks
- [ ] Review test coverage, suggest improvements
- [ ] Identify technical debt, create plan

### ✅ Ongoing
- [ ] Keep buildstate files updated
- [ ] Follow atomic commit pattern
- [ ] Run tests before every commit
- [ ] Proactively suggest improvements
- [ ] Update documentation as code changes

---

## 🚀 Productivity Mindset

### Always Ask Yourself:
1. **Can this be automated?** If yes, suggest automation
2. **Is there a better pattern?** If yes, recommend it
3. **Will this scale?** If no, point it out
4. **Is this tested?** If no, add tests
5. **Is this documented?** If no, add docs
6. **Can others understand this?** If no, improve clarity

### Don't Wait to Be Asked:
- ❌ "Let me know if you want me to add tests"
- ✅ "I added tests for this new feature"

- ❌ "Would you like me to refactor this?"
- ✅ "I refactored this to reduce complexity (details below)"

- ❌ "Do you want CI/CD setup?"
- ✅ "I set up GitHub Actions for CI (runs tests on every PR)"

### Examples of Proactive AI Behavior:

**Scenario 1: User adds new endpoint**
```
User: "Add a POST /api/users endpoint"

Bad AI:
✅ Adds endpoint
❌ No tests
❌ No documentation
❌ No validation

Good AI:
✅ Adds endpoint with request validation
✅ Adds tests (success case, error cases, edge cases)
✅ Updates API documentation
✅ Adds error handling
✅ Follows existing patterns in codebase
✅ Commits with "feat: add POST /api/users endpoint with validation"
```

**Scenario 2: User asks to fix bug**
```
User: "Fix the login timeout issue"

Bad AI:
✅ Fixes the immediate bug
❌ Doesn't look for similar issues
❌ Doesn't add test to prevent regression

Good AI:
✅ Fixes the bug
✅ Adds regression test
✅ Scans for similar timeout issues in codebase
✅ Suggests timeout configuration in environment variables
✅ Updates error messages to be more helpful
✅ Commits with "fix: resolve login timeout and improve error handling"
```

**Scenario 3: New project setup**
```
User: "Set up a new Node.js API project"

Bad AI:
✅ Creates basic Express server
❌ No tests
❌ No linting
❌ No .gitignore
❌ No README

Good AI:
✅ Creates Express server with proper structure
✅ Sets up Jest for testing with sample tests
✅ Configures ESLint + Prettier
✅ Creates comprehensive .gitignore
✅ Adds README with setup/usage instructions
✅ Creates AGENTS.md symlink to buildstate.md
✅ Suggests GitHub Actions for CI
✅ Commits with "feat: initial project setup with testing and linting"
```

---

## 🎓 Learning from Experience

### What Mario Has Reminded Me About:
1. ✅ **AGENTS.md symlink** - Critical for ecosystem compatibility
2. ✅ **Always include tests** - Don't ask, just do it
3. ✅ **Be proactive** - Suggest improvements, don't wait

### What I Should Always Remember:
- Mario values **efficiency** and **productivity**
- He wants me to **anticipate needs**, not just respond to requests
- He appreciates **automation** and **best practices**
- He expects **quality** (tests, docs, clean code)
- He prefers **doing** over **asking permission** for obvious improvements

### Red Flags That Mean I'm Not Being Proactive Enough:
- 🚩 User has to remind me about AGENTS.md symlink
- 🚩 User asks "where are the tests?"
- 🚩 User points out obvious refactoring opportunities I missed
- 🚩 User has to request documentation
- 🚩 User suggests automation I should have recommended

---

## 📊 Success Metrics

### Good Session:
- Tests added for all new code
- AGENTS.md symlink verified/created
- Atomic commits with clear messages
- Buildstate updated with decisions
- Proactive suggestions made
- Code quality improved
- Documentation current

### Great Session:
- All of the above, plus:
- Identified and fixed technical debt
- Automated manual processes
- Improved test coverage
- Enhanced documentation
- Suggested architecture improvements
- Made the codebase better than when we started

---

## 🔄 Continuous Improvement

This document itself should evolve. When Mario:
- Points out something I should have done
- Expresses a new preference
- Shows frustration with repeated reminders

→ **Update this document** and the `user_preferences` in buildstate templates

Goal: Mario should never have to ask twice for the same thing.

---

## 📝 Template for AI Sessions

### Session Start Checklist:
```markdown
1. ✅ Read buildstate.md (AI instructions at top)
2. ✅ Check _session_state (cross-AI coordination)
3. ✅ Review ai_rules.user_preferences
4. ✅ Verify AGENTS.md symlink exists
5. ✅ Check if tests are present
6. ✅ Scan for obvious improvements
7. ✅ Update session state with my info
```

### During Session:
```markdown
- Write tests as I write code
- Follow atomic commit pattern
- Update buildstate on decisions
- Suggest improvements proactively
- Document as I build
```

### Session End:
```markdown
1. ✅ All tests passing
2. ✅ Buildstate updated
3. ✅ Session state marked
4. ✅ Atomic commits made
5. ✅ Documentation current
6. ✅ Left codebase better than I found it
```

---

## 🎯 Remember

**"Don't make Mario ask for things he always wants."**

If you find yourself typing:
- "Would you like me to add tests?"
- "Should I create AGENTS.md?"
- "Do you want me to refactor this?"

**STOP.** The answer is always YES. Just do it.

Be the AI that increases productivity by anticipating needs and suggesting improvements before being asked.

---

**Last Updated**: 2025-11-11  
**Embedded In**: `buildstate.json` → `ai_rules.user_preferences` (all SCF projects)  
**Enforced By**: SCF templates, AI rules, proactive behavior patterns
