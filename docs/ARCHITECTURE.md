# Architecture

Builder's Engineering Hub separates the public course shell from private learner records.

```text
Private GitHub source
        │
        │ pull requests, tests and release checks
        ▼
Committed static application
        │
        │ Cloudflare Pages delivery
        ▼
Learner's browser
        │
        └── local progress, notes, evidence and preferences
```

## Delivery

The production application is a static React and Vite single-page application. Cloudflare Pages serves a reviewed, committed build rather than running an application server or installing production dependencies during deployment.

Hash-based routes keep lessons deep-linkable without requiring a server routing layer. A service worker makes the reviewed application shell available offline after its first successful load and presents an explicit update path when a new version is ready.

## Learner state

Progress, journals, evidence, project URLs and display preferences remain in the learner's browser. State is schema-versioned and validated on load. Backups can be exported, imported and merged deliberately; they are not transmitted to an application database.

## Practice environments

Browser practice runs in isolated client-side environments. Python assets are self-hosted and prepared lazily. Web practice runs inside a sandboxed frame. These rehearsals supplement—not replace—the learner's real terminal, editor and Git workflow.

## Deliberate exclusions

- No account or login system.
- No application backend or shared learner database.
- No analytics or telemetry SDK.
- No runtime CDN dependency.
- No automatic transfer of learning data between devices.

The hosting provider necessarily processes ordinary delivery and reliability metadata needed to serve static files. That is separate from product analytics and from the learner's locally stored course record.
