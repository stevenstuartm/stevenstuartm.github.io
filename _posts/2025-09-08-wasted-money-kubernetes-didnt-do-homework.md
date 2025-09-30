---
layout: post
title: "I Wasted $$$ on Kubernetes Because I Didn't Do My Homework"
date: 2025-09-08
tags: [kubernetes, aws, architecture, lessons-learned]
description: "A lesson in avoiding technology hype—how I wasted $2K/month on Kubernetes when simpler solutions like AWS ECS were a better fit."
---

So I messed up...

Over 2 years ago I threw Kubernetes into the "adopt" circle on our tech radar without really thinking it through. Everyone was talking about it, it looked cool, and honestly I wanted to play with it. I knew better, right?

Fast forward to last month—I finally moved everything to AWS ECS and immediately saved $2K/month while making my life waaaaaaaaaaaaay easier. Like, I can actually sleep again.

## This One's on Me

Kubernetes didn't fail. I did. As a software architect, my job is to research this stuff properly and understand the tradeoffs before we commit. Instead I got caught up in the hype and made an expensive assumption. We did learn a lot about k8s best practices, but it was not enough to stop the bleeding.

I should have asked better questions and been more honest:

- Do we actually need multi-cloud deployment? **(No)**
- Are we running hundreds of microservices? **(We had like 20 containers)**
- Do we have platform engineers who want to manage this thing? **(No)**
- Is the operational overhead worth it for our team size? **(No)**
- Do we want to deal with an additional auth layer which is not cloud native? **(No)**
- Do we want to constantly tweak our deployments to make the most of our node costs? **(No)**

But I didn't, not really. I just saw everyone else doing it and figured we should too.

## What Kubernetes Is Actually For

Turns out K8s is built for companies with massive scale and dedicated platform teams. If you're Google running thousands of services, it's perfect. If you're a 20-person startup with a dozen containers, it's like buying a semi truck to deliver pizza.

Most of us just need our apps to run reliably without babysitting a cluster every weekend.

## What I Use Now

ECS Fargate. That's it. No cluster to manage, scales automatically, integrates with everything else on AWS. Of course, there are similar solutions; ECS is just what I determined was the most cost effective for me.

## The Lesson

When something looks shiny and new, actually dig into whether you need it before you put it on your roadmap. The boring and simple solution is usually the right solution.