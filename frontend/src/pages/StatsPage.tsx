import { sampleStats, sampleComplaints } from '../data/sampleData';

interface StatCardProps {
  icon: string;
  value: number;
  label: string;
  glowColor: string;
  id: string;
}

function StatCard({ icon, value, label, glowColor, id }: StatCardProps) {
  return (
    <div className="stat-card" id={id}>
      <div className="stat-card__glow" style={{ background: glowColor }} />
      <div className="stat-card__icon">{icon}</div>
      <div className="stat-card__value">{value}</div>
      <div className="stat-card__label">{label}</div>
    </div>
  );
}

export default function StatsPage() {
  const maxCount = Math.max(...sampleStats.byCategory.map((c) => c.count), 1);

  // Average upvotes
  const avgUpvotes =
    sampleComplaints.length > 0
      ? Math.round(
          sampleComplaints.reduce((s, c) => s + c.upvotes, 0) /
            sampleComplaints.length
        )
      : 0;

  // Most reported category
  const topCategory =
    sampleStats.byCategory.length > 0
      ? sampleStats.byCategory.reduce((a, b) => (a.count >= b.count ? a : b)).category
      : '—';

  return (
    <main className="page-wrapper" id="stats-page">
      <div className="container">
        {/* Hero */}
        <div className="page-hero">
          <span className="page-hero__eyebrow">Analytics</span>
          <h1 className="page-hero__title">Complaint Statistics</h1>
          <p className="page-hero__subtitle">
            A live overview of civic issues reported across the city.
          </p>
        </div>

        {/* KPI cards */}
        <div className="stats-grid" aria-label="Key metrics">
          <StatCard
            id="stat-total"
            icon="📋"
            value={sampleStats.total}
            label="Total Complaints"
            glowColor="hsl(224, 76%, 55%)"
          />
          <StatCard
            id="stat-open"
            icon="🔵"
            value={sampleStats.open}
            label="Open"
            glowColor="hsl(200, 80%, 55%)"
          />
          <StatCard
            id="stat-in-progress"
            icon="🟡"
            value={sampleStats.in_progress}
            label="In Progress"
            glowColor="hsl(38, 90%, 55%)"
          />
          <StatCard
            id="stat-resolved"
            icon="🟢"
            value={sampleStats.resolved}
            label="Resolved"
            glowColor="hsl(156, 70%, 45%)"
          />
          <StatCard
            id="stat-rejected"
            icon="🔴"
            value={sampleStats.rejected}
            label="Rejected"
            glowColor="hsl(0, 68%, 55%)"
          />
          <StatCard
            id="stat-avg-upvotes"
            icon="▲"
            value={avgUpvotes}
            label="Avg. Upvotes"
            glowColor="hsl(156, 72%, 47%)"
          />
        </div>

        {/* Two-column section */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
            gap: 'var(--sp-6)',
          }}
        >
          {/* By Category */}
          <div className="card" id="stats-by-category">
            <h2 style={{ fontWeight: 700, marginBottom: 'var(--sp-5)' }}>
              Complaints by Category
            </h2>
            <div className="bar-list">
              {sampleStats.byCategory
                .sort((a, b) => b.count - a.count)
                .map(({ category, count }) => (
                  <div key={category}>
                    <div className="bar-item__header">
                      <span>{category}</span>
                      <span style={{ color: 'var(--clr-text-muted)' }}>{count}</span>
                    </div>
                    <div className="bar-item__track">
                      <div
                        className="bar-item__fill"
                        style={{ width: `${(count / maxCount) * 100}%` }}
                        role="progressbar"
                        aria-valuenow={count}
                        aria-valuemax={maxCount}
                        aria-label={`${category}: ${count} complaints`}
                      />
                    </div>
                  </div>
                ))}
            </div>
          </div>

          {/* Highlights */}
          <div className="card" id="stats-highlights">
            <h2 style={{ fontWeight: 700, marginBottom: 'var(--sp-5)' }}>
              Highlights
            </h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--sp-4)' }}>
              {[
                {
                  icon: '🏆',
                  label: 'Most Reported Category',
                  value: topCategory,
                },
                {
                  icon: '📊',
                  label: 'Resolution Rate',
                  value:
                    sampleStats.total > 0
                      ? `${Math.round((sampleStats.resolved / sampleStats.total) * 100)}%`
                      : '—',
                },
                {
                  icon: '⏳',
                  label: 'Pending (Open + In Progress)',
                  value: sampleStats.open + sampleStats.in_progress,
                },
                {
                  icon: '❌',
                  label: 'Rejection Rate',
                  value:
                    sampleStats.total > 0
                      ? `${Math.round((sampleStats.rejected / sampleStats.total) * 100)}%`
                      : '—',
                },
              ].map(({ icon, label, value }) => (
                <div
                  key={label}
                  style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    padding: 'var(--sp-3) 0',
                    borderBottom: '1px solid var(--clr-border)',
                  }}
                >
                  <span style={{ color: 'var(--clr-text-muted)', fontSize: 'var(--fs-sm)' }}>
                    {icon}&nbsp; {label}
                  </span>
                  <strong style={{ fontSize: 'var(--fs-base)' }}>{value}</strong>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
