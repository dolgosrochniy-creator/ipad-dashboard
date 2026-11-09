-- Выполнить в Supabase SQL Editor ОДИН РАЗ.
-- Частный bucket; доступ к объектам только авторизованным пользователям.
-- ВАЖНО: пока разрешено ЛЮБОМУ вошедшему в проект пользователю.
-- Перед реальным использованием ограничить доступ по auth.uid() для конкретных пользователей.
create policy "Authenticated users can upload frame photos"
on storage.objects for insert to authenticated
with check (bucket_id = 'frame-photos');
create policy "Authenticated users can view frame photos"
on storage.objects for select to authenticated
using (bucket_id = 'frame-photos');
