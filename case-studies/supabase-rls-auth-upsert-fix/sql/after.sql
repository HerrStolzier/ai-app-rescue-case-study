-- Demo fix: server/session-owned insert.
-- The client no longer decides ownership.

create table patrol_reports (
  id uuid primary key default gen_random_uuid(),
  user_id text not null,
  report_text text not null,
  created_at timestamptz not null default now()
);

alter table patrol_reports enable row level security;

create policy "users can insert their own reports"
on patrol_reports
for insert
with check (auth.uid()::text = user_id);

create policy "users can read their own reports"
on patrol_reports
for select
using (auth.uid()::text = user_id);

-- Fixed app behavior:
-- insert into patrol_reports (user_id, report_text)
-- values (auth.uid()::text, 'North gate checked');
--
-- The row owner is derived from the authenticated session.
