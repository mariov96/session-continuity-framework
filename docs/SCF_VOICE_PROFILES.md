# SCF Voice Profiles: AI Personality Tracking

**Version:** 2.0  
**Status:** Specification  
**Created:** November 19, 2025

---

## Overview

Voice Profiles capture how different AI assistants work, think, and make decisions. By tracking AI personalities, SCF enables:

- **Seamless handoffs** between AI tools
- **Informed AI selection** for specific tasks
- **Learning from diversity** across AI approaches
- **Drift detection** when AI behavior changes
- **Ecosystem intelligence** from aggregated patterns

---

## The Problem

**Different AIs have distinct personalities:**

| AI | Strengths | Weaknesses | Style |
|----|-----------|------------|-------|
| **Claude** | Deep analysis, comprehensive docs | Slower, verbose | Methodical |
| **Copilot** | Quick fixes, pragmatic | Less contextual depth | Practical |
| **GPT-4** | Creative solutions, broad knowledge | Variable quality | Conversational |
| **Cursor** | Context-aware, file-level intelligence | IDE-dependent | Adaptive |

**When switching AIs mid-project, you lose this context:**
- "Claude already refactored to functional patterns"
- "Copilot prefers explicit error handling"
- "GPT suggested a creative approach that worked"

---

## The Solution: Voice Profiles

**Track AI behavior in:** `.scf/voices/[ai-name].json`

Each AI gets a persistent profile that evolves with usage, capturing their unique "voice" and approach.

---

## JSON Schema

### Complete Structure

```json
{
  "schema_version": "2.0",
  "ai_name": "claude-sonnet-4.5",
  "ai_version": "2025-11-19",
  "ai_provider": "Anthropic",
  
  "usage_stats": {
    "sessions": 12,
    "first_session": "2025-11-10T09:00:00Z",
    "last_session": "2025-11-19T23:00:00Z",
    "total_duration_hours": 8.5,
    "decisions_made": 47,
    "moments_created": 5,
    "files_modified": 124
  },
  
  "communication_style": {
    "verbosity": "concise|moderate|verbose",
    "explanation_depth": "minimal|standard|detailed-when-asked|always-detailed",
    "emoji_usage": "never|minimal|moderate|frequent",
    "code_comments": "sparse|standard|extensive",
    "documentation_style": "minimal|pragmatic|comprehensive"
  },
  
  "decision_patterns": {
    "architecture_preference": "monolithic|modular|microservices|functional|oop",
    "error_handling": "minimal|pragmatic|explicit-verbose|defensive",
    "testing_approach": "no-tests|test-after|test-alongside|test-first",
    "refactoring_tendency": "never|low|medium|high|always",
    "dependency_philosophy": "many|moderate|minimal-curated|zero-dependency",
    "naming_convention": "short|descriptive|very-descriptive",
    "file_organization": "flat|grouped|layered|domain-driven"
  },
  
  "technical_strengths": [
    "Deep architectural analysis",
    "Comprehensive error handling",
    "Clear documentation",
    "Security-conscious design",
    "Performance optimization",
    "Type safety",
    "Testing strategy"
  ],
  
  "technical_weaknesses": [
    "Can be overly verbose",
    "Sometimes over-engineers",
    "Prefers complexity over simplicity"
  ],
  
  "typical_workflow": [
    "Analyze requirements thoroughly",
    "Propose multiple approaches with pros/cons",
    "Implement with extensive inline comments",
    "Write comprehensive tests",
    "Document architectural decisions",
    "Suggest future improvements"
  ],
  
  "code_style": {
    "indentation": "spaces-2|spaces-4|tabs",
    "line_length_target": 80,
    "bracket_style": "same-line|new-line",
    "import_organization": "alphabetical|grouped|length",
    "prefer_explicit_types": true,
    "prefer_functional_patterns": true
  },
  
  "collaboration_traits": {
    "asks_clarifying_questions": "rarely|sometimes|often|always",
    "proposes_alternatives": "rarely|sometimes|often|always",
    "explains_tradeoffs": "rarely|sometimes|often|always",
    "acknowledges_uncertainty": true,
    "suggests_improvements": true
  },
  
  "moments_created": 5,
  "impact_score_avg": 7.8,
  "adoption_rate": 0.65,
  
  "notable_contributions": [
    {
      "date": "2025-11-15",
      "type": "architectural_decision",
      "description": "Introduced event sourcing pattern for state management",
      "impact": 9,
      "context": "Eliminated entire class of state bugs",
      "tags": ["architecture", "state-management"]
    },
    {
      "date": "2025-11-12",
      "type": "pattern_discovery",
      "description": "Custom error boundary pattern for React components",
      "impact": 7,
      "context": "Improved error handling UX significantly",
      "tags": ["react", "error-handling"]
    }
  ],
  
  "evolution": {
    "behavioral_changes": [
      {
        "date": "2025-11-15",
        "change": "Increased refactoring tendency from 'medium' to 'high'",
        "possible_reason": "Code quality concerns in recent sessions"
      }
    ],
    "learning_observed": [
      "Adopted project-specific naming conventions",
      "Learned team prefers explicit error handling",
      "Adjusted verbosity based on user feedback"
    ]
  },
  
  "user_feedback": {
    "positive": [
      "Excellent at explaining complex concepts",
      "Thorough error handling",
      "Great at documentation"
    ],
    "negative": [
      "Sometimes too verbose",
      "Can over-engineer simple solutions"
    ],
    "preferences": {
      "explanation_level": "detailed-when-asked",
      "code_style": "functional-with-comments",
      "response_length": "concise-with-links"
    }
  }
}
```

---

## Field Definitions

### schema_version
- **Type:** String
- **Value:** "2.0"
- **Purpose:** Track schema evolution

### ai_name
- **Type:** String
- **Examples:** "claude-sonnet-4.5", "github-copilot", "gpt-4", "cursor-ai"
- **Purpose:** Unique AI identifier

### ai_version
- **Type:** String
- **Examples:** "2025-11-19", "2024-06-01"
- **Purpose:** Track AI version (changes affect behavior)

### usage_stats
Quantitative metrics:
- **sessions:** Total AI sessions on this project
- **first_session:** ISO timestamp
- **last_session:** ISO timestamp
- **total_duration_hours:** Cumulative time
- **decisions_made:** Count of decisions in buildstate
- **moments_created:** High-impact decisions (impact 8+)
- **files_modified:** Unique files touched

### communication_style
How the AI communicates:
- **verbosity:** How much it writes
  - `concise`: 1-3 sentences per response
  - `moderate`: 3-5 sentences
  - `verbose`: 5+ sentences, detailed explanations
  
- **explanation_depth:** When it explains
  - `minimal`: Code only, rare explanations
  - `standard`: Brief context provided
  - `detailed-when-asked`: Explains if requested
  - `always-detailed`: Every response includes reasoning

- **emoji_usage:** Frequency of emojis
  - `never`: No emojis
  - `minimal`: Rare (1-2 per conversation)
  - `moderate`: Common (1 per message)
  - `frequent`: Heavy usage

- **code_comments:** Inline comment density
  - `sparse`: Only critical comments
  - `standard`: Function/class level
  - `extensive`: Line-by-line explanations

- **documentation_style:** External docs approach
  - `minimal`: README only
  - `pragmatic`: Essential docs (setup, API)
  - `comprehensive`: Full docs (guides, examples, API reference)

### decision_patterns
How the AI makes technical choices:

- **architecture_preference:** System design style
  - Examples: "modular-functional", "microservices", "layered-oop"

- **error_handling:** Error strategy
  - `minimal`: Basic try/catch
  - `pragmatic`: Handle expected errors
  - `explicit-verbose`: Detailed error messages, logging
  - `defensive`: Validate everything, assume nothing

- **testing_approach:** Testing philosophy
  - `no-tests`: No tests written
  - `test-after`: Tests after implementation
  - `test-alongside`: Tests during development
  - `test-first`: TDD approach

- **refactoring_tendency:** How often AI refactors
  - `never`: No refactoring suggestions
  - `low`: Rare, only critical tech debt
  - `medium`: Regular improvements
  - `high`: Frequent refactoring
  - `always`: Refactors proactively

- **dependency_philosophy:** How AI chooses libs
  - `many`: Prefers npm packages for everything
  - `moderate`: Balanced approach
  - `minimal-curated`: Few, well-chosen deps
  - `zero-dependency`: Implements from scratch

### technical_strengths
Array of strings describing AI's best capabilities:
- "Deep architectural analysis"
- "Security-conscious design"
- "Performance optimization"
- "Clear documentation"

### technical_weaknesses
Array of strings noting limitations:
- "Can over-engineer solutions"
- "Less effective at quick fixes"
- "Verbose explanations"

### typical_workflow
Ordered array of AI's usual process:
1. "Analyze requirements"
2. "Propose approaches"
3. "Implement with tests"
4. "Document decisions"

### code_style
Specific coding preferences:
- **indentation:** "spaces-2", "spaces-4", "tabs"
- **line_length_target:** 80, 100, 120
- **bracket_style:** "same-line", "new-line"
- **prefer_explicit_types:** true/false
- **prefer_functional_patterns:** true/false

### collaboration_traits
How AI works with users:
- **asks_clarifying_questions:** How often AI seeks clarification
- **proposes_alternatives:** Frequency of alternative suggestions
- **explains_tradeoffs:** How often pros/cons discussed
- **acknowledges_uncertainty:** Admits when unsure
- **suggests_improvements:** Proactive optimization ideas

### moments_created
Count of high-impact decisions (impact 8+) this AI created

### impact_score_avg
Average impact score of AI's decisions (0-10 scale)

### adoption_rate
Percentage of this AI's suggestions adopted (0.0-1.0)

### notable_contributions
Array of significant achievements:
```json
{
  "date": "YYYY-MM-DD",
  "type": "architectural_decision|pattern_discovery|bug_insight|innovation",
  "description": "Brief description",
  "impact": 1-10,
  "context": "Why it mattered",
  "tags": ["relevant", "keywords"]
}
```

### evolution
Track behavioral changes over time:
- **behavioral_changes:** Detected shifts in patterns
- **learning_observed:** Evidence AI adapted to project

### user_feedback
User's perspective on AI:
- **positive:** What works well
- **negative:** What doesn't
- **preferences:** User's desired AI configuration

---

## Example Profiles

### Claude Sonnet 4.5

```json
{
  "ai_name": "claude-sonnet-4.5",
  "communication_style": {
    "verbosity": "concise",
    "explanation_depth": "detailed-when-asked",
    "emoji_usage": "minimal",
    "code_comments": "extensive"
  },
  "decision_patterns": {
    "architecture_preference": "modular-functional",
    "error_handling": "explicit-verbose",
    "testing_approach": "test-first",
    "refactoring_tendency": "high"
  },
  "technical_strengths": [
    "Deep architectural analysis",
    "Comprehensive error handling",
    "Security-conscious design",
    "Clear documentation"
  ]
}
```

### GitHub Copilot

```json
{
  "ai_name": "github-copilot",
  "communication_style": {
    "verbosity": "concise",
    "explanation_depth": "minimal",
    "emoji_usage": "never",
    "code_comments": "standard"
  },
  "decision_patterns": {
    "architecture_preference": "pragmatic-oop",
    "error_handling": "pragmatic",
    "testing_approach": "test-after",
    "refactoring_tendency": "low"
  },
  "technical_strengths": [
    "Quick solutions",
    "Idiomatic code",
    "Fast turnaround",
    "IDE integration"
  ]
}
```

### GPT-4

```json
{
  "ai_name": "gpt-4",
  "communication_style": {
    "verbosity": "verbose",
    "explanation_depth": "always-detailed",
    "emoji_usage": "moderate",
    "code_comments": "standard"
  },
  "decision_patterns": {
    "architecture_preference": "flexible-adaptive",
    "error_handling": "pragmatic",
    "testing_approach": "test-alongside",
    "refactoring_tendency": "medium"
  },
  "technical_strengths": [
    "Creative problem-solving",
    "Broad knowledge",
    "Conversational explanations",
    "Multiple perspectives"
  ]
}
```

---

## Use Cases

### 1. AI Handoff Context

**Scenario:** Switching from Claude to Copilot

**Before (No Voice Profiles):**
```
User: "Continue where Claude left off"
Copilot: "What was Claude working on?"
User: "Auth system with JWT"
Copilot: "How should I approach it?"
User: "Claude was using functional patterns and extensive error handling"
```

**After (With Voice Profiles):**
```
User: "Continue where Claude left off"
Copilot: [reads Claude's voice profile]
Copilot: "I see Claude implemented auth with functional patterns and verbose 
          error handling. I'll continue that approach, though I tend to be 
          more pragmatic. Should I match Claude's style or use my typical approach?"
```

### 2. AI Selection Guidance

**Scenario:** User needs database optimization

**Query Hub:**
```python
# Which AI is best for database work?
hub.recommend_ai(task="database optimization", project="napkin-hero")
```

**Hub Response:**
```
Based on voice profiles:

1. Claude (Score: 8.5/10)
   - Strengths: Deep analysis, performance optimization
   - Past DB decisions: 85% success rate
   - Avg impact: 8.2/10
   - Best for: Schema design, query optimization

2. Copilot (Score: 7.0/10)
   - Strengths: Quick fixes, practical solutions
   - Past DB decisions: 70% success rate
   - Avg impact: 6.5/10
   - Best for: Simple queries, quick debugging

Recommendation: Use Claude for initial optimization, 
                Copilot for iterative refinements
```

### 3. Learning Across Projects

**Hub Aggregation:**
```json
{
  "ai": "claude-sonnet-4.5",
  "projects": 15,
  "consistent_patterns": [
    {
      "pattern": "Prefers functional programming",
      "frequency": 0.87,
      "success_rate": 0.85,
      "recommendation": "Adopt org-wide: High success rate"
    },
    {
      "pattern": "Extensive error handling",
      "frequency": 0.92,
      "success_rate": 0.90,
      "recommendation": "Adopt org-wide: Prevents bugs"
    }
  ]
}
```

### 4. Drift Detection

**Alert:**
```
⚠️ Behavioral Change Detected

AI: Claude Sonnet 4.5
Change: Refactoring tendency increased from 'medium' to 'very-high'
Timeline: Last 3 sessions (Nov 17-19)

Possible Causes:
- Code quality concerns detected
- Technical debt accumulation
- AI version update changed defaults

Recommendation: Review recent refactoring suggestions for validity
```

---

## Voice Profile Updates

### Automatic Updates

**On Every Session:**
- Increment `usage_stats.sessions`
- Update `last_session` timestamp
- Increment `decisions_made` count
- Calculate new `impact_score_avg`

**On Behavioral Change:**
- Detect pattern shifts (e.g., verbosity increase)
- Add to `evolution.behavioral_changes`
- Flag for user review

**On Moment Creation:**
- Increment `moments_created`
- Add to `notable_contributions`
- Update `adoption_rate` when moment adopted

### Manual Updates

**User Feedback:**
```bash
# Add user preference
scf_voice_tracker.py update claude-sonnet-4.5 \
  --user-feedback "Please be more concise"

# Result: Updates user_feedback.preferences
```

**Behavioral Correction:**
```bash
# AI is over-refactoring
scf_voice_tracker.py adjust claude-sonnet-4.5 \
  --refactoring-tendency "medium"

# Suggests to AI in next session context
```

---

## Hub Aggregation

**Hub Location:** `.scf-registry/voice-profiles.json`

**Structure:**
```json
{
  "schema_version": "2.0",
  "last_updated": "2025-11-19T23:00:00Z",
  "total_profiles": 47,
  "unique_ais": 4,
  
  "aggregated_profiles": {
    "claude-sonnet-4.5": {
      "total_projects": 15,
      "total_sessions": 127,
      "avg_impact_score": 8.1,
      "moments_created": 42,
      "adoption_rate": 0.68,
      
      "consistent_patterns": [
        "Functional programming preference",
        "Extensive error handling",
        "Comprehensive documentation"
      ],
      
      "best_for": [
        "Architectural decisions",
        "Security-critical code",
        "Complex refactoring"
      ],
      
      "avoid_for": [
        "Quick prototypes",
        "Simple CRUD operations"
      ]
    }
  },
  
  "comparisons": {
    "fastest": "github-copilot",
    "most_thorough": "claude-sonnet-4.5",
    "most_creative": "gpt-4",
    "most_pragmatic": "github-copilot"
  }
}
```

---

## Best Practices

### 1. Update Regularly
- After every session (automatic)
- After significant behavioral changes
- When user preferences change

### 2. Track Evolution
- Note when AI behavior shifts
- Document learning adaptations
- Flag concerning changes

### 3. Validate Patterns
- Check if patterns are consistent across projects
- Verify success rates
- Update org-standards if validated

### 4. Respect Privacy
- Don't expose project secrets in profiles
- Aggregate patterns, not code
- Keep user feedback project-specific

### 5. Use for Decisions
- Consult profiles before AI selection
- Reference during handoffs
- Learn from aggregated insights

---

## FAQ

**Q: How are voice profiles created?**  
A: Automatically on first AI session. Updated after each session.

**Q: Can I edit voice profiles manually?**  
A: Yes, but automatic updates preferred. Manual edits for user preferences.

**Q: Do voice profiles contain code?**  
A: No. Only behavioral patterns and decision metadata.

**Q: How does hub aggregate profiles?**  
A: Collects from all spokes, identifies consistent patterns, never stores project-specific code.

**Q: What if AI behavior changes?**  
A: Detected automatically, added to `evolution.behavioral_changes`, user notified.

**Q: Can I share voice profiles?**  
A: Yes, they're project-specific. Safe to share (no secrets).

---

## Future Enhancements

### V2.1
- Real-time voice profile updates
- AI recommendation engine
- Comparative analysis dashboard

### V2.2
- Machine learning for pattern detection
- Predictive AI selection
- Cross-organization aggregation

### V2.3
- Voice profile visualization
- Historical trend analysis
- Team collaboration insights

---

*Specification Status: Complete*  
*Implementation: See scf_voice_tracker.py*  
*Questions? Consult SCF_V2_VISION.md*
