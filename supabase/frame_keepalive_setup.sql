-- Run once in Supabase SQL Editor for Moscow Photo Frame.
-- Isolated heartbeat table: no access to photos or user data.
create table if not exists public.frame_keepalive (
  id integer primary key check (id = 1),
  last_ping_at timestamptz not null default now()
);
alter table public.frame_keepalive enable row level security;
revoke all on public.frame_keepalive from anon, authenticated;
insert into public.frame_keepalive (id, last_ping_at)
values (1, now())
on conflict (id) do nothing;

create or replace function public.frame_keepalive_ping()
returns timestamptz
language plpgsql
security definer
set search_path = ''
as $$
declare
  ping_time timestamptz;
begin
  update public.frame_keepalive
  set last_ping_at = now()
  where id = 1
  returning last_ping_at into ping_time;
  return ping_time;
end;
$$;
revoke all on function public.frame_keepalive_ping() from public;
grant execute on function public.frame_keepalive_ping() to anon;
