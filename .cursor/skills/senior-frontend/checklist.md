# Frontend definition of done

Copy this list and check items for the change.

## Loading / error / empty

- [ ] Library shows `saved_loading` while `useAsyncData('saved-resumes')` is pending
- [ ] Logged-out library shows `saved_empty`; logged-in with no rows shows `saved_none`
- [ ] Generate button uses `generating` + loading state; failures toast `generate_failed`
- [ ] Export failures toast `export_failed`; 401 opens `LoginModal`
- [ ] Auth errors surface in the modal (`auth_failed`), not an uncaught promise

## Accessibility

- [ ] Inputs have labels (`UFormField` / `t(...)` keys)
- [ ] `LangSwitch` keeps `role="group"` and `aria-pressed`
- [ ] Primary nav has `aria-label`; skip/focus rings still visible on the logo
- [ ] Wizard generate/export are keyboard reachable
- [ ] No new icon-only buttons without an accessible name

## Quality

- [ ] `pnpm lint` from `frontend/`
- [ ] `pnpm typecheck` from `frontend/`
- [ ] `pnpm test` from `frontend/` (schemas, auth store, wizard)
- [ ] No `any`; Zod still mirrors `backend/schemas.py` if the contract changed
- [ ] KK + RU + EN keys added together

## Browser verify

- [ ] `/` renders the four-step wizard (personal → experience → skills → preview)
- [ ] Login/register stores JWT in `resume_ai_token` and `/api/auth/me` hydrates the bar
- [ ] Generate (with backend on `:8000`) fills preview + analysis and refreshes Saved
- [ ] Open / delete a saved resume; other pages that share wizard/auth state still match
- [ ] PDF and DOCX export download when a result `id` exists
- [ ] Locale switch KK / RU / EN updates chrome and wizard copy without a full remount bug
