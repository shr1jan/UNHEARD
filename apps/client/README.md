# @unheard/client

Unheard mobile client — **React Native + TypeScript** (one codebase, iOS + Android).
A web client can later reuse the existing TanStack Start stack (`E11-4`).

## Status

Placeholder. The React Native app is scaffolded as part of **`E0-5`** (foundations),
because `npx react-native init` pulls a large native toolchain that doesn't belong
in this planning commit. To scaffold it:

```bash
# from apps/
npx @react-native-community/cli init UnheardClient --directory client --pm npm
```

Then keep this package name (`@unheard/client`) so the workspace wiring holds.

## What the client owns (Phase 1)

- The **post flow**: Open → Record → (server mask) → **Preview** → Post. (`FR-POST-01`)
  - The **preview gate** is sacred: the masked clip is played back and confirmed
    before publish. The client must not allow publish without it. (`FR-POST-03`)
- The **feed**: waveform + duration + topic + reaction counts; sorts Newest /
  Most heard / Needs love. (`FR-FEED-*`)
- **Reactions** (Heard you / Felt this / Sending strength), **Echo**, **topic follow**.
- **"My posts"** private view + **instant delete**. (`FR-ACCT-04`, `FR-POST-09`)
- **Save original to Files** opt-in, with the first-save safety warning and a
  neutral default filename. (`FR-POST-06/07`)
- Calm, anti-doomscroll UX; WCAG 2.2 AA. (`FR-FEED-08`, `NFR-UX-01`)

## Hard rule

The client NEVER persists or uploads the original recording anywhere except the
single masking request, and surfaces the masked preview before anything is public.
