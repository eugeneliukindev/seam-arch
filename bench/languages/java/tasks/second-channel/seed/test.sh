#!/bin/sh
# Compiles src/ and test/ into build/ and runs every *Test class; stops at the first failure.
set -eu
cd "$(dirname "$0")"
rm -rf build
javac -d build $(find src test -name '*.java')
for test in $(cd test && find . -name '*Test.java' | sed 's|^\./||; s|\.java$||; s|/|.|g'); do
  java -cp build "$test"
done
