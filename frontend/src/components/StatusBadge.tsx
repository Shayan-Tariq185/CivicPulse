import type { ComplaintStatus } from '../types/complaint';

const LABELS: Record<ComplaintStatus, string> = {
  open: 'Open',
  in_progress: 'In Progress',
  resolved: 'Resolved',
  rejected: 'Rejected',
};

interface Props {
  status: ComplaintStatus;
}

export default function StatusBadge({ status }: Props) {
  return (
    <span className={`badge badge--${status}`}>
      {LABELS[status]}
    </span>
  );
}
