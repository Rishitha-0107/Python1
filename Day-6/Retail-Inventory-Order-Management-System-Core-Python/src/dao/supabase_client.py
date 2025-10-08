# src/dao/supabase_client.py
from supabase import create_client
SUPABASE_URL="https://odknmjvgxctsqjkprnpk.supabase.co"
SUPABASE_KEY ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9ka25tanZneGN0c3Fqa3BybnBrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgxNzA4MjQsImV4cCI6MjA3Mzc0NjgyNH0.18jIU8bL9qgIt8cWqzI4IfnmSTWPJQe2GbilZkn7eYM"


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)