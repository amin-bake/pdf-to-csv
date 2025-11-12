# GitHub Release Checklist

Use this checklist when preparing a new release for GitHub.

## Pre-Release Preparation

### 1. Code Quality

- [ ] All tests pass locally (`python test_*.py`)
- [ ] No lint errors or warnings
- [ ] Code follows style guidelines
- [ ] All functions have proper docstrings
- [ ] No debug print statements or commented code

### 2. Documentation

- [ ] README.md is up to date
- [ ] CHANGELOG.md includes all changes for this version
- [ ] API documentation is accurate
- [ ] All new features are documented
- [ ] Installation instructions tested on clean environment

### 3. Testing

- [ ] All unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Tested on Windows, Linux, and macOS (if possible)
- [ ] Tested with Python 3.8, 3.9, 3.10, 3.11
- [ ] Browser compatibility verified (Chrome, Firefox, Safari, Edge)

### 4. Security

- [ ] No hardcoded secrets or credentials
- [ ] Dependencies audited (`pip-audit`)
- [ ] Security policy reviewed
- [ ] Known vulnerabilities documented

### 5. Dependencies

- [ ] requirements.txt is up to date
- [ ] All dependencies have version constraints
- [ ] Unnecessary dependencies removed
- [ ] License compatibility verified

## Release Process

### 1. Version Bump

- [ ] Update version in CHANGELOG.md
- [ ] Add release date to CHANGELOG.md
- [ ] Create git tag: `git tag -a v1.0.0 -m "Release v1.0.0"`

### 2. GitHub Release

- [ ] Push tag: `git push origin v1.0.0`
- [ ] Create release on GitHub
- [ ] Copy CHANGELOG entry to release notes
- [ ] Attach any necessary files
- [ ] Mark as pre-release if applicable

### 3. Post-Release

- [ ] Verify release on GitHub
- [ ] Test installation from release
- [ ] Update project boards
- [ ] Close related issues and milestones
- [ ] Announce release (if applicable)

## Release Notes Template

```markdown
# Version X.Y.Z - YYYY-MM-DD

## 🎉 Highlights

Brief overview of major changes

## ✨ New Features

- Feature 1 (#issue)
- Feature 2 (#issue)

## 🐛 Bug Fixes

- Fix 1 (#issue)
- Fix 2 (#issue)

## 📚 Documentation

- Documentation updates

## 🔒 Security

- Security improvements

## ⚠️ Breaking Changes

- Breaking change description and migration guide

## 📦 Dependencies

- Dependency updates

## 🙏 Contributors

Thank you to all contributors:

- @username1
- @username2

**Full Changelog**: https://github.com/user/repo/compare/v1.0.0...v1.1.0
```

## Versioning Guidelines

Follow Semantic Versioning (semver):

- **MAJOR** (X.0.0): Breaking changes
- **MINOR** (x.Y.0): New features, backward compatible
- **PATCH** (x.y.Z): Bug fixes, backward compatible

Examples:

- `1.0.0` → `1.0.1`: Bug fix
- `1.0.0` → `1.1.0`: New feature
- `1.0.0` → `2.0.0`: Breaking change
