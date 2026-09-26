import { useState } from 'react';
import { sampleComplaints } from '../data/sampleData';
import StatusBadge from '../components/StatusBadge';
import type { ComplaintStatus } from '../types/complaint';

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
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<ComplaintStatus | 'all'>('all');

  const filtered = sampleComplaints.filter((c) => {
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

        {/* Count */}
        <p style={{ marginBottom: 'var(--sp-5)', color: 'var(--clr-text-muted)', fontSize: 'var(--fs-sm)' }}>
          Showing <strong style={{ color: 'var(--clr-text)' }}>{filtered.length}</strong> complaint{filtered.length !== 1 ? 's' : ''}
        </p>

        {/* Grid */}
        {filtered.length === 0 ? (
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

                <div className="complaint-card__footer">
                  <div className="complaint-card__meta">
                    📍 {c.location}
                  </div>
                  <div className="complaint-card__meta">
                    🏷️ {c.category}
                  </div>
                  <div className="complaint-card__meta">
                    📅 {formatDate(c.submittedAt)}
                  </div>
                  <div className="complaint-card__upvotes">
                    ▲ {c.upvotes}
                  </div>
                </div>
              </article>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
