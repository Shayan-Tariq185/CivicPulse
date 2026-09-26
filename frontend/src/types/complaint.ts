export type ComplaintStatus = 'open' | 'in_progress' | 'resolved' | 'rejected';

export type ComplaintCategory =
  | 'Roads & Infrastructure'
  | 'Water & Sanitation'
  | 'Electricity'
  | 'Waste Management'
  | 'Public Safety'
  | 'Parks & Recreation'
  | 'Noise Pollution'
  | 'Other';

export interface Complaint {
  id: string;
  title: string;
  description: string;
  category: ComplaintCategory;
  status: ComplaintStatus;
  submittedAt: string; // ISO date string
  location: string;
  upvotes: number;
}
