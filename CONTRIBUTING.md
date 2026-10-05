# Contributing to Advanced Calculator

شكراً لاهتمامك بالمساهمة في مشروع الآلة الحاسبة المتقدمة!

Thank you for your interest in contributing to the Advanced Calculator project!

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- wxPython 4.1 or higher

### Setting Up Development Environment

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/CalcForBlind.git
cd CalcForBlind

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python calculator.py
```

## Development Guidelines

### Code Style
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Use type hints where applicable

### Commit Messages
- Use clear, descriptive commit messages
- Format: `type(scope): description`
- Examples:
  - `feat(ui): add high contrast theme`
  - `fix(calculator): resolve division by zero error`
  - `docs(readme): update installation instructions`

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Build, dependencies, etc.

## Creating a Pull Request

1. **Fork the repository**
   ```bash
   Click "Fork" on GitHub
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write clear, commented code
   - Test thoroughly
   - Update documentation if needed

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat(feature): add your feature description"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Go to GitHub
   - Click "New Pull Request"
   - Fill in the description
   - Reference any related issues

## PR Description Template

```markdown
## Description
Brief description of changes

## Related Issues
Fixes #(issue number)

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update

## Testing
Describe testing performed

## Screenshots (if applicable)
Add screenshots for UI changes
```

## Areas for Contribution

### High Priority
- [ ] Unit tests
- [ ] Additional languages
- [ ] Bug fixes

### Medium Priority
- [ ] Scientific calculator functions
- [ ] Unit conversion
- [ ] Improved themes
- [ ] Keyboard shortcuts documentation

### Nice to Have
- [ ] Configuration UI
- [ ] Plugin system
- [ ] Export history to file
- [ ] Sound feedback options

## Reporting Issues

### Bug Reports
Include:
- Python version
- Windows/OS version
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots if applicable
- Error messages/logs

### Feature Requests
Include:
- Clear description of feature
- Why it would be useful
- Potential implementation approach

## Code Review Process

1. Automated checks will run
2. Maintainers will review your code
3. Changes may be requested
4. Once approved, your PR will be merged

## Questions?

- Check existing issues/discussions
- Create a new discussion
- Reach out to maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Happy Contributing! 🎉**
