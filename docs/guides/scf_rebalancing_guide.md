# SCF Content Rebalancing Guide

## Overview

The SCF Content Rebalancing system intelligently optimizes the placement of information between `.json` and `.md` files according to SCF principles, ensuring that each file contains the optimal content for its purpose.

## Rebalancing Principles

### JSON Files (`buildstate.json`)
**Purpose**: Technical specifications and machine-readable data
- Technical configurations and settings
- Current implementation status and tracking
- Quantifiable metrics and performance data
- AI collaboration rules and structured guidance
- API definitions and technical specifications

### Markdown Files (`buildstate.md`)
**Purpose**: Human-readable context and strategic thinking
- Conceptual thinking and ideation
- User stories and personas
- Strategic vision and documentation
- Context explanations and rationale
- Narrative descriptions and guides

## Usage Examples

### 1. Check Balance Scores
```bash
# Check balance scores without making changes
python3 buildstate_hunter_learner.py --ecosystem-wide --check-balance

# Check specific project balance
python3 scf_rebalancer.py analyze /path/to/project --suggest-moves
```

### 2. Targeted Rebalancing
```bash
# Rebalance high-quality projects during discovery
python3 buildstate_hunter_learner.py --ecosystem-wide --rebalance --dry-run

# Rebalance after inheritance updates
python3 buildstate_hunter_learner.py --update-libraries --inheritance-level org --rebalance
```

### 3. Comprehensive Rebalancing
```bash
# Rebalance all discovered projects
python3 buildstate_hunter_learner.py --ecosystem-wide --rebalance-all --dry-run

# Batch rebalance multiple projects
python3 scf_rebalancer.py batch-rebalance "/path/to/projects/*" --min-score 0.6
```

### 4. During Ecosystem Learning
```bash
# Full ecosystem analysis with rebalancing and library updates
python3 buildstate_hunter_learner.py --ecosystem-wide --update-libraries --inheritance-level org --rebalance --verbose
```

## Rebalancing Scenarios

### When Content Gets Rebalanced

1. **Discovery Phase**: High-quality projects (score ≥ 60) get analyzed for balance
2. **After Updates**: Projects receive content rebalancing after inheritance updates
3. **Comprehensive Mode**: All projects with balance scores < 0.7 get rebalanced
4. **Manual Mode**: Specific projects or patterns can be rebalanced on demand

### Content Classification Examples

#### Moves to JSON (Technical/Structured)
```json
{
  "ai_rules": {
    "purpose": "Guide technical sessions",
    "session": "Load for coding context"
  },
  "performance_metrics": {
    "target_response_time": "< 200ms",
    "success_criteria": "95% uptime"
  },
  "api_endpoints": [
    "/api/v1/users",
    "/api/v1/projects"
  ]
}
```

#### Moves to Markdown (Contextual/Strategic)
```markdown
## Project Vision & Strategy

The vision for this project is to create a seamless user experience that...

## User Stories & Personas

**Primary User**: Development teams who need to...

## Innovation Opportunities

We should explore opportunities to enhance the workflow by...
```

## Balance Scoring

### Score Ranges
- **0.8 - 1.0**: Well balanced, minimal changes needed
- **0.6 - 0.79**: Moderately balanced, some optimization beneficial
- **0.4 - 0.59**: Needs rebalancing, significant improvements possible
- **0.0 - 0.39**: Poorly balanced, major reorganization needed

### Factors in Scoring
- **Content Type Alignment**: How well content matches file purpose
- **Information Architecture**: Logical organization of information
- **Confidence Levels**: System confidence in placement decisions
- **SCF Compliance**: Adherence to framework principles

## Advanced Usage

### Custom Content Rules

The rebalancer uses configurable rules for content classification:

```python
# Technical indicators (JSON)
json_indicators = {
    'technical': ['version', 'status', 'config', 'api_url', 'dependencies'],
    'tracking': ['change_log', 'metrics', 'performance'],
    'ai_structured': ['ai_rules', 'coding_standards', 'testing']
}

# Human-readable indicators (Markdown)
md_indicators = {
    'ideation': ['vision', 'concept', 'strategy', 'philosophy'],
    'context': ['background', 'motivation', 'explanation'],
    'user_focused': ['user_stories', 'personas', 'journey'],
    'documentation': ['notes', 'guide', 'lessons_learned']
}
```

### Integration with Inheritance

Rebalancing works seamlessly with the inheritance system:

1. **Library Updates**: Shared libraries get rebalanced after innovation updates
2. **Project Inheritance**: Individual projects inherit well-balanced patterns
3. **Propagation**: Balance improvements spread across the ecosystem
4. **Safety**: Individual project files never get touched directly

### Backup and Safety

All rebalancing operations include safety measures:

```bash
# Automatic backups created
buildstate.json.backup.20250108_143022
buildstate.md.backup.20250108_143022

# Change logging in both files
"change_log": [{
  "date": "2025-01-08",
  "version": "rebalanced", 
  "desc": "SCF rebalancing: moved 5 items to MD, 2 items from MD",
  "source": "scf_rebalancer",
  "balance_score": "0.89"
}]
```

## Best Practices

### 1. Regular Balance Checks
- Run `--check-balance` monthly to monitor ecosystem health
- Focus on projects with scores below 0.7
- Use balance metrics to guide content organization

### 2. Integrated Workflow
```bash
# Recommended workflow for ecosystem maintenance
python3 buildstate_hunter_learner.py \
  --ecosystem-wide \
  --update-libraries \
  --inheritance-level org \
  --rebalance \
  --verbose
```

### 3. Gradual Improvement
- Start with high-quality projects (better success rate)
- Use dry-run mode to understand changes before applying
- Monitor balance scores over time to track improvement

### 4. Content Strategy Alignment
- JSON for AI tools and automation
- Markdown for human understanding and strategy
- Clear separation enables better tool integration
- Improved readability and maintenance

## Troubleshooting

### Common Issues

**Low Balance Scores**
- Too much documentation in JSON files
- Technical data mixed with narrative content
- Solution: Run comprehensive rebalancing

**Rebalancer Not Available**
- Check import: `from scf_rebalancer import SCFBuildstateRebalancer`
- Verify file exists: `scf_rebalancer.py`
- Solution: Ensure rebalancer is in the same directory

**Missing Buildstate Pairs**
- Some projects only have `.json` or `.md` files
- Solution: Create missing files before rebalancing

### Performance Optimization

For large ecosystems:
- Use `--min-score` to focus on projects that need rebalancing
- Process projects in batches rather than all at once
- Run during maintenance windows for large rebalancing operations

## Integration Examples

### With VS Code Extensions
```json
{
  "tasks": [
    {
      "label": "SCF Rebalance Check",
      "type": "shell",
      "command": "python3 buildstate_hunter_learner.py --check-balance"
    },
    {
      "label": "SCF Ecosystem Update",
      "type": "shell", 
      "command": "python3 buildstate_hunter_learner.py --ecosystem-wide --update-libraries --rebalance"
    }
  ]
}
```

### With CI/CD Pipelines
```yaml
- name: SCF Balance Check
  run: |
    python3 buildstate_hunter_learner.py --ecosystem-wide --check-balance
    # Fail if average balance score < 0.6
```

This rebalancing system ensures that your SCF ecosystem maintains optimal information architecture, supporting both human understanding and AI tool integration while preserving the evolutionary record of your development process.