#!/bin/bash

set -e

echo ""
echo ""
echo ""
echo "============================================="
echo "Fixing Travis and Git stuff"
echo "============================================="

if [ z"$TRAVIS_PULL_REQUEST_SLUG" != z ]; then
	echo ""
	echo ""
	echo ""
	echo "- Adding pull request source repo"
	echo "---------------------------------------------"
	git remote add source https://github.com/$TRAVIS_PULL_REQUEST_SLUG
	echo "---------------------------------------------"

	echo ""
	echo ""
	echo ""
	echo "- Fetching pull request head"
	echo "---------------------------------------------"
	git fetch origin refs/pull/$TRAVIS_PULL_REQUEST/head:pull-head
	echo "---------------------------------------------"
	git log -n 5 --graph pull-head
	echo "---------------------------------------------"

	echo ""
	echo ""
	echo ""
	echo "- Fetching pull request merge"
	echo "---------------------------------------------"
	git fetch origin refs/pull/$TRAVIS_PULL_REQUEST/merge:merge-head
	echo "---------------------------------------------"
	git log -n 5 --graph merge-head
	echo "---------------------------------------------"
fi

echo ""
echo ""
echo ""
echo "- Fetching non-shallow"
echo "---------------------------------------------"
git fetch --unshallow

echo "- Fetching tags"
echo "---------------------------------------------"
git fetch --tags --all


if [ z"$TRAVIS_BRANCH" != z ]; then
	TRAVIS_COMMIT_ACTUAL=$(git log --pretty=format:'%H' -n 1)
	echo ""
	echo ""
	echo ""
	echo "Fixing detached head (current $TRAVIS_COMMIT_ACTUAL -> $TRAVIS_COMMIT)"
	echo "---------------------------------------------"
	git log -n 5 --graph
	echo "---------------------------------------------"
	git fetch origin $TRAVIS_COMMIT
	git branch -v
	echo "---------------------------------------------"
	git log -n 5 --graph
	echo "---------------------------------------------"
	git branch -D $TRAVIS_BRANCH || true
	git checkout $TRAVIS_COMMIT -b $TRAVIS_BRANCH
	git branch -v
	echo
fi

echo "============================================="

GIT_REVISION=$(git describe)

set -x

# Run the script once to check it works
time scripts/download-env.sh
# Run the script again to check it doesn't break things
time scripts/download-env.sh

set +x
set +e
source scripts/enter-env.sh
