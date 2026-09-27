import { BrowserRouter } from 'react-router-dom';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import SubmitPage from './SubmitPage';

const complaintResponse = {
  id: 'CMP-TEST',
  title: 'Urgent water pipe leak',
  description: 'An urgent water pipe leak is flooding the road near the market.',
  category: 'Water & Sanitation',
  status: 'open',
  location: 'Sector 7, Main Road',
  upvotes: 0,
  submitted_at: '2026-09-28T10:00:00Z',
  priority: 'high',
  ai_summary: 'Urgent water leak reported near the market.',
  triaged_by: 'llm:groq',
  triage_latency_ms: 120,
  triage_confidence: 0.94,
};

function renderPage() {
  return render(
    <BrowserRouter>
      <SubmitPage />
    </BrowserRouter>
  );
}

async function fillForm() {
  const user = userEvent.setup();
  await user.type(screen.getByLabelText('Title'), 'Urgent water pipe leak');
  await user.selectOptions(screen.getByLabelText('Category'), 'Water & Sanitation');
  await user.type(screen.getByLabelText('Location'), 'Sector 7, Main Road');
  await user.type(
    screen.getByLabelText('Description'),
    'An urgent water pipe leak is flooding the road near the market.'
  );
  return user;
}

describe('SubmitPage', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('shows validation errors for an empty form', async () => {
    const user = userEvent.setup();
    renderPage();
    await user.click(screen.getByRole('button', { name: /submit complaint/i }));
    expect(screen.getByText('Title is required')).toBeInTheDocument();
    expect(screen.getByText('Description is required')).toBeInTheDocument();
  });

  it('shows loading while the request is pending', async () => {
    vi.stubGlobal('fetch', vi.fn(() => new Promise(() => undefined)));
    renderPage();
    const user = await fillForm();
    await user.click(screen.getByRole('button', { name: /submit complaint/i }));
    expect(screen.getByRole('button', { name: 'Submitting...' })).toBeDisabled();
  });

  it('renders the real triage result after a successful response', async () => {
    vi.stubGlobal('fetch', vi.fn(() => Promise.resolve(
      new Response(JSON.stringify(complaintResponse), { status: 201 })
    )));
    renderPage();
    const user = await fillForm();
    await user.click(screen.getByRole('button', { name: /submit complaint/i }));
    expect(await screen.findByText('Triage result')).toBeInTheDocument();
    expect(screen.getByText('llm:groq')).toBeInTheDocument();
    expect(screen.getByText(/Latency:.*120 ms/)).toBeInTheDocument();
  });

  it('shows the server error detail when submission fails', async () => {
    vi.stubGlobal('fetch', vi.fn(() => Promise.resolve(
      new Response(JSON.stringify({ detail: 'Description is invalid' }), { status: 422 })
    )));
    renderPage();
    const user = await fillForm();
    await user.click(screen.getByRole('button', { name: /submit complaint/i }));
    expect(await screen.findByText('Description is invalid')).toBeInTheDocument();
  });

  it('does not submit invalid short descriptions', async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal('fetch', fetchMock);
    renderPage();
    const user = userEvent.setup();
    await user.type(screen.getByLabelText('Title'), 'Short test');
    await user.selectOptions(screen.getByLabelText('Category'), 'Other');
    await user.type(screen.getByLabelText('Location'), 'Town');
    await user.type(screen.getByLabelText('Description'), 'short');
    await user.click(screen.getByRole('button', { name: /submit complaint/i }));
    expect(fetchMock).not.toHaveBeenCalled();
  });
});
