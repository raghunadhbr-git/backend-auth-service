#!/bin/bash

# ==========================================================
# 🚀 HOW TO RUN THIS SCRIPT (VERY IMPORTANT)
# ==========================================================
# Step 1: Open VS Code → Terminal (Git Bash)
#
# Step 2: Give execute permission (ONLY FIRST TIME)
# chmod +x release.sh
#
# Step 3: Run the script
# ./release.sh
#
# ==========================================================
# WHAT THIS SCRIPT DOES
# ==========================================================
# ✅ Fetch latest tags from remote repository
# ✅ Detect latest version tag (vX.Y.Z format)
# ✅ Increment PATCH version automatically
# ✅ Create new tag
# ✅ Push new tag to GitHub
#
# Example:
# v1.0.0 → v1.0.1
# v1.0.1 → v1.0.2
#
# After push → GitHub Actions CI/CD will trigger automatically 🚀
# ==========================================================


echo "=========================================="
echo "🚀 STARTING RELEASE PROCESS"
echo "=========================================="

# ----------------------------------------------------------
# STEP 1: FETCH LATEST TAGS FROM REMOTE
# ----------------------------------------------------------
echo "🔄 Fetching latest tags from remote..."
git fetch --tags

# ----------------------------------------------------------
# STEP 2: GET LATEST TAG
# ----------------------------------------------------------
# Sort tags in descending order and pick latest
latest_tag=$(git tag --sort=-v:refname | head -n 1)

# ----------------------------------------------------------
# STEP 3: HANDLE FIRST RELEASE (NO TAG EXISTS)
# ----------------------------------------------------------
if [ -z "$latest_tag" ]; then
  echo "⚠️ No existing tags found."
  new_tag="v1.0.0"
else
  echo "📌 Latest tag found: $latest_tag"

  # --------------------------------------------------------
  # STEP 4: REMOVE 'v' PREFIX
  # --------------------------------------------------------
  version=${latest_tag#v}

  # --------------------------------------------------------
  # STEP 5: SPLIT VERSION INTO MAJOR.MINOR.PATCH
  # --------------------------------------------------------
  IFS='.' read -r major minor patch <<< "$version"

  # --------------------------------------------------------
  # STEP 6: INCREMENT PATCH VERSION
  # --------------------------------------------------------
  patch=$((patch + 1))

  # --------------------------------------------------------
  # STEP 7: CREATE NEW VERSION TAG
  # --------------------------------------------------------
  new_tag="v$major.$minor.$patch"
fi

echo "🚀 New tag will be: $new_tag"

# ----------------------------------------------------------
# OPTIONAL SAFETY CHECK (CONFIRM BEFORE PROCEEDING)
# ----------------------------------------------------------
read -p "👉 Type YES to confirm release: " confirm

if [ "$confirm" != "YES" ]; then
  echo "❌ Release cancelled by user."
  exit 1
fi

# ----------------------------------------------------------
# STEP 8: CREATE NEW TAG
# ----------------------------------------------------------
echo "🏷️ Creating new tag..."
git tag "$new_tag"

# ----------------------------------------------------------
# STEP 9: PUSH TAG TO REMOTE
# ----------------------------------------------------------
echo "📤 Pushing tag to origin..."
git push origin "$new_tag"

# ----------------------------------------------------------
# SUCCESS MESSAGE
# ----------------------------------------------------------
echo "=========================================="
echo "✅ RELEASE COMPLETED SUCCESSFULLY!"
echo "🎉 Tag pushed: $new_tag"
echo "🚀 CI/CD PIPELINE SHOULD TRIGGER NOW"
echo "=========================================="