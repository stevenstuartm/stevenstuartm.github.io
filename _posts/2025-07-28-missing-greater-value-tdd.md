---
layout: post
title: "I Think We Are Missing the Greater Value of Test-Driven Development"
date: 2025-07-28
tags: [tdd, testing, software-design, best-practices]
description: "Reframing TDD as testing assumptions rather than just code—executable business hypotheses that prevent building the wrong thing."
---

I've always struggled with TDD's theoretical promise versus practical reality. The constant test rewrites during discovery, mocking unknown contracts, building for domains you don't yet understand—it often feels wasteful. From my own work, I often get the same results but more quickly (or I think so anyway) by focusing on discovery and then leveraging personal discipline to write the correct tests. Beyond the time suck contention, I confess that it is somewhat self-evident that having assertions mocked upfront can help you maintain focus on all needs and to not get lost in the weeds of what you value the most as you develop one aspect of the code more than another. But even then, management often agrees with the skeptics and I do not blame them.

And yet... I think that I and so many others have been framing TDD in a way which is not only sub-optimal but is guaranteed to create division. So here is my attempt to create unity even if my proposition does not reflect what TDD is originally and strictly meant for.

## The Problem

We see TDD primarily as a code quality tool. Advocates measure test coverage while skeptics see rewritten tests as waste. Both may be missing the greater potential.

## The Real Value

TDD isn't just testing code—it's also testing assumptions. Every test can be an executable hypothesis about user needs or business logic. When tests change or are even removed during the process of discovery when implementing, they're actually delivering their core value: proving which assumptions were wrong or missing before you built the wrong thing.

## The Reframe

Think "executable business hypotheses" not only "code quality practice." TDD becomes a business intelligence tool that prevents the costliest software mistake: solving the wrong problem. Code discovery proves the original assertion as much as the assertion proves the code.

Altered and even discarded tests have ROI—they're evidence of assumptions validated or disproven before expensive implementation. Instead of arguing about test coverage percentages, we focus on assumption coverage: How quickly can we validate our riskiest beliefs about what users actually need?

## The Bottom Line

The goal isn't perfect tests—it's perfect understanding.