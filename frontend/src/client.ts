import type {
  Complaint,
  ComplaintCreate,
  ComplaintStats,
  StatusUpdate,
} from './types/complaint';

const BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000/api/v1";

export class ApiError extends Error {
  public status: number;
  public detail: unknown;

  constructor(status: number, detail: unknown) {
    super(`API error ${status}`);
    this.name = 'ApiError';
    this.status = status;
    this.detail = detail;
  }
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => null);
    throw new ApiError(res.status, body?.detail ?? body);
  }
  return res.json();
}

export const api = {
  createComplaint: (data: ComplaintCreate) =>
    request<Complaint>('/complaints', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  getComplaint: (id: string) =>
    request<Complaint>(`/complaints/${id}`),

  listComplaints: () =>
    request<Complaint[]>('/complaints'),

  updateStatus: (id: string, status: StatusUpdate['status']) =>
    request<Complaint>(`/complaints/${id}/status`, {
      method: 'PATCH',
      body: JSON.stringify({ status }),
    }),

  getStats: () =>
    request<ComplaintStats>('/stats'),
};