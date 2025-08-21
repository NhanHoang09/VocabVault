#!/bin/bash

echo "🔍 Checking Git Repository Status for My Vocabulary Vault"
echo "=================================================="

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not in a git repository!"
    exit 1
fi

echo "✅ Main git repository found"

# Check for any nested git repositories
echo ""
echo "🔍 Checking for nested git repositories..."
nested_gits=$(find . -name ".git" -type d | grep -v "^./.git$")

if [ -z "$nested_gits" ]; then
    echo "✅ No nested git repositories found"
else
    echo "⚠️  Found nested git repositories:"
    echo "$nested_gits"
    echo ""
    echo "💡 You may want to remove these to avoid conflicts"
fi

# Check git status
echo ""
echo "📊 Git Status:"
git status --short

# Show current branch
echo ""
echo "🌿 Current branch: $(git branch --show-current)"

# Show last commit
echo ""
echo "📝 Last commit:"
git log -1 --oneline

# Show remote repositories
echo ""
echo "🔗 Remote repositories:"
git remote -v

echo ""
echo "🎯 Repository is ready for development!"
echo ""
echo "📋 Available commands:"
echo "  - git add .                    # Add all changes"
echo "  - git commit -m 'message'      # Commit changes"
echo "  - git push origin main         # Push to remote"
echo "  - git remote add origin <url>  # Add remote repository"
