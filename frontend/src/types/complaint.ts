export type ComplaintStatus =
  | 'open'
  | 'in_progress'
  | 'resolved'
  | 'rejected';

export type ComplaintCategory =
  | 'Roads & Infrastructure'
  | 'Water & Sanitation'
  | 'Electricity'
  | 'Waste Management'
  | 'Public Safety'
  | 'Parks & Recreation'
  | 'Noise Pollution'
  | 'Other';

export interface ComplaintCreate {
  title: string;
  description: string;
  category: ComplaintCategory;
  location: string;
}

export interface StatusUpdate {
  status: ComplaintStatus;
}

export interface Complaint {
  id: string;
  title: string;
  description: string;
  category: ComplaintCategory;
  status: ComplaintStatus;
  location: string;
  upvotes: number;
  submitted_at: string;
}

export interface CategoryStat {
  category: string;
  count: number;
}

export interface ComplaintStats {
  total: number;
  open: number;
  in_progress: number;
  resolved: number;
  rejected: number;
  byCategory: CategoryStat[];
}