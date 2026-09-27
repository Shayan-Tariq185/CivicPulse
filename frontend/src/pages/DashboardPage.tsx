import { useEffect, useState } from 'react';
import { api, ApiError } from '../client';
import StatusBadge from '../components/StatusBadge';
import type { Complaint, ComplaintStatus } from '../types/complaint';

const STATUS_OPTIONS: Array<ComplaintStatus | 'all'> = [
  'all', 'open', 'in_progress', 'resolved', 'rejected',
];

const STATUS_LABELS: Record<ComplaintStatus | 'all', string> = {
  all: 'All',
  open: 'Open',
  in_progress: 'In Progress',
  resolved: 'Resolved',
  rejected: 'Rejected',
};

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString('en-PK', {
    year: 'numeric', month: 'short', day: 'numeric',
  });
}

export default function DashboardPage() {
  const [complaints, setComplaints] = useState<Complaint[]>([]);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<ComplaintStatus | 'all'>('all');
  const [isLoading, setIsLoading] = useState(true);
  const [loadingError, setLoadingError] = useState('');
  const [statusError, setStatusError] = useState('');
  const [updatingId, setUpdatingId] = useState<string | null>(null);

  useEffect(() => {
    async function loadComplaints() {
      setIsLoading(true);
      setLoadingError('');

      try {
        setComplaints(await api.listComplaints());
      } catch (error) {
        setLoadingError(
          error instanceof ApiError && typeof error.detail === 'string'
            ? error.detail
            : 'Unable to load complaints. Please try again.'
        );
      } finally {
        setIsLoading(false);
      }
    }

    void loadComplaints();
  }, []);

  async function handleStatusChange(id: string, status: ComplaintStatus) {
    setUpdatingId(id);
    setStatusError('');

    try {
      const updatedComplaint = await api.updateStatus(id, status);
      setComplaints((current) =>
        current.map((complaint) =>
          complaint.id === id ? updatedComplaint : complaint
        )
      );
    } catch (error) {
      setStatusError(
        error instanceof ApiError && typeof error.detail === 'string'
          ? error.detail
          : 'Unable to update the complaint status.'
      );
    } finally {
      setUpdatingId(null);
    }
  }

  const filtered = complaints.filter((c) => {
    const matchesStatus = statusFilter === 'all' || c.status === statusFilter;
    const q = search.toLowerCase();
    const matchesSearch =
      !q ||
      c.title.toLowerCase().includes(q) ||
      c.category.toLowerCase().includes(q) ||
      c.location.toLowerCase().includes(q);
    return matchesStatus && matchesSearch;
  });

  return (
    <main className="page-wrapper" id="dashboard-page">
      <div className="container">
        {/* Hero */}
        <div className="page-hero">
          <span className="page-hero__eyebrow">Community Issues</span>
          <h1 className="page-hero__title">Complaints Dashboard</h1>
          <p className="page-hero__subtitle">
            Browse and track all submitted complaints in your city.
          </p>
        </div>

        {/* Filter bar */}
        <div className="filter-bar" role="search" aria-label="Filter complaints">
          {/* Search */}
          <div className="filter-bar__search form-group" style={{ margin: 0 }}>
            <input
              id="dashboard-search"
              className="form-input"
              type="search"
              placeholder="Search by title, category, or location…"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              aria-label="Search complaints"
            />
          </div>

          {/* Status filter */}
          <div style={{ display: 'flex', gap: 'var(--sp-2)', flexWrap: 'wrap' }} role="group" aria-label="Status filter">
            {STATUS_OPTIONS.map((s) => (
              <button
                key={s}
                id={`filter-${s}`}
                className={`btn btn--ghost`}
                onClick={() => setStatusFilter(s)}
                style={
                  statusFilter === s
                    ? { borderColor: 'var(--clr-primary)', color: 'var(--clr-primary-light)' }
                    : {}
                }
                aria-pressed={statusFilter === s}
              >
                {STATUS_LABELS[s]}
              </button>
            ))}
          </div>
        </div>

        {loadingError && (
          <div className="empty-state" role="alert">
            <div className="empty-state__title">Unable to load complaints</div>
            <p>{loadingError}</p>
          </div>
        )}

        {statusError && (
          <div className="toast" role="alert" style={{ marginBottom: 'var(--sp-5)' }}>
            {statusError}
          </div>
        )}

        {/* Count */}
        <p style={{ marginBottom: 'var(--sp-5)', color: 'var(--clr-text-muted)', fontSize: 'var(--fs-sm)' }}>
          {isLoading ? 'Loading complaints...' : (
            <>Showing <strong style={{ color: 'var(--clr-text)' }}>{filtered.length}</strong> complaint{filtered.length !== 1 ? 's' : ''}</>
          )}
        </p>

        {/* Grid */}
        {!isLoading && filtered.length === 0 ? (
          <div className="empty-state" id="dashboard-empty">
            <div className="empty-state__icon">🔍</div>
            <div className="empty-state__title">No complaints found</div>
            <p>Try adjusting your search or filter.</p>
          </div>
        ) : (
          <div className="complaint-grid" id="complaint-list">
            {filtered.map((c) => (
              <article key={c.id} className="complaint-card" aria-label={c.title}>
                <div className="complaint-card__header">
                  <span className="complaint-card__id">{c.id}</span>
                  <StatusBadge status={c.status} />
                </div>

                <h2 className="complaint-card__title">{c.title}</h2>
                <p className="complaint-card__description">{c.description}</p>
                <p className="complaint-card__description">
                  <strong>AI summary:</strong> {c.ai_summary}
                </p>

                <div className="complaint-card__footer">
                  <div className="complaint-card__meta">
                    📍 {c.location}
                  </div>
                  <div className="complaint-card__meta">
                    🏷️ {c.category}
                  </div>
                  <div className="complaint-card__meta">
                    ⚑ {c.priority}
                  </div>
                  <div className="complaint-card__meta">
                    🤖 {c.triaged_by}
                  </div>
                  <div className="complaint-card__meta">
                    📅 {formatDate(c.submitted_at)}
                  </div>
                  <div className="complaint-card__upvotes">
                    ▲ {c.upvotes}
                  </div>
                </div>

                <label className="form-label" htmlFor={`status-${c.id}`}>
                  Update status
                </label>
                <select
                  id={`status-${c.id}`}
                  className="form-select"
                  value={c.status}
                  disabled={updatingId === c.id}
                  onChange={(event) =>
                    void handleStatusChange(
                      c.id,
                      event.target.value as ComplaintStatus
                    )
                  }
                >
                  {STATUS_OPTIONS.filter((status) => status !== 'all').map((status) => (
                    <option key={status} value={status}>
                      {STATUS_LABELS[status]}
                    </option>
                  ))}
                </select>
              </article>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
