<!--
File: /CONTRIBUTING.md
Description: Community contribution guidelines for the Session Continuity Framework. Explains how to report issues, submit features, contribute code, and collaborate with the open-source community.
Last Edited: July 15, 2025 08:25 UTC
-->

# Contributing to Session Continuity Framework

Thank you for your interest in contributing to the Session Continuity Framework! This project thrives on community collaboration and your contributions help make AI-assisted collaboration better for everyone across all domains.

## Code of Conduct

This project follows a simple principle: **Be excellent to each other**. We're all here to build amazing things and help fellow developers succeed with AI collaboration.

## How to Contribute

### 🐛 Reporting Issues

**Before submitting an issue:**

- Check existing issues to avoid duplicates
- Use the search function to find related discussions
- Review the documentation to ensure it's not a usage question

**When submitting an issue:**

- Use a clear, descriptive title
- Provide detailed steps to reproduce (for bugs)
- Include your environment details (AI model, IDE, OS)
- Share relevant _SC-buildstate.md or other _SC-*.md file snippets
- Explain the expected vs actual behavior

### 💡 Feature Requests

We love new ideas! Check the [Future Features](https://claude.ai/chat/README.md#future-features--vision) section first to see if your idea is already planned.

**For feature requests:**

- Explain the problem you're trying to solve in your domain
- Describe your proposed solution
- Consider how it fits with Session Continuity Framework's core principles
- Share any alternative approaches you've considered

### 🔧 Code Contributions

### Setting Up Development

1. **Fork the repository**
    
    ```bash
    # Click "Fork" on GitHub, then clone your fork
    git clone https://github.com/yourusername/session-continuity-framework.git
    cd session-continuity-framework
    
    ```
    
2. **Create a feature branch**
    
    ```bash
    git checkout -b feature/your-feature-name
    # or
    git checkout -b fix/issue-description
    
    ```
    
3. **Make your changes**
    - Follow the existing file structure
    - Test your changes with real projects
    - Update documentation as needed
4. **Commit your changes**
    
    ```bash
    git add .
    git commit -m "feat: add support for X feature"
    # Use conventional commit format
    
    ```
    
5. **Submit a pull request**
    - Push to your fork
    - Create a PR with clear title and description
    - Reference any related issues

### Contribution Types

**📋 Templates & Examples**

- New session type templates (_SC-*.md files for different domains)
- Industry-specific configurations
- Language/framework specific examples for development
- Professional service templates (therapy, legal, consulting)
- Real-world case studies across different fields

**📝 Documentation**

- Improve existing docs
- Add tutorials and guides
- Create video walkthroughs
- Translate to other languages

**🛠️ Tools & Automation**

- IDE extensions
- CLI tools
- Git hooks
- Automation scripts

**🎨 Framework Improvements**

- New _SC-buildstate.md sections
- Enhanced AI prompt protocols
- Better session management patterns
- Integration with new AI models

### Coding Standards

Since Session Continuity Framework is about maintaining standards and practices across sessions, we practice what we preach:

**Markdown Files:**

- Use clear, scannable headers
- Include code examples where helpful
- Keep lines under 100 characters when possible
- Use consistent formatting throughout

**Example Projects:**

- Follow domain/framework best practices
- Include comprehensive _SC-*.md files appropriate to the session type
- Document all important decisions
- Provide clear setup instructions

**AI Prompts:**

- Test with multiple AI models when possible
- Make instructions clear and specific
- Include fallback options for edge cases
- Document expected AI responses

### _SC Template Contributions

When creating new _SC templates:

- **Follow the naming convention**: `_SC-[domain].md`
- **Include clear sections**: Purpose, context, standards, current state
- **Add AI prompt suggestions**: How should AI interpret this template?
- **Cross-link related resources**: Reference other _SC files, documentation, or external resources that AI should be aware of but not responsible for maintaining
- **Provide examples**: Show the template in action
- **Test with real sessions**: Verify it actually improves session continuity

#### Cross-Linking Guidelines
- **Link to related _SC files**: Reference other session continuity files that provide context
- **External resource references**: Include links to documentation, standards, or resources AI should know about
- **Clear responsibility boundaries**: Make it explicit that AI should be informed by these resources but not author or maintain them
- **Use descriptive linking**: Explain why the resource is relevant to session continuity

### 📚 Documentation Contributions

**Improving existing docs:**

- Fix typos and grammatical errors
- Clarify confusing sections
- Add missing information
- Update outdated content

**Creating new content:**

- Step-by-step tutorials
- Video walkthroughs
- Blog post examples
- Conference talk materials

### 🌟 Community Contributions

**Share your experience:**

- Write blog posts about Session Continuity implementation
- Create video tutorials for different session types
- Share success stories from various domains
- Help others in GitHub Discussions

**Spread the word:**

- Star the repository
- Share on social media
- Present at meetups or conferences
- Mention Session Continuity Framework in relevant discussions

## Pull Request Process

1. **Ensure your PR:**
    - Has a clear title and description
    - References related issues (use "fixes #123")
    - Includes tests or examples when applicable
    - Updates documentation if needed
2. **PR Review Process:**
    - Maintainers will review within 1-2 weeks
    - Address any requested changes
    - Keep discussions constructive and focused
    - Be patient with the review process
3. **After Approval:**
    - Squash commits if requested
    - Ensure CI passes
    - Thank reviewers for their time

## Recognition

Contributors are recognized in several ways:

- Added to the Contributors section
- Mentioned in release notes for significant contributions
- Invited to join the maintainer team for ongoing contributors
- Featured in blog posts and social media

## Questions?

- **General questions:** Use GitHub Discussions
- **Bugs or features:** Open an issue
- **Direct contact:** Reach out to [@mariov96](https://github.com/mariov96)

## Thank You!

Every contribution, no matter how small, helps make Session Continuity Framework better for the entire community. Whether you're fixing a typo, adding a new session template, or proposing a major feature - we appreciate your time and effort.

Let's build the future of AI-assisted collaboration together! 🚀