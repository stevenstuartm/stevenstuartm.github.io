---
layout: post
title: "TDD Tests Assumptions, Not Just Code"
date: 2025-07-28
series: "Development Practice"
tags: [tdd, testing, software-design, best-practices]
description: "Reframing TDD as testing assumptions rather than just code: executable business hypotheses that prevent building the wrong thing."
---

I've been thinking about TDD's place in modern development, and I keep running into the same tension. The practical reality often contradicts the theoretical promise. Teams write tests for features they don't yet understand, design interfaces around incomplete requirements, and spend hours writing tests before discovering the domain model was wrong. Then they rewrite everything. The tests that guided development get thrown away.

This feels wasteful. Many experienced developers achieve similar results through focused discovery followed by disciplined testing, delivering quality code without strict TDD adherence. The debates get heated: advocates measure test coverage and celebrate red-green-refactor while skeptics count rewritten tests as waste.

But I think we're framing TDD wrong in a way that creates division rather than surfacing value. Both sides may be missing the greater potential.

## Testing Assumptions, Not Just Code

Most discussions about TDD frame it as a code quality tool. Write tests first, implement to make them pass, refactor for quality. The tests ensure correctness and prevent regressions. Coverage metrics become the measure of success.

But every test is also an executable hypothesis about user needs and business logic. When you write a test asserting business rules, you're testing assumptions about how the system should behave. When that test changes during discovery because requirements were misunderstood, the test delivered value by surfacing wrong assumptions before you built the wrong system.

Changed tests aren't waste; they're evidence of learning. The alternative is implementing vague requirements, shipping to production, and discovering the actual rules through production bugs.

## Executable Business Hypotheses

What if we reframed TDD as testing business assumptions rather than just testing code quality? The test suite becomes a living document of hypotheses about how the business works. When a test changes, you're not admitting failure; you're documenting discovered truth.

This shift changes how we evaluate TDD's value. Instead of measuring test coverage percentage, we measure how many wrong assumptions were caught before production. Instead of celebrating passing tests, we celebrate tests that revealed misunderstood requirements before implementation. Instead of viewing rewritten tests as waste, we recognize them as questions answered before building the wrong system.

Tests force specific questions that conversation alone won't surface. Writing executable assertions exposes complexity that wasn't obvious when discussing requirements abstractly. The test suite becomes documentation that new developers can read to understand system constraints without archeology through old conversations and tickets.

## What This Means Practically

Focus on testing assumptions that matter most to users and business logic. If requirements are clear and stable, write tests to validate implementation. If requirements are uncertain, write tests to validate assumptions and expect them to change as understanding develops.

Don't measure success by coverage percentage. Measure it by how many wrong assumptions were caught, how quickly tests surfaced ambiguity in requirements, and how often tests forced clarifying conversations that prevented bugs.

Stop debating "test-first versus test-after" and start asking: What assumptions are we making about user needs? What's the fastest way to validate them? Sometimes that's writing a test first, other times it's building a prototype first, and sometimes it's showing mockups to users first. The goal isn't perfect tests; it's perfect understanding.

The greatest value of TDD isn't in the tests that pass. It's in the tests that change because they revealed assumptions worth questioning. That's not waste. That's exactly the kind of failure worth having early.
