export type Note = {
  id: number;
  user_id: string;
  title: string | null;
  content: string;
  summary?: string | null;
  source: string;
  category: string;
  mood?: string | null;
  importance: number;
  is_archived: boolean;
  created_at: string;
  updated_at: string;
  tags: string[];
};
