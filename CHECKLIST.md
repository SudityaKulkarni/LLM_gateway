# PyPI Publishing Checklist

## ✅ Completed Steps

- [x] Created package structure with detectors/, services/, schemas/, utils/
- [x] Added __init__.py files to all package directories
- [x] Created setup.py with metadata and dependencies
- [x] Created pyproject.toml for modern packaging
- [x] Created LICENSE file (MIT)
- [x] Created MANIFEST.in for file inclusion
- [x] Created README_PACKAGE.md with comprehensive documentation
- [x] Created example.py with 10 test cases
- [x] Updated llm_safety_guard.py with all 7 detectors
- [x] Verified package structure with `python setup.py check`

## 📋 Pre-Publishing Steps (DO THESE BEFORE BUILDING)

### 1. Update Author Email
- [ ] Edit `setup.py` line 17: Change `author_email='your.email@example.com'` to your real email
- [ ] Edit `pyproject.toml` line 8: Change email in authors field

### 2. Test Locally
```bash
# Install in development mode
pip install -e .

# Test imports
python -c "from llm_safety_guard import Guard, Guards; print('Success!')"

# Run example
python example.py
```

### 3. Install Build Tools
```bash
pip install --upgrade build twine
```

## 🏗️ Build Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build package
python -m build
```

This creates:
- `dist/llm_safety_guard-0.1.0.tar.gz` (source distribution)
- `dist/llm_safety_guard-0.1.0-py3-none-any.whl` (wheel distribution)

## 🧪 Test on Test PyPI (RECOMMENDED)

### 4. Create Test PyPI Account
- [ ] Go to https://test.pypi.org/account/register/
- [ ] Verify email
- [ ] Enable 2FA

### 5. Create API Token for Test PyPI
- [ ] Go to https://test.pypi.org/manage/account/
- [ ] Scroll to "API tokens" section
- [ ] Click "Add API token"
- [ ] Name: `llm-safety-guard-test`
- [ ] Scope: "Entire account" or specific project
- [ ] Copy token (starts with `pypi-`)

### 6. Upload to Test PyPI
```bash
python -m twine upload --repository testpypi dist/*
# Username: __token__
# Password: <paste your Test PyPI token>
```

### 7. Test Installation from Test PyPI
```bash
# Create a test environment
python -m venv test_env
test_env\Scripts\activate

# Install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ llm-safety-guard

# Test it works
python -c "from llm_safety_guard import Guard; print('Test PyPI Success!')"

# Deactivate
deactivate
```

## 🚀 Publish to Production PyPI

### 8. Create PyPI Account
- [ ] Go to https://pypi.org/account/register/
- [ ] Verify email
- [ ] Enable 2FA

### 9. Create API Token for PyPI
- [ ] Go to https://pypi.org/manage/account/
- [ ] Scroll to "API tokens" section
- [ ] Click "Add API token"
- [ ] Name: `llm-safety-guard`
- [ ] Scope: "Entire account" (first upload) or specific project
- [ ] Copy token (starts with `pypi-`)

### 10. Upload to PyPI
```bash
python -m twine upload dist/*
# Username: __token__
# Password: <paste your PyPI token>
```

### 11. Verify on PyPI
- [ ] Visit https://pypi.org/project/llm-safety-guard/
- [ ] Check package metadata
- [ ] Check README displays correctly

### 12. Test Installation
```bash
pip install llm-safety-guard
python -c "from llm_safety_guard import Guards; print('Production Success!')"
```

## 📝 Post-Publishing

### 13. Create Git Tag
```bash
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0
```

### 14. Create GitHub Release
- [ ] Go to your GitHub repository
- [ ] Click "Releases" → "Create a new release"
- [ ] Tag: v0.1.0
- [ ] Title: "v0.1.0 - Initial Release"
- [ ] Description: Copy from CHANGELOG or README highlights
- [ ] Attach dist files (optional)

### 15. Update Documentation
- [ ] Add PyPI badge to README: `[![PyPI version](https://badge.fury.io/py/llm-safety-guard.svg)](https://badge.fury.io/py/llm-safety-guard)`
- [ ] Add installation instructions
- [ ] Update project README.md with package link

## 🔄 For Future Updates

### Version Bumping
1. Update version in `setup.py` (line 15)
2. Update version in `pyproject.toml` (line 6)
3. Update CHANGELOG
4. Rebuild: `python -m build`
5. Upload: `python -m twine upload dist/*`
6. Tag: `git tag -a v0.x.x -m "Release v0.x.x"`

### Version Numbering (SemVer)
- **0.1.0 → 0.1.1**: Bug fixes, no new features (patch)
- **0.1.0 → 0.2.0**: New features, backward compatible (minor)
- **0.1.0 → 1.0.0**: Breaking changes (major)

## 🐛 Troubleshooting

### "File already exists"
- Package name taken → Change name in setup.py and pyproject.toml
- Uploading same version → Bump version number

### "Invalid distribution"
- Missing README_PACKAGE.md → Check file exists
- Setup.py errors → Run `python setup.py check`

### Import errors after install
- Missing __init__.py → Check all package directories
- Missing dependencies → Check requirements.txt and setup.py install_requires match

### README not rendering on PyPI
- Markdown syntax → Test with `python -m readme_renderer README_PACKAGE.md`
- Image paths → Use absolute URLs, not relative paths

## 📞 Support

- PyPI Help: https://pypi.org/help/
- Packaging Guide: https://packaging.python.org/
- Twine Docs: https://twine.readthedocs.io/

---

**Current Status**: Package structure complete, ready for Step 1 (update email)

**Next Action**: Update author email in setup.py and pyproject.toml, then proceed with local testing
