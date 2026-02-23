---
layout: post
title: "How One Screen Holds the Entire Industry Hostage"
date: 2026-02-17
tags: [architecture, web-development, mobile, pwa, cross-platform]
description: "The web platform already does what most apps do, but Apple's control of the phone screen keeps the industry building native. The 'users prefer native' narrative is circular logic created by the constraint itself."
---

Frameworks like React Native, Flutter, and MAUI keep promising to end the "write it twice" problem across mobile platforms. One codebase, every platform, native-quality results. Yet every time, the abstraction leaks, and then it floods so fast that bailing water is all you have time to do. I've been working with MAUI recently, and the experience crystallized a question I should have asked sooner: why am I not just building a website?

This isn't an argument that native apps are obsolete or that local executables should disappear. There are good reasons to run code on your own hardware, and the pure thin-client terminal hasn't arrived yet; maybe it shouldn't. But when teams default to native without questioning it, they accept costs and constraints on the client side that the backend abandoned years ago.

Once you pull that thread, it unravels fast. The web platform's capability surface is far larger than the industry acknowledges, and nearly everything preventing universal web adoption is inertia, business incentives, or mental models rather than real technical constraints.

<blockquote class="pull-quote">
<p>The web can do the job. One company made sure you'd never trust it to.</p>
</blockquote>

## What the Web Platform Can Actually Do

The capabilities list for the modern web is longer than most developers and decision-makers expect. For the typical business application, whether it runs on a phone, a tablet, or a desktop, the web platform already covers the core requirements:

| Capability                             | Web Technology                                     |
|----------------------------------------|----------------------------------------------------|
| Offline support                        | Service Workers, Cache API                         |
| Push notifications                     | Push API (iOS 16.4+, March 2023)                   |
| Camera, microphone, biometrics         | getUserMedia, WebAuthn/Passkeys                    |
| Payment processing                     | Payment Request API (includes Apple Pay)           |
| Home screen installation               | Web App Manifest, standalone window                |
| GPU-accelerated graphics and compute   | WebGPU (all major browsers, Nov 2025)              |
| Peripheral device access               | WebUSB, WebSerial, WebBluetooth, WebHID (Chromium) |
| Local file access                      | File System Access API, Origin Private File System |
| Near-native performance                | WebAssembly, Web Workers                           |
| Real-time communication                | WebRTC                                             |

That list covers what the vast majority of apps in the App Store and on corporate desktops actually do. Most applications are thin clients over an API: they authenticate a user, fetch data, display it in a list or form, and let the user interact with it. The web handles all of that with a single codebase that runs on every platform with a browser. The deployment model alone should make teams reconsider. Web apps update instantly through the server. No App Store review cycles, no waiting days for a critical bug fix to clear approval, no maintaining separate release pipelines for each platform.

## What Genuinely Requires Native

The web can't do everything. Some capabilities have no web equivalent and genuinely require native development.

- **Wearable integration and health data** like Apple Watch complications, Wear OS tiles, HealthKit, and Google Health Connect require platform SDKs with no web alternative
- **Advanced augmented reality** using LiDAR scanning, scene understanding, and body tracking exceeds what WebXR currently offers
- **Deep OS integration** like Siri Shortcuts, Google Assistant routines, home screen widgets, and inter-app communication remains outside the web's reach
- **True background processing** for geofencing, long-running background jobs, and persistent location tracking requires native APIs
- **Specific hardware access** like NFC writing on iOS, advanced camera controls, and screenshot blocking are native-only capabilities

This list is relevant, but it's also narrow. Look at the apps on your phone and the software on your desktop, and count how many actually need any of these features.

## Cross-Platform Frameworks Are the Wrong Answer

Cross-platform frameworks don't eliminate the two-codebase problem; they disguise it. You still end up dealing with platform-specific workarounds, conditional rendering logic, and bugs that only reproduce on one platform. Abstractions like React Native's bridge architecture, Flutter's custom rendering engine, and MAUI's handler pattern each introduce their own category of bugs that don't exist in either native platform. You haven't removed the platform differences; you've added a third abstraction layer on top of two platforms and inherited all three bug surfaces.

The tech debt is unprojectable because you don't control the framework's roadmap. When Apple changes something in a new iOS release, you wait for the framework to catch up. When the framework ships breaking changes, you're locked into an upgrade you didn't plan for. When a critical bug sits in the issue tracker for months, your only options are workarounds or forks.

The original economic justification for cross-platform frameworks was that hiring specialized native developers is expensive, so share code to reduce cost. AI code generation has collapsed that constraint. A competent developer with AI assistance can ship Swift or Kotlin without years of prior experience. The hiring cost advantage that justified the abstraction overhead is gone, but all the original disadvantages remain.

## Two Companies, Two Arcs

To understand why the web hasn't become the default, it helps to look at how the two most influential companies in software development have traded places.

In the early 2000s, Microsoft was the villain. They owned the desktop, the browser, the runtime, and the development tools, and they used that control aggressively. The DOJ antitrust case in 2001 was about exactly this: using a Windows monopoly to crush Netscape and control how people accessed the internet. Apple, by contrast, was the scrappy alternative making beautiful things for creative people. When the iPhone launched in 2007, it felt like liberation from the clunky, carrier-controlled mobile landscape.

Then each company lost something important, and their responses tell you everything.

Microsoft lost mobile and Windows 8 alienated more and more desktop users. Their response was to stop trying to own the screen and instead to compete on the stack. .NET went open source, Visual Studio Code became the most popular editor in the world, they acquired GitHub and kept it open, and Azure now runs more Linux workloads than Windows. The company that once tried to kill Linux now employs more Linux kernel contributors than most Linux companies.

I am still baffled why Microsoft did not backpedal their bloated OS and clunky UX for Desktop as soon as their market assumptions proved to be so very wrong. Windows seems to have gotten worse with each version and with no sign of redemption. Two steps forward and one step back.

Apple very quickly went the other direction. When the iPhone became the dominant computing device, Apple discovered what Microsoft had known in the 1990s: if you control the platform people depend on, you don't have to compete on openness. You compete on control.

I write .NET code for a living and I choose to do it on a Mac because the experience is genuinely better. Notice what that sentence reveals about both companies though. Microsoft made that possible by building .NET and VS Code to run everywhere, making the deliberate decision that their tools should work regardless of platform. Try the reverse. Try building an iOS app without a Mac. Try submitting to the App Store without Xcode. Try running Swift development tooling on Windows with the same first-class support that .NET has on macOS. You can't. Microsoft earns wise developers and enterprise companies by being useful regardless of platform. Apple captures developers by making their platform mandatory.

Apple's products deserve their loyalty. The Mac is excellent, the ecosystem integration is seamless, and users trust the brand for good reasons. That trust is exactly what makes the constraint so effective. When a company makes products this good, people don't scrutinize the walls. They assume the walls exist for good reasons.

But look at what Apple controls versus what they build. Siri has been outperformed by competitors for over a decade, and it doesn't matter because Siri doesn't need to be good; it needs to be on the iPhone. Owning the screen means you don't have to be the best at anything that runs on it; you just need to be good enough at the thing people hold, and everything else flows through you.

<blockquote class="pull-quote">
<p>Apple doesn't compete on technology. They compete on constraint ownership. The phone is the aperture, and Apple controls the aperture.</p>
</blockquote>

## The Walls Apple Built

The walls Apple has constructed around iOS are higher than anything Microsoft built around Windows in the 1990s, and they're more sophisticated because they're framed as user protection rather than vendor control.

Every browser on iOS must use Apple's WebKit rendering engine. Chrome on your iPhone isn't really Chrome. It's a WebKit skin with Chrome's UI on top. Firefox, Edge, Brave: all WebKit underneath. This means Apple alone controls what web capabilities exist on every iOS device, regardless of which browser icon a user taps.

On Chrome and Android, web apps can access over 47 Web APIs including Bluetooth, NFC, Background Sync, USB, and serial devices. On iOS, none of those APIs are available on any browser. In June 2020, Apple publicly rejected 16 Web APIs citing "privacy and fingerprinting concerns." Android handles the same APIs with straightforward permission prompts. The privacy argument doesn't hold up when every other platform manages these capabilities without the problems Apple claims are unsolvable.

Chrome on Android supported push notifications in 2015. iOS didn't get web push until March 2023, an eight-year gap for one of the most fundamental features an app needs. And even then, Apple's implementation requires users to first install the web app to their home screen before they can receive notifications. On Android, any website can request push permission.

The EU's Digital Markets Act forced Apple's hand on browser engine choice in 2024, but the response was revealing. Rather than comply, Apple attempted to remove PWA support entirely in the EU, converting installed web apps into simple bookmarks that lost all their data, offline capability, and push notifications. Their justification was that alternative browser engines would create "complex security and privacy concerns." The developer community pushed back hard. Open Web Advocacy organized an open letter to Tim Cook that gathered over 4,200 individual signatures and 441 organizations. The European Commission sent formal inquiries. Within two weeks, Apple reversed the decision. If the security concerns were genuine, they wouldn't have evaporated under two weeks of public pressure.

And even after the DMA technically required browser engine choice on iOS, as of early 2026, zero browsers have shipped a non-WebKit engine on iOS in the EU. Apple's technical and financial barriers make it unviable in practice. The regulation exists on paper. The WebKit monopoly persists in reality.

The financial incentive is straightforward. The App Store generated approximately $27 billion in commissions in 2024 on a 30% cut. Every app that ships as a web app is revenue Apple doesn't collect. The U.S. Department of Justice made this connection explicit in their March 2024 antitrust lawsuit, which specifically cites the WebKit requirement as part of Apple's monopoly maintenance strategy.

Android doesn't have these restrictions. Chrome supports the full suite of web APIs, Google actively advances web standards, and PWAs work as first-class applications on Android devices. But it doesn't matter. No product leader will ship something that doesn't work on iPhones, because Apple's users represent the highest-value demographic in every Western market. The most constrained major platform sets the ceiling for what anyone is willing to build, and every platform-neutral decision gets made against Apple's restrictions by default.

## The Circular Logic of "Users Prefer Native"

The most common justification for building native apps is market data showing that users spend 88-92% of their mobile time in apps and only 8-12% in browsers. Native apps retain users at 32% after 90 days compared to 20% for web apps. Mobile banking sees 50% more transactions through native apps. The data seems decisive.

But this is a post-hoc fallacy dressed up as market research. Users spend time in apps because apps are what gets built, promoted, funded, and placed on their home screens. Native gets the discovery mechanisms, the design talent, and the push notification support. Web experiences get a fraction of the budget and are treated as a fallback for users who haven't installed the app yet.

Of course the native experience retains users better; it received ten times the investment. Of course users spend more time in apps; they were never given an equivalent web alternative. You cannot measure user preference when one option was deliberately hobbled by the platform owner and underfunded by the developer.

The developer survey data has the same circularity. Flutter and React Native adoption is growing, but these frameworks exist specifically because Apple won't let the web do what it already does on every other platform. They're not evidence that native development is inherently better. They're evidence that the industry has responded to Apple's artificial restrictions by building billion-dollar workarounds rather than questioning the constraint.

A developer considers building a web app, checks iOS capabilities, and finds that background sync doesn't work, push notifications require a home screen install, and Bluetooth is unavailable. So they build native. That decision gets counted in a survey as evidence that the web isn't ready. The constraint creates the behavior that justifies the constraint.

The counterfactual has never been tested at scale because Apple has prevented it. Equivalent web and native experiences have never existed on iOS. The assumption that native is inherently superior has become so embedded that most teams skip straight to "which framework?" without ever stopping at "does this need to be an app?"

The few times the counterfactual has been tested, the results are telling. The Financial Times left the App Store in 2011 and went web-only; they're still web-first over a decade later. Starbucks built a PWA that was 99.84% smaller than their iOS app and doubled daily active users. But even Starbucks kept the native app alongside it, which raises an important question I can't answer: did they keep it because native was genuinely better, or because no one in the room was willing to ask "why do we still have this?"

## The Anxiety That Predates Mobile

When the iPhone launched in 2007, Steve Jobs told developers to build web apps. The web genuinely wasn't ready, and the App Store arrived a year later. But the response to that technical gap matters more than the gap itself. Rather than rallying behind closing it, the industry built an entirely parallel native ecosystem, following a pattern that has repeated since the 1960s: every generation of computing produces a viable thin-client model, and every generation finds reasons to reject it. Mainframe terminals gave way to PCs. Sun's network computer was technically sound and commercially dead. Chromebooks were dismissed for years as laptops that couldn't work offline, even as every application people actually used was migrating to the browser. The anxiety is always the same: if computation lives somewhere else, you lose control. That concern carries emotional weight far beyond its practical relevance today, and companies that profit from local-first computing have always been happy to amplify it.

The backend already completed the thin-client transition. Cloud won decisively; nobody serious argues for on-premises-first anymore. But the frontend is frozen at the same conceptual barrier that existed when the first PC replaced the first terminal. We accepted that our servers are someone else's computers. We haven't accepted that our applications could be someone else's rendering.

Mobile is also the reason the web became capable enough to challenge native at all. Service workers, WebGL, touch APIs, and WebAssembly weren't inevitable. They were a competitive response to native threatening to make the web irrelevant. The ecosystem that pressured the web into becoming a genuine application platform is now the same ecosystem preventing it from being used as one.

Cloud broke through because no single company controlled the server. The web can't break through until it works on Apple's phone, and Apple decides what works on Apple's phone.

## Progress Often Comes by Getting Out of Its Way

Before writing that new shiny app, ask yourselves: "Do we have a specific, documented constraint that the web platform cannot satisfy?"

For most mobile software needs, the answer is no. The web runs everywhere, deploys instantly, requires no framework intermediary, and its capability surface grows with every browser release. Cross-platform frameworks tried to solve platform fragmentation by adding another platform on top. The web solved it by being the platform that was already there. In Android-dominant markets like India and Southeast Asia, companies like Flipkart and JioSaavn have already proven this works: one codebase, instant deployment, no App Store tax.

The immediate objection is discoverability. People find apps by searching the App Store, so if you're not in the store, you're invisible. But most app discovery doesn't actually happen through store browsing; it happens through web search, social media, ads, and word of mouth. The store is more of a checkout counter than a shopping mall. Google Play already supports Trusted Web Activities, which let PWAs appear as store listings. The Microsoft Store accepts PWAs directly. For enterprise and B2B products, store discovery was never relevant to begin with. The discoverability argument is narrower than it sounds, and it gets narrower every year as deep links, QR codes, and social sharing put users directly into web experiences without a store in between.

The pragmatic strategy might be web-first. Build for the browser as the default platform, and only build native when a specific capability genuinely can't be delivered through the web. The web app is your product. The native app, if you need one at all, exists only for the features that Apple won't let the browser handle.

Cost, velocity, and agility shouldn't be values we only demand from our backend infrastructure. The same expectations that drove the industry from on-premises servers to cloud should apply to how we build and deliver client software. Native apps aren't going away, and they shouldn't. But we should be progressing toward both efficiency and sustainability rather than accepting a status quo where one company's business model determines how the entire industry ships code.
