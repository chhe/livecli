#!/bin/bash
UPSTREAM_REPO="livecli"
CLI="livecli"

usage() {
  echo "This will prepare $CLI for release!"
  echo ""
  echo "Requirements:"
  echo " git"
  echo " gpg - with a valid GPG key already generated"
  echo " github-release"
  echo " GITHUB_TOKEN in your env variable"
  echo " "
  echo "Not only that, but you must have permission for:"
  echo " Tagging releases within Github"
  echo ""
}

requirements() {
  if [ ! -f /usr/bin/git ] && [ ! -f /usr/local/bin/git ]; then
    echo "No git. What's wrong with you?"
    exit 1
  fi

  if [ ! -f /usr/bin/gpg ] && [ ! -f /usr/local/bin/gpg ]; then
    echo "No gpg. What's wrong with you?"
    exit 1
  fi

  if [ ! -f $GOPATH/bin/github-release ]; then
    echo "No github-release. Please run 'go get -v github.com/aktau/github-release'"
    echo "or run"
    echo "export GOPATH=\$HOME/go"
    echo "export PATH=\$PATH:\$GOROOT/bin:\$GOPATH/bin"
    exit 1
  fi

  if [[ -z "$GITHUB_TOKEN" ]]; then
    echo "export GITHUB_TOKEN=yourtoken needed for using github-release"
    exit 1
  fi
}

# Clone upstream master
clone() {
  git clone ssh://git@github.com/$UPSTREAM_REPO/$CLI.git
  if [ $? -eq 0 ]; then
        echo OK
  else
        echo FAIL
        exit
  fi
}

test_changelog() {
  # Test Changelog
  cd $CLI
  if grep --quiet "Livecli $1" CHANGELOG.rst ; then
    echo "OK - Found version"
  else
    echo "!!!"
    echo "FAIL - No version $1 in the changelog"
    echo "Update the changelog on github"
    echo "cleanup the release or manually git pull"
    echo "RUN THIS TEST AGAIN"
    echo "!!!"
  fi
  cd ..
}

sign() {
  # Tarball it!
  cd $CLI
  git tag $1
  python setup.py sdist
  mv dist/$CLI-$1.tar.gz ..
  cd ..

  # Sign it!
  echo -e "SIGN THE TARBALL!\n"
  gpg --detach-sign --armor $CLI-$1.tar.gz
  if [ $? -eq 0 ]; then
        echo SIGN OK
  else
        echo SIGN FAIL
        exit
  fi

  echo ""
  echo "The tar.gz. is now located at $CLI-$1.tar.gz"
  echo "and the signed one at $CLI-$1.tar.gz.asc"
  echo ""
}

push() {
  CHANGES="Changelog pending ..."
  # Release it!
  $GOPATH/bin/github-release release \
      --user $UPSTREAM_REPO \
      --repo $CLI \
      --tag $1 \
      --name "$1" \
      --description "$CHANGES"
  if [ $? -eq 0 ]; then
        echo RELEASE UPLOAD OK
  else
        echo RELEASE UPLOAD FAIL
        exit
  fi

  $GOPATH/bin/github-release upload \
      --user $UPSTREAM_REPO \
      --repo $CLI \
      --tag $1 \
      --name "$CLI-$1.tar.gz" \
      --file $CLI-$1.tar.gz
  if [ $? -eq 0 ]; then
        echo TARBALL UPLOAD OK
  else
        echo TARBALL UPLOAD FAIL
        exit
  fi

  $GOPATH/bin/github-release upload \
      --user $UPSTREAM_REPO \
      --repo $CLI\
      --tag $1 \
      --name "$CLI-$1.tar.gz.asc" \
      --file $CLI-$1.tar.gz.asc
  if [ $? -eq 0 ]; then
        echo SIGNED TARBALL UPLOAD OK
  else
        echo SIGNED TARBALL UPLOAD FAIL
        exit
  fi

  echo "DONE"
  echo "DOUBLE CHECK IT:"
  echo "!!!"
  echo "https://github.com/$UPSTREAM_REPO/$CLI/releases/edit/$1"
  echo "!!!"
}

clean() {
  rm -rf $CLI $CLI-$1 $CLI-$1.tar.gz $CLI-$1.tar.gz.asc $CLI-$1.exe changes.txt
}

main() {
  local cmd=$1
  usage
  requirements

  echo ""
  echo "First, please enter the version of the NEW release: "
  read VERSION
  echo "You entered: $VERSION"
  echo ""

  echo ""
  echo "Second, please enter the version of the LAST release: "
  read PREV_VERSION
  echo "You entered: $PREV_VERSION"
  echo ""

  clear

  echo "Now! It's time to go through each step of releasing $CLI!"
  echo "If one of these steps fails / does not work, simply re-run ./release.sh"
  echo "Re-enter the information at the beginning and continue on the failed step"
  echo ""

  PS3='Please enter your choice: '
  options=(
  "Git clone master"
  "Test changelog"
  "Tarball and sign - requires gpg key"
  "Upload the tarball and source code to GitHub release page"
  "Clean"
  "Quit")
  select opt in "${options[@]}"
  do
      echo ""
      case $opt in
          "Git clone master")
              clone $VERSION
              ;;
          "Test changelog")
              test_changelog $VERSION
              ;;
          "Tarball and sign - requires gpg key")
              sign $VERSION
              ;;
          "Upload the tarball and source code to GitHub release page")
              push $VERSION
              ;;
          "Clean")
              clean $VERSION
              ;;
          "Quit")
              clear
              break
              ;;
          *) echo invalid option;;
      esac
      echo ""
  done
}

main "$@"
