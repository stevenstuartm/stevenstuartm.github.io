---
layout: post
title: "Why Are We Still Writing Two Mobile Apps?"
date: 2026-02-12
tags: [architecture, web-development, mobile, pwa, cross-platform]
description: "Cross-platform frameworks like MAUI, React Native, and Flutter promise 'write once, run everywhere' but deliver leaky abstractions and platform-specific workarounds. Progressive Web Apps can handle most of what business apps need today. The real question isn't which framework to pick; it's whether the approach itself is wrong."
---

Every few years, a new cross-platform mobile framework appears and promises to end the "write it twice" problem. React Native, Flutter, MAUI, Xamarin before it. The pitch is always the same: one codebase, every platform, native-quality results. And every time, the abstraction leaks.

I've been working with MAUI and React Native recently, and the experience has been a masterclass in frustration. A component that renders correctly on Android breaks on iOS. A gesture that works on a phone behaves differently on a tablet. Conditional platform checks start creeping into what was supposed to be shared code. Before long, you're not maintaining one codebase; you're maintaining one codebase that behaves like two, with a framework-specific debugging layer on top.

At some point during a particularly janky layout issue that only appeared on iOS, I stopped and asked the question that I think more developers should be asking: why not just build a website?

<blockquote class="pull-quote">
<p>The question isn't which cross-platform framework to pick. The question is whether the approach itself is wrong.</p>
</blockquote>

Progressive Web Apps have been around for years, and most developers either dismiss them as glorified bookmarks or assume they can't do anything meaningful. Both assumptions are wrong, and the gap between what PWAs can do and what most apps actually need is far smaller than the industry acknowledges.

## What PWAs Can Actually Do

The capabilities list for modern PWAs is longer than most developers expect. For the typical business application (forms, lists, dashboards, notifications, content delivery, e-commerce), PWAs already cover the core requirements:

- **Offline support** through service workers and the Cache API, with full control over what gets cached and how
- **Push notifications** on both Android and iOS (iOS added support in March 2023 with version 16.4)
- **Camera and microphone** access through getUserMedia, including video capture
- **Biometric authentication** via WebAuthn and Passkeys, supporting fingerprint and face recognition
- **Payment processing** through the Payment Request API, including Apple Pay
- **Home screen installation** with a standalone app window, separate from the browser
- **Real-time communication** via WebRTC for voice and video
- **Heavy computation** using Web Workers and WebAssembly, running off the main thread
- **Geolocation**, device orientation, clipboard access, media recording, and screen wake lock

That list covers what 80% of apps in the App Store actually do. Most mobile apps are thin clients over an API: they authenticate a user, fetch data, display it in a list or form, and let the user interact with it. A PWA handles all of that with a single codebase that runs on every platform with a browser.

The deployment model alone should make teams reconsider. PWAs update instantly through the web server. No App Store review cycles, no waiting days for a critical bug fix to clear approval, no maintaining separate release pipelines for iOS and Android. You deploy once and every user gets the update on their next visit.

## What Genuinely Requires Native

PWAs can't do everything. Some capabilities have no web equivalent and genuinely require native development:

**Home screen widgets** on iOS (WidgetKit) and Android have no PWA equivalent. If your product relies on glanceable information on the home screen, that's a native-only feature.

**Wearable integration** like Apple Watch complications and Wear OS tiles requires platform SDKs. There's no web API for smartwatch development.

**Health and fitness data** through HealthKit and Google Health Connect is native-only. Fitness trackers, health monitoring apps, and medical devices that need to read or write health data can't use PWAs for that integration.

**Advanced augmented reality** using the full capabilities of ARKit (LiDAR scanning, scene understanding, body tracking) or ARCore exceeds what WebXR currently offers. Basic AR works on the web, but production AR applications still need native SDKs.

**Deep OS integration** like Siri Shortcuts, Google Assistant routines, inter-app communication, and system-level controls remain outside the web platform's reach.

**True background processing** for tasks like geofencing (triggering actions when entering or leaving a location), long-running background jobs, and persistent background location tracking requires native APIs.

**Specific hardware access** like NFC writing (web NFC on Android is read-only), advanced camera controls (manual focus, RAW capture, multi-camera switching), and blocking screenshots are native-only capabilities.

This list is real and shouldn't be minimized. But it's also narrow. Look at the apps on your phone and count how many actually need any of these features. Most don't. Your banking app, your e-commerce app, your news reader, your project management tool, your internal company dashboard: none of them need widgets, wearables, health data, or AR. They need authentication, data display, forms, and notifications.

## The Elephant in the Room

If PWAs are this capable, why aren't more teams using them? The answer starts and ends with Apple.

The capability gap between PWAs and native apps is primarily an iOS problem, not a web platform problem. On Chrome and Android, PWAs can access over 47 Web APIs including Bluetooth, NFC, Background Sync, USB, and serial devices. On iOS, none of those APIs are available on any browser because Apple requires every browser on iOS to use its WebKit rendering engine. Chrome on your iPhone isn't really Chrome. It's a WebKit skin with Chrome's UI on top. Firefox, Edge, Brave: all WebKit underneath.

This means Apple alone controls what web capabilities exist on every iOS device, and the pace of that progress has been revealing.

Chrome on Android supported push notifications in 2015. iOS didn't get web push until March 2023, an eight-year gap for one of the most fundamental features a mobile app needs. And even then, Apple's implementation requires users to first install the PWA to their home screen before they can receive notifications. On Android, any website can request push permission.

In June 2020, Apple publicly rejected 16 Web APIs including Bluetooth, NFC, USB, battery status, and idle detection, citing "privacy and fingerprinting concerns." Android handles the same APIs with straightforward permission prompts. The privacy argument doesn't hold up when every other platform manages these capabilities without the problems Apple claims are unsolvable.

<blockquote class="pull-quote">
<p>The EU incident tells you everything you need to know about Apple's actual priorities.</p>
</blockquote>

In early 2024, when the EU's Digital Markets Act required Apple to allow alternative browser engines on iOS, Apple's response wasn't to comply gracefully. They attempted to remove PWA support entirely in the EU, converting installed web apps into simple bookmarks that lost all their data, offline capability, and push notifications. Their justification was that alternative browser engines would create "complex security and privacy concerns."

The developer community pushed back hard. Open Web Advocacy organized an open letter to Tim Cook that gathered over 4,200 individual signatures and 441 organizations. The European Commission sent formal inquiries. Within two weeks, Apple reversed the decision. If the security concerns were genuine, they wouldn't have evaporated in two weeks of public pressure.

Apple's financial incentive is straightforward. The App Store generated approximately $27 billion in commissions in 2024 on a standard 30% cut of all in-app purchases and app sales. Every app that ships as a PWA instead of a native iOS app is revenue Apple doesn't collect. The U.S. Department of Justice made this connection explicit in their March 2024 antitrust lawsuit, which specifically cites the WebKit requirement as part of Apple's monopoly maintenance strategy.

None of this is speculation. The timeline, the rejected APIs, the EU reversal, the financial model, and the DOJ case all point in the same direction. Apple's restrictions on web capabilities are a business strategy, not a technical limitation.

## The Real Cost of Defaulting to Native

Even setting Apple aside, the cost of defaulting to native or cross-platform development is higher than most teams acknowledge.

Cross-platform frameworks don't eliminate the two-codebase problem; they disguise it. You still end up dealing with platform-specific workarounds, conditional rendering logic, and bugs that only reproduce on one platform. The abstraction adds a layer of complexity on top of the platform differences rather than removing them. Abstractions like React Native's bridge architecture, Flutter's custom rendering engine, and MAUI's handler pattern each introduce their own category of bugs that don't exist in either native platform.

App Store distribution creates deployment friction that web development eliminated years ago. A critical bug fix that takes 20 minutes to deploy on the web can take days to clear App Store review. Teams build elaborate over-the-air update systems (like CodePush for React Native) specifically to work around this friction, adding complexity to solve a problem that only exists because of the distribution model.

The hiring equation favors PWAs significantly. Web developers are the largest talent pool in software engineering. Finding developers who can build a responsive web application is straightforward. Finding developers with MAUI experience, or developers who can debug platform-specific issues in React Native's bridge layer, is a much harder search.

App Store discovery is often cited as a reason to ship native, but the data complicates that argument. Less than 5% of users still use a newly installed app 30 days after installation. The average smartphone user has about 80 apps installed but uses only 11 per day. For most businesses, users aren't discovering their app through the App Store; they're arriving through a web link, a QR code, or a direct URL. PWAs serve that journey directly.

Companies that have adopted PWAs report meaningful results. Starbucks doubled daily active users on their mobile web experience with a PWA that was 99.84% smaller than their iOS app. Pinterest saw a 60% increase in core engagement after launching their PWA. Flipkart tripled time spent on site and saw 70% higher conversions from users who installed their PWA to the home screen. These aren't edge cases; these are large-scale consumer applications where PWAs outperformed native in the metrics that matter.

## Ask the Right Question

The default question in mobile development is "which cross-platform framework should we use?" It's the wrong question. The right question is "do we have a specific constraint that requires native?"

If you need home screen widgets, wearable integration, health data access, or advanced AR, the answer is yes and native development is the right call. If you need Bluetooth or NFC on iOS, Apple has made that decision for you and you'll need native until that changes. But if your app authenticates users, fetches data from an API, displays it in a list or form, sends notifications, and works offline, you're describing a PWA.

The cross-platform framework isn't solving the problem; it's adding a new one. Instead of dealing with iOS and Android differences directly, you're dealing with those differences through an abstraction layer that introduces its own bugs, its own upgrade cycles, and its own limitations. A PWA doesn't abstract away platform differences. It avoids them entirely by building on the one platform that already runs everywhere.

- Start with a PWA and prove it's insufficient before reaching for native
- If iOS push notifications are a concern, PWAs have supported them since March 2023
- If Apple's API restrictions are your only blocker, that's a business constraint, not a technical one
- If your app is a thin client over an API, you're building native infrastructure for a web-shaped problem
- Reserve native development for the narrow set of capabilities that genuinely require it

The web won the platform war two decades ago. Most of the mobile industry just hasn't noticed yet.
