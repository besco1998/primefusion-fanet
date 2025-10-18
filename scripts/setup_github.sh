#!/bin/bash
# GitHub Repository Setup Script for PrimeFusion-FANET

echo "==================================================================="
echo "PrimeFusion-FANET GitHub Repository Setup"
echo "==================================================================="
echo ""

# Navigate to project root
cd /home/ubuntu/primefusion-project

# Initialize git if not already initialized
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
    echo "✓ Git repository initialized"
else
    echo "✓ Git repository already initialized"
fi

# Configure git user (update with your details)
echo ""
echo "Configuring Git user..."
read -p "Enter your GitHub username: " github_user
read -p "Enter your email: " github_email

git config user.name "$github_user"
git config user.email "$github_email"
echo "✓ Git user configured"

# Add all files
echo ""
echo "Staging files..."
git add .
echo "✓ Files staged"

# Initial commit
echo ""
echo "Creating initial commit..."
git commit -m "Initial commit: PrimeFusion-FANET project structure

- Python implementation (proof-of-concept)
- NS-3 simulation framework (structure)
- Comprehensive documentation
- Research reports and analysis
- Testing infrastructure
- Results and visualization tools"
echo "✓ Initial commit created"

# Create GitHub repository (requires authentication)
echo ""
echo "==================================================================="
echo "GitHub Repository Creation"
echo "==================================================================="
echo ""
echo "To create the GitHub repository, you need to authenticate first:"
echo ""
echo "Option 1: Use GitHub CLI (recommended)"
echo "  1. Run: gh auth login"
echo "  2. Follow the prompts to authenticate"
echo "  3. Then run: gh repo create primefusion-fanet --public --source=. --push"
echo ""
echo "Option 2: Create repository manually on GitHub"
echo "  1. Go to https://github.com/new"
echo "  2. Create a new repository named 'primefusion-fanet'"
echo "  3. Then run:"
echo "     git remote add origin https://github.com/$github_user/primefusion-fanet.git"
echo "     git branch -M main"
echo "     git push -u origin main"
echo ""
echo "==================================================================="
echo "Setup complete! Choose an option above to push to GitHub."
echo "==================================================================="

