#!/usr/bin/env python
import sys

def exec():
    metadata = sys.stdin.read()
    exec(metadata)
