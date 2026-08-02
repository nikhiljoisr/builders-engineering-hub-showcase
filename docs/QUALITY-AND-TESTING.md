# Quality and testing

The course teaches evidence-led engineering, so its release process is held to the same standard.

## Current verified release

| Verification area | Evidence |
|---|---:|
| Automated tests | 110 passing |
| Production browser scenarios | 28 passing |
| Mobile module-and-tab states | 260 checked at 375px |
| Known production dependency vulnerabilities | 0 |

Last verified: **2 August 2026**.

## What the automated suite covers

- Current and legacy learner-state migrations.
- Restore validation, repair, merge and emergency backup behaviour.
- Immediate save paths, quota failures and two-tab editing safety.
- Deep-link routing and resume behaviour.
- Quiz scoring, retrieval scheduling and evidence gates.
- Browser sandboxes and deny-by-default boundaries.
- Accessibility tokens, contrast, reading preferences and reduced motion.
- Offline assets, service-worker updates and committed-bundle reproducibility.
- Sharing redaction and tutor-prompt privacy boundaries.

## Browser acceptance

Production scenarios exercise fresh onboarding, Module 1's five tabs, keyboard focus, state migration, backup merge, lock takeover, private-safe sharing, Python success and failure, offline reload and update activation.

The 260-state mobile sweep covers all 52 modules across Overview, Learn, Practise, Build and Verify at a 375px viewport.

## Honest limits

Automated checks do not replace human use. The small friend pilot is intended to add real Windows and Edge evidence, physical PWA installation and offline reopening, and normal assistive-technology use where available. The product does not claim those environments as manually verified until that evidence exists.
