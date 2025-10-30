# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Project**: AI Programming Crash Course v2.0 - From Scenario-Driven Practice to Enterprise Integration
**Type**: Scenario-Driven Learning Educational Course
**Duration**: 15 hours core content + flexible practical exercises
**Target**: Teaching developers to master AI-assisted programming tools through real-world scenarios

### Core Philosophy

This is a **scenario-driven learning curriculum** modeled after Linux learning methodology:
- NOT about memorizing commands, but about knowing "which direction to explore" when problems arise
- Learning through solving real problems, building organic command memory
- Redefining Claude Code as an **AI Agent Platform**, not just a code assistant

## Repository Structure

### Main Course Content

```
AI_Programming_15h_Course_v2.0/
├── 00_情境驅動學習法入門/        # Module 0: Scenario-Driven Learning (NEW in v2.0)
├── 01_AI編程基礎認知/            # Module 1: AI Programming Foundations
├── 02_CLI工具精通/               # Module 2: CLI Tool Mastery
├── 02.5_進階指令整合應用/        # Module 2.5: Advanced Command Integration (NEW in v2.0)
├── 03-12 模組/                   # Modules 3-12: IDE, TDD/BDD, CI/CD, etc.
├── 補充資源/                     # Supplementary Resources
│   ├── 情境題庫總覽/             # 300+ scenario problems (Level 1/2/3)
│   ├── Anki記憶卡總庫/           # 500+ Anki flashcards
│   └── 範例專案庫/               # Sample projects
└── 講師專區/                     # Instructor Zone
    └── 1.1_課程設計與規劃/       # Course Design & Planning
```

### Key Documentation

- **Course Overview**: `AI_Programming_15h_Course_v2.0/README.md`
- **WBS (Work Breakdown Structure)**: `AI_Programming_15h_Course_v2.0/WBS_工作分解結構.md`
- **Structure Guide**: `docs/課程資料夾結構說明.md`
- **Complete Syllabus**: `docs/AI編程速成課程_完整大綱_v2.0.md`

## Development Workflow

### WBS-Driven Development

This project follows a strict WBS (Work Breakdown Structure) methodology:

1. **Check WBS before starting**: Always review `WBS_工作分解結構.md` to understand current phase
2. **Update progress**: After completing work, update WBS with:
   - Completed items (mark with ✅)
   - Progress records in `## 📈 進度記錄` section
   - Deliverables statistics
3. **Git workflow**:
   - Use Conventional Commits format (defined in global CLAUDE.md)
   - Update WBS progress in the same commit when completing major milestones
   - Push changes after confirming WBS is updated

### Current Development Phase

**Phase 1 Completed (✅ Milestone 1)**:
- 1.1 Course Design & Planning (15%)
- All design documents in `講師專區/1.1_課程設計與規劃/` completed
- Total: 7 documents, ~3,200 lines

**Next Phase**:
- 1.2.1 Module 0: Scenario-Driven Learning Introduction (3%)

### Conventional Commits Reference

Follow the Conventional Commits format defined in `~/.claude/CLAUDE.md`:

**Common types for this project**:
- `feat(module-X)`: New module content or features
- `docs(design)`: Design documentation
- `docs(wbs)`: WBS updates
- `feat(scenarios)`: Scenario problems
- `feat(flashcards)`: Anki flashcards
- `fix(structure)`: File structure corrections
- `refactor(content)`: Content reorganization

## Architecture & Design Principles

### Three-Layer Scenario Pyramid

Course problems are structured in three difficulty levels:

1. **Level 1 (Basic)**: Single scenarios - 50 problems
   - Focus on individual command mastery
   - 30 min - 1 hour per scenario

2. **Level 2 (Intermediate)**: Composite scenarios - 150 problems
   - Combine multiple commands/concepts
   - 1-3 hours per scenario
   - Example: "Complete open-source contribution workflow"

3. **Level 3 (Advanced)**: Complex scenarios - 100 problems
   - Multi-day projects requiring full workflow orchestration
   - Example: "Personal knowledge management system from scratch"

### Learning Theory Foundation

Core pedagogical approach (see `講師專區/1.1_課程設計與規劃/1.1.1_學習理論設計/`):

1. **Cognitive Science Based**
   - Spaced repetition (Anki flashcards)
   - Active recall through scenarios
   - Elaborative interrogation

2. **Linux Learning Analogy**
   - Learn by doing, not memorizing
   - Build mental models through problem-solving
   - Understand "when to use what" rather than "what does this do"

3. **Validation-First Paradigm**
   - Shift from "generate code" to "validate code"
   - TDD/BDD integration with AI collaboration
   - Systematic security scanning

### Module Structure Pattern

Each module follows consistent structure:

```
XX_ModuleName/
├── README.md              # Module overview
├── 理論/                  # Theory & concepts
├── 情境題庫/              # Scenario problems (Level 1/2/3)
├── 實作/                  # Hands-on exercises
├── 記憶卡庫/              # Anki flashcards
└── 作業/                  # Assignments
```

## Working with Content

### Creating New Module Content

When developing new module content:

1. **Check WBS task list**: Verify what's needed in `WBS_工作分解結構.md`
2. **Follow module structure**: Use the pattern above
3. **Write scenarios first**: Start with real-world problems, derive commands naturally
4. **Create flashcards**: Write situation-based flashcards, NOT definition-based
5. **Update WBS**: Mark completed items and add progress records

### Flashcard Design Philosophy

**WRONG ❌**:
```
Q: What does /agents command do?
A: Manages AI agents
```

**RIGHT ✅**:
```
Q: 【Scenario】You need deep security audit covering SQL injection,
   XSS, permissions. What's your approach?

A: 【Solution】
   1. Switch to expert mode: /agents:security-auditor
   2. Run comprehensive scan: claude /security-review ./src
   3. Generate report: /output-style:security-report
   4. Log learnings: /memory

   【Memory Point】Need professional analysis → Switch to corresponding agent
```

### Scenario Problem Design

Each scenario should include:

- **Background**: Real-world context
- **Task**: Clear objective
- **Time estimate**: Realistic completion time
- **Checkpoints**: Learning verification points
- **Natural command discovery**: Commands learned organically through solving the problem
- **Reference solution**: Not just code, but thought process

Example structure in `補充資源/情境題庫總覽/情境設計模板.md`

## Important Conventions

### File Naming

- Use descriptive Chinese names for directories: `情境題庫/`, `記憶卡庫/`
- Use numbered prefixes for modules: `00_`, `01_`, `02_`, etc.
- Markdown files use `.md` extension
- README.md in every major directory

### Documentation Standards

- All theory files use Markdown with clear headings
- Include examples and diagrams where helpful
- Reference WBS task IDs when completing deliverables
- Keep line length reasonable for readability

### Git Workflow

After completing significant work:

```bash
# 1. Review what changed
git status
git diff

# 2. Stage changes
git add <files>

# 3. Commit with Conventional Commits format
git commit -m "$(cat <<'EOF'
feat(module-X): brief description

Detailed explanation of changes.

Completed WBS tasks:
- 1.2.X.Y Task description
- 1.2.X.Z Another task

Deliverables:
- File1.md (XXX lines)
- File2.md (YYY lines)
EOF
)"

# 4. Update WBS progress
# Edit WBS_工作分解結構.md to reflect completed work

# 5. Commit WBS update
git add WBS_工作分解結構.md
git commit -m "docs(wbs): update progress for module X completion"

# 6. Push
git push origin main
```

## WHEN TO GIT COMMIT AND PUSH

### ⚡ COMMIT Triggers (When to Create Commits)

**ALWAYS COMMIT when you complete**:

1. **✅ WBS Task Completion** (Most Important)
   - Any task marked with checkbox in `WBS_工作分解結構.md`
   - Even if it's a single file, if it completes a WBS deliverable
   - **Example**: Completing `1.2.1.1 理論內容` → Immediate commit

2. **✅ Logical Units of Work**
   - One complete document (e.g., `2.1_Claude_Code安裝與配置.md`)
   - One complete scenario problem with solution
   - One set of related flashcards (e.g., all flashcards for Module 2)
   - One README.md with complete module overview

3. **✅ Milestone Completions**
   - Finishing all documents for a sub-section (e.g., `1.1.1_學習理論設計/`)
   - Completing all scenarios for one difficulty level
   - Finishing all theory files for one module

4. **✅ Structure Changes**
   - Creating new directory structures
   - Moving files to correct locations
   - Renaming files for consistency

5. **✅ WBS Updates**
   - ALWAYS commit WBS updates separately after content commits
   - Include progress statistics and completion records
   - Use `docs(wbs):` prefix

**DO NOT COMMIT**:
- ❌ Incomplete drafts (unless explicitly saving work-in-progress)
- ❌ Broken content (untested examples, incomplete scenarios)
- ❌ Uncommitted changes before switching tasks

### 🚀 PUSH Triggers (When to Push to Remote)

**ALWAYS PUSH after**:

1. **✅ Completing Any WBS Sub-Task** (1.X.X.X level)
   - Even if just one document
   - Ensures work is backed up immediately
   - **Example**: After committing `1.2.1.1` theory content → Push

2. **✅ End of Work Session**
   - Before closing Claude Code
   - Before switching to different task
   - At natural stopping points

3. **✅ Milestone Achievements**
   - After completing a major WBS section (e.g., 1.1.1, 1.1.2)
   - After updating WBS with milestone completion
   - **Example**: Completing `1.1 課程設計與規劃` → Push

4. **✅ Multiple Related Commits**
   - After 2-3 commits that form a logical group
   - **Example**:
     - Commit 1: New module content
     - Commit 2: WBS update
     - → Push both together

**DO NOT PUSH**:
- ❌ Broken/incomplete work (unless intentionally saving WIP)
- ❌ Before testing that examples work
- ❌ Content that violates quality standards

### 📋 Standard Workflow Pattern

**Pattern 1: Single Document Completion**
```bash
# 1. Complete work (e.g., write 2.1_Claude_Code安裝與配置.md)
# 2. Test/verify content
# 3. Commit content
git add AI_Programming_15h_Course_v2.0/02_CLI工具精通/理論/2.1_Claude_Code安裝與配置.md
git commit -m "feat(module-2): add Claude Code installation guide"
# 4. Update WBS
git add AI_Programming_15h_Course_v2.0/WBS_工作分解結構.md
git commit -m "docs(wbs): mark 1.2.3.1 installation guide complete"
# 5. Push immediately
git push origin main
```

**Pattern 2: Multiple Files (Same WBS Task)**
```bash
# 1. Complete all files for one WBS task
# 2. Commit all together
git add AI_Programming_15h_Course_v2.0/02_CLI工具精通/情境題庫/基礎級/*.md
git commit -m "feat(scenarios): add 15 Level-1 scenarios for Module 2"
# 3. Update WBS
git add AI_Programming_15h_Course_v2.0/WBS_工作分解結構.md
git commit -m "docs(wbs): complete 1.2.3.2 basic scenario bank"
# 4. Push
git push origin main
```

**Pattern 3: Milestone Completion**
```bash
# 1. Complete final task of milestone
git commit -m "feat(design): complete evaluation system design"
# 2. Update WBS with comprehensive milestone record
git add AI_Programming_15h_Course_v2.0/WBS_工作分解結構.md
git commit -m "$(cat <<'EOF'
docs(wbs): complete Milestone 1 - Course Design & Planning

Completed all tasks in 1.1 課程設計與規劃 (15%)

Deliverables:
- 7 design documents (~3,200 lines)
- Learning theory foundation established
- Three-layer scenario pyramid designed
- Assessment system framework complete

Next: Begin Phase 2 - Content Development (Module 0)
EOF
)"
# 3. Push milestone
git push origin main
```

### 🎯 Decision Tree: Should I Commit/Push Now?

```
Did I complete a WBS task?
├─ YES → Commit + Update WBS + Push ✅
└─ NO
    └─ Did I complete a logical unit (1 doc, 1 scenario)?
        ├─ YES → Commit (Push if end of session) ✅
        └─ NO
            └─ Am I switching tasks or ending session?
                ├─ YES → Commit WIP + Push (with clear message) ⚠️
                └─ NO → Keep working, don't commit yet ❌
```

### 📊 Commit Frequency Guidelines

**Recommended Frequency**:
- **Commits**: 3-5 per work session (typically 1-2 hours)
- **Pushes**: 1-2 per work session (at natural breakpoints)
- **WBS Updates**: After each significant WBS task completion

**Example Daily Pattern**:
```
9:00  - Start work on Module 2 theory
10:30 - Complete 2.1_安裝與配置.md → COMMIT + PUSH
11:00 - Complete 2.2_上下文管理.md → COMMIT
12:00 - Complete 2.3_程式碼庫分析.md → COMMIT + Update WBS + PUSH
```

### 🚨 Special Cases

**Case 1: Found Error After Push**
```bash
# Fix immediately
git add <fixed-file>
git commit -m "fix(module-X): correct typo in installation guide"
git push origin main
# No need to wait - fix and push immediately
```

**Case 2: Large Milestone with Many Files**
```bash
# Break into multiple commits by category
git add 理論/*.md
git commit -m "feat(module-X): add all theory documents"

git add 情境題庫/**/*.md
git commit -m "feat(scenarios): add complete scenario bank for Module X"

git add 記憶卡庫/*.md
git commit -m "feat(flashcards): add Anki flashcard set for Module X"

# Then update WBS once
git add WBS_工作分解結構.md
git commit -m "docs(wbs): complete Module X content development"

# Push all together
git push origin main
```

**Case 3: Experimental/Draft Work**
```bash
# Clearly mark as WIP
git add <draft-files>
git commit -m "wip(module-X): draft scenario outline (not final)"
# Push to backup but don't mark WBS complete
git push origin main
```

### ✅ Commit Message Quality Checklist

Before each commit, verify:

- [ ] Used correct Conventional Commits type (`feat`, `docs`, `fix`, etc.)
- [ ] Included scope (e.g., `module-2`, `wbs`, `scenarios`)
- [ ] Subject line is clear and concise (<50 chars)
- [ ] Body explains WHAT and WHY (if not obvious)
- [ ] Referenced WBS task IDs (if applicable)
- [ ] Listed deliverables with statistics (for WBS commits)
- [ ] Followed format from global `~/.claude/CLAUDE.md`

### 🎓 Examples from This Project

**Good Commit Examples**:
```bash
✅ feat(course-design): 完成 1.1 課程設計與規劃所有文檔
✅ docs(wbs): 更新 WBS 進度記錄與里程碑狀態
✅ fix(structure): 移動課程設計文檔到正確位置
```

**Bad Commit Examples**:
```bash
❌ update files                    # Too vague
❌ add stuff                       # No context
❌ work in progress                # Not descriptive
❌ 完成所有工作                     # Too broad, no English type
```

---

**Remember**:
- **Commit early, commit often** - Each logical unit of work
- **Push regularly** - After WBS tasks and at session ends
- **Update WBS separately** - Always commit WBS updates after content
- **Quality over speed** - But don't delay pushing completed work

## Quality Standards

### Content Quality

- Every scenario must be tested and validated in practice
- All code examples must be executable
- Documentation format must be consistent
- Diagrams and charts must be clear

### Deliverable Checklist

Before marking WBS items complete:

- [ ] Content is complete and accurate
- [ ] Examples are tested
- [ ] Flashcards are created (if applicable)
- [ ] Scenarios are designed (if applicable)
- [ ] README.md is updated
- [ ] WBS is updated with progress
- [ ] Git commit follows conventions

## Development Commands

### Check Project Status

```bash
# View WBS current phase
cat AI_Programming_15h_Course_v2.0/WBS_工作分解結構.md | grep -A 10 "進度記錄"

# List all module directories
exa -la AI_Programming_15h_Course_v2.0/ --ignore-glob="補充資源|講師專區"

# Find incomplete WBS items
rg "\[ \]" AI_Programming_15h_Course_v2.0/WBS_工作分解結構.md
```

### Create New Module Content

```bash
# Navigate to module directory
cd AI_Programming_15h_Course_v2.0/XX_ModuleName/

# Create standard structure (if needed)
mkdir -p 理論 情境題庫/{基礎級,組合級,複雜級} 實作 記憶卡庫 作業

# Start writing content
# Use Read/Write/Edit tools for file operations
```

## Project Goals (from WBS)

### Success Criteria

- [ ] Complete 13 core modules (52 hours content)
- [ ] Build 300+ scenario problem bank
- [ ] Create 500+ Anki flashcards
- [ ] Develop 10+ sample projects
- [ ] Establish complete assessment system

### Milestones

1. **Milestone 1** (Week 2): Design Complete ✅
   - Learning theory documented
   - Course architecture finalized
   - Detailed WBS plan complete

2. **Milestone 2** (Week 10): Core Content Complete
   - Modules 0-2.5 content finished
   - Basic scenario bank complete
   - Flashcard system prototype ready

3. **Milestone 3** (Week 14): Practical Projects Complete
   - Sample project library finished
   - Comprehensive practical projects done
   - Tool integration examples complete

4. **Milestone 4** (Week 16): Course Release
   - All content quality checked
   - Supplementary resources integrated
   - Release package prepared

## Context for AI Assistance

### When Writing Module Content

- Focus on **scenario-driven** approach, not command-listing
- Each concept should emerge from solving a real problem
- Include "自然學到的指令" (naturally learned commands) in scenarios
- Write flashcards that test problem-solving, not definitions

### When Updating WBS

- Be specific about deliverables (file names, line counts)
- Include statistics and metrics
- Link to actual completed files
- Update both task checkboxes AND progress records section

### When Creating Scenarios

- Start with realistic background
- Set clear objectives and time estimates
- Define checkpoints for self-assessment
- Show how commands are discovered naturally, not prescribed upfront
- Include reference solution with reasoning, not just code

---

**Last Updated**: 2025-10-30
**Current Phase**: Phase 2 - Content Development (Module 0 next)
**Project Version**: v2.0 (Scenario-Driven Learning Edition)
