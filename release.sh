#!/bin/bash

# ========================================
# 🚀 HOW TO RUN THIS SCRIPT (IMPORTANT)
# ========================================
# 1. Open Git Bash (NOT PowerShell)
# 2. Navigate to project folder
# 3. Run:
#    chmod +x release.sh   (first time only)
#    ./release.sh
#
# OR directly:
#    bash release.sh
#
# ========================================
# 🚀 RELEASE SCRIPT STARTS
# ========================================

echo "🚀 RELEASE STARTED"
echo "--------------------------------"

git checkout main
git pull origin main
git fetch --tags

LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null)

if [ -z "$LATEST_TAG" ]; then
  LATEST_TAG="v1.0.0"
fi

echo "📌 Latest tag: $LATEST_TAG"

echo "--------------------------------"

COMMITS=$(git log ${LATEST_TAG}..HEAD --oneline)

if [ -z "$COMMITS" ]; then
  echo "⚠️ No new commits since last release!"
  read -p "❓ Still create new tag? (y/n): " FORCE

  if [ "$FORCE" != "y" ]; then
    echo "✅ Skipping release. Nothing to do."
    exit 0
  fi
fi

echo "📜 Changes:"
echo "$COMMITS"

echo "--------------------------------"

VERSION=${LATEST_TAG#v}
IFS='.' read -r MAJOR MINOR PATCH <<< "$VERSION"
PATCH=$((PATCH+1))

SUGGESTED_TAG="v$MAJOR.$MINOR.$PATCH"

echo "💡 Suggested tag: $SUGGESTED_TAG"

read -p "👉 Enter tag (or press Enter): " USER_TAG

if [ -z "$USER_TAG" ]; then
  NEW_TAG=$SUGGESTED_TAG
else
  NEW_TAG=$USER_TAG
fi

echo "🚀 Selected: $NEW_TAG"

read -p "❓ Proceed with tagging? (y/n): " CONFIRM

if [ "$CONFIRM" != "y" ]; then
  echo "❌ Cancelled"
  exit 0
fi

git tag $NEW_TAG
git push origin $NEW_TAG

echo "✅ Tag pushed: $NEW_TAG"

read -p "📦 Create GitHub Release? (y/n): " CREATE_RELEASE

if [ "$CREATE_RELEASE" == "y" ]; then
  if command -v gh &> /dev/null; then
    gh release create $NEW_TAG \
      --title "🚀 Release $NEW_TAG" \
      --notes "$COMMITS"
    echo "✅ Release created"
  else
    echo "⚠️ gh CLI not installed"
  fi
else
  echo "⏭️ Release skipped"
fi

echo "🎯 DONE"

# ========================================
# 🧪 TEST CASES
# ========================================
# Case 1: No commits → exits safely
# Case 2: Skip manually → exits cleanly
# Case 3: Full run → tag + release created
# ========================================