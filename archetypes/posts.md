---
title: "{{ replace .File.ContentBaseName `-` ` ` | title }}"
date: {{ .Date }}
draft: true
summary: ""
tags: []
categories: []
series: []
showTableOfContents: true
---

**Problem.** What was broken, and why it mattered. One paragraph a busy engineer can read in 20 seconds.

## Context

What the system looked like before, the constraints you were under, and what you had already ruled out.

## Diagnosis

How you narrowed it down. Keep the dead ends in — they save the reader the most time.

## Fix

The change itself. Code, config, or process. Link to the commit if it is public.

## Lessons

What you would do differently next time. This is the section people actually quote, so make it specific.
