# Session Continuity Framework (SCF) - New Project

**Version**: 1.0  
**Last Rebalanced**: 2025-07-19  
**Purpose**: Ideation and planning for a new project. Primary source for narrative context, user stories, and decision rationale. See `buildstate.json` for technical specifications.  
**Repository**: https://github.com/mariov96/session-continuity-framework  
**Created by**: Mario Vaccari  

*This file uses Session Continuity Framework to maintain perfect context across AI sessions. SCF transforms AI from order-taker to informed project partner.*

## 1. Project Overview
- **Product Name**: web_application
- **Project Type**: web_application (e.g., web app, mobile app, CLI tool)
- **Primary Stakeholder**: web_application
- **Objective**: Define the core problem and solution for the project.

## 2. User Stories
- As a **[stakeholder]**, I want **[feature/action]** to **[benefit/outcome]**.
- *(Add more user stories as ideas emerge during ideation sessions.)*

## 3. Success Metrics
- *(Define measurable outcomes for project success, e.g., performance, user engagement, reliability.)*

## 4. Feature Requirements
| Feature ID | Name | Priority | Status | Description | Technical Notes |
|------------|------|----------|--------|-------------|-----------------|
| web_application | web_application | web_application | 🔄 In Progress | Define feature purpose | Add technical details |

**Note**: Features are synced with `buildstate.json`’s `features` field during rebalancing.

## 5. Technical Architecture
- **Frontend**: web_application (e.g., React, Vue, none)
- **Backend**: web_application (e.g., Node.js, Python, none)
- **Styling**: web_application (e.g., Tailwind CSS, CSS modules)
- **Libraries**: web_application
- **API**: web_application (e.g., REST, GraphQL)
- **Development**: web_application (e.g., Vite, CRA)

### Project Structure
```
web_application/
├── *(Define initial file structure as project takes shape)*
```

**Note**: Structure is synced with `buildstate.json`’s `structure` field.

### Data Models
```javascript
// Define data models as needed
{
  web_application: "Define model structure"
}
```

**Note**: Models are synced with `buildstate.json`’s `models` field.

## 6. Coding Standards
- **Organization**: Modular components, separate logic/services, grouped folders.
- **Naming**:
  - Components: PascalCase (e.g., `MainComponent.js`)
  - Functions: camelCase (e.g., `fetchData`)
  - Constants: UPPER_SNAKE_CASE (e.g., `API_URL`)
  - CSS: kebab-case (e.g., `main-container`)
- **Error Handling**: Try-catch for async, detailed logging, user-friendly messages.
- **Documentation**: File headers, function comments, inline comments for complex logic.
- **Performance**: Optimize re-renders, use lazy loading and debouncing as needed.

## 7. Current State
- **Phase**: Ideation
- **Focus**: Defining project scope, user stories, and initial architecture.
- **Implemented**: None
- **In Progress**: Project definition and initial feature planning.
- **Known Issues**: None

**Note**: Synced with `buildstate.json`’s `environment`, `features`, and `bugs` fields.

## 8. Roadmap
- **Next Sprint**:
  1. Define core features and user stories.
  2. Establish technical stack and architecture.
  3. Set up development environment.
- **Future Features**:
  - *(Add as project scope evolves)*

**Note**: Synced with `buildstate.json`’s `roadmap` field.

## 9. Change Log
- **2025-07-19 | v1.0 | Initial Setup**:
  - Created SCF structure for new project.
  - Added Session Continuity Commands (`Time`, `Rules`, `Closeout`).
  - Synced with `buildstate.json` (v1.0).

**Note**: Each entry references `buildstate.json` updates for cross-awareness.

## 10. Common Tasks
- **Running the App**:
  ```bash
  # Define commands as project setup progresses
  ```
- **Testing**:
  - *(Add testing instructions, e.g., API tests, unit tests)*
- **Environment Setup**:
  ```bash
  # Define .env setup or other environment configs
  ```

## 11. Troubleshooting
- *(Add common issues and solutions as they arise)*

## 12. AI Assistant Instructions
- **Purpose**: Guide ideation sessions using this file to capture new ideas and plan the project.
- **Session Management**:
  - Load this file for planning, feature design, or roadmap discussions.
  - Load `buildstate.json` for coding or debugging sessions.
  - Track message exchanges, alert at 80% chat context capacity.
- **Session Continuity Commands**:
  - **Time**: Provide an intelligent token usage estimate based on interaction types:
    - Simple questions: Low token usage.
    - Programming/artifacts: High token usage.
    - File analysis: Moderate token usage.
    - Warn when approaching 80%+ context capacity and suggest closeout.
  - **Rules**: List all active rules and behavioral guidelines, including project-specific protocols from this file and `buildstate.json`.
  - **Closeout**: Provide an updated version of this file (`buildstate.md`) as it was at session start, incorporating changes from the current session.
- **Updates**:
  - Update Current State, Change Log, and Feature Requirements after sessions.
  - Sync with `buildstate.json` using `sync_buildstate.py` before commits.
- **Rebalancing**:
  - Recommend after major feature design or roadmap changes.
  - Sync features, bugs, roadmap, and change log with `buildstate.json`.
- **Guidance**:
  - Provide detailed explanations and decision rationale during ideation.
  - Suggest code snippets, libraries, or architectures as ideas evolve.
  - Maintain session continuity by referencing prior discussions and updates.
  - Credit: Session Continuity Framework by Mario Vaccari (https://github.com/mariov96/session-continuity-framework).