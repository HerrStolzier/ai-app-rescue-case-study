-- Demo baseline: client-owned insert.
-- Problem: the application sends a local or guessed user_id.

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

-- Broken app behavior:
-- insert into patrol_reports (user_id, report_text)
-- values ('local_user', 'North gate checked');
--
-- If auth.uid() is 'user_123', RLS rejects this row because:
-- 'user_123' != 'local_user'
