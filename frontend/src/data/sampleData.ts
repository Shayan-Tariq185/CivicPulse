import type { Complaint } from '../types/complaint';

export const sampleComplaints: Complaint[] = [
  {
    id: 'CMP-001',
    title: 'Pothole on Main Street near Mall',
    description:
      'Large pothole causing vehicle damage. Has been there for over a month with no repair.',
    category: 'Roads & Infrastructure',
    status: 'open',
    submitted_at: '2026-09-20T08:30:00Z',
    location: 'Main Street, Block 4',
    upvotes: 42,
  },
  {
    id: 'CMP-002',
    title: 'Water pipe burst in Sector 7',
    description:
      'Underground pipe burst flooding the street. Water is being wasted for 3 days.',
    category: 'Water & Sanitation',
    status: 'in_progress',
    submitted_at: '2026-09-22T14:10:00Z',
    location: 'Sector 7, Street 12',
    upvotes: 87,
  },
  {
    id: 'CMP-003',
    title: 'Street lights out on Canal Road',
    description: 'Five consecutive street lights are non-functional, making the road dangerous at night.',
    category: 'Electricity',
    status: 'resolved',
    submitted_at: '2026-09-15T19:00:00Z',
    location: 'Canal Road, near Bridge',
    upvotes: 31,
  },
  {
    id: 'CMP-004',
    title: 'Garbage not collected for 2 weeks',
    description:
      'Garbage collection has been completely absent in our area for two weeks. Serious health risk.',
    category: 'Waste Management',
    status: 'open',
    submitted_at: '2026-09-24T09:45:00Z',
    location: 'DHA Phase 3, Street 8',
    upvotes: 115,
  },
  {
    id: 'CMP-005',
    title: 'Stray dogs attacking pedestrians',
    description:
      'Pack of stray dogs near the park have bitten two people. Immediate action required.',
    category: 'Public Safety',
    status: 'in_progress',
    submitted_at: '2026-09-23T07:15:00Z',
    location: 'Jinnah Park Entrance',
    upvotes: 64,
  },
  {
    id: 'CMP-006',
    title: 'Park swings broken — children at risk',
    description: 'All three swings in the children\'s play area have broken chains.',
    category: 'Parks & Recreation',
    status: 'rejected',
    submitted_at: '2026-09-10T11:00:00Z',
    location: 'Model Town Park',
    upvotes: 18,
  },
];

export const sampleStats = {
  total: sampleComplaints.length,
  open: sampleComplaints.filter((c) => c.status === 'open').length,
  in_progress: sampleComplaints.filter((c) => c.status === 'in_progress').length,
  resolved: sampleComplaints.filter((c) => c.status === 'resolved').length,
  rejected: sampleComplaints.filter((c) => c.status === 'rejected').length,
  byCategory: Object.entries(
    sampleComplaints.reduce<Record<string, number>>((acc, c) => {
      acc[c.category] = (acc[c.category] ?? 0) + 1;
      return acc;
    }, {})
  ).map(([category, count]) => ({ category, count })),
};
