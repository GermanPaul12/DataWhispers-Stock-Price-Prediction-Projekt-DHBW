#!/bin/bash
mkdir result

for file in *.pickle; do mv $file ${file:5}; done
for file in *.pickle; do mv $file ${file/_trainEval/}; done
for file in *.pickle; do mv $file ./result/${file/_onData_/_}; done
