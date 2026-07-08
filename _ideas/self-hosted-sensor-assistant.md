---
layout: idea
title: "Self-hosted sensor assistant"
status: idea
date: 2026-07-08
one_liner: "An open-source, self-hosted assistant that turns phone + wearable data into real-time coaching over Siri and push notifications — without the data ever leaving your control."
tags: [ios, wearables, self-hosted, privacy, ai, health]
---

## The pitch

Every fitness band, phone, and smartwatch already collects a rich stream of
signals — heart rate, HRV, sleep stages, motion, location, blood oxygen. Today
that data gets funneled into a vendor's cloud, and whatever "insights" come back
are shallow, ad-adjacent, and locked behind a subscription. I want the opposite:
a DIY assistant I run myself that ingests my own sensor streams, reasons over
them locally, and nudges me in real time — "your HRV tanked, maybe skip the hard
workout," "you've been sedentary for 3 hours," "you sleep worse the nights you
eat after 9pm" — delivered through the interfaces I already use: **Siri** and
**Apple push notifications**.

The non-negotiable is data ownership. Sensor data lands on hardware I control
(the homelab Mac Mini is the obvious host), inference runs against a local model,
and nothing about my body is shipped to a third party. It's the self-hosted,
privacy-first answer to Whoop/Oura/Fitbit coaching — an assistant that happens to
live in my house instead of theirs.

Rough shape: a HealthKit / wearable bridge that syncs readings to a local store,
a rules-plus-LLM layer that decides when something is worth surfacing, and a thin
delivery path out to Siri (App Intents / Shortcuts) and APNs for the actual
feedback. Open source so anyone can point it at their own stack.

## Open questions

- **Ingest path.** HealthKit export is easy but not real-time; getting *live*
  wearable data off-device (Apple Watch especially) is the hard part. How close
  to realtime can this actually get without a first-party watch app?
- **Siri surface.** App Intents vs. Shortcuts automations vs. a full companion
  app — what's the lightest way to make it conversational both directions?
- **The reasoning layer.** How much is deterministic rules ("HRV < baseline →
  alert") vs. an LLM summarizing trends? Where's the line where a local model
  earns its keep over a few thresholds?
- **Push without a backend.** Can APNs be driven cleanly from a self-hosted box,
  or does it need a tiny always-on relay? (Ties into the homelab setup.)
