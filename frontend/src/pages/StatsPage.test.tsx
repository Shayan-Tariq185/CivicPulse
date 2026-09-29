import { BrowserRouter } from 'react-router-dom';
import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';

import StatsPage from './StatsPage';


describe('StatsPage', () => {
  it('renders live statistics from the API', async () => {
    vi.stubGlobal('fetch', vi.fn(() => Promise.resolve(new Response(JSON.stringify({
      total: 4,
      open: 1,
      in_progress: 1,
      resolved: 2,
      rejected: 0,
      byCategory: [{ category: 'Water & Sanitation', count: 4 }],
    }), { status: 200, headers: { 'X-Cache': 'HIT' } }))));

    render(<BrowserRouter><StatsPage /></BrowserRouter>);
    expect((await screen.findAllByText('Water & Sanitation')).length).toBeGreaterThan(0);
    expect(screen.getAllByText('4').length).toBeGreaterThan(0);
  });
});
