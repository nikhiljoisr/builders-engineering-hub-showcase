# Privacy boundary

Builder's Engineering Hub is local-first by design.

## What stays in the learner's browser

- Module and step progress.
- Journals, notes and highlights.
- Evidence and project URLs.
- Confidence and learning preferences.
- Backups until the learner deliberately downloads or imports them.

## What the application does not add

- An account or login.
- A shared learner database.
- Product analytics, telemetry or advertising trackers.
- Automatic cloud sync between devices.
- Automatic transmission of prompts or notes to an AI provider.

## Deliberate exits from the browser

Learning data leaves the browser only when the learner takes an explicit action, such as downloading a backup, copying a tutor prompt or exporting a redacted progress artifact. The interface distinguishes full backups from redacted sharing artifacts because a backup can contain private text.

## Public shell versus private state

The course shell is hosted at a public, unlisted address during the friend pilot. Anyone with that address may open or forward it. That does not expose another learner's progress: browser storage is isolated by origin and browser profile.

The public showcase repository contains no learner state, backups, private URLs or production application source.
