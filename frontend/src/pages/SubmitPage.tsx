import React, { useState, type FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import type { Complaint, ComplaintCategory } from '../types/complaint';
import { api, ApiError } from '../client';

const CATEGORIES: ComplaintCategory[] = [
  'Roads & Infrastructure',
  'Water & Sanitation',
  'Electricity',
  'Waste Management',
  'Public Safety',
  'Parks & Recreation',
  'Noise Pollution',
  'Other',
];

type FormErrors = {
  title?: string;
  description?: string;
  category?: string;
  location?: string;
};

export default function SubmitPage() {
  const navigate = useNavigate();
  const [submitted, setSubmitted] = useState(false);
  const [newId, setNewId] = useState('');
  const [createdComplaint, setCreatedComplaint] = useState<Complaint | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState('');

  const [form, setForm] = useState({
    title: '',
    description: '',
    category: '' as ComplaintCategory | '',
    location: '',
  });

  const [errors, setErrors] = useState<FormErrors>({});

  function validate(): boolean {
    const e: FormErrors = {};
    if (!form.title.trim())       e.title       = 'Title is required';
    if (!form.description.trim()) {
      e.description = 'Description is required';
    } else if (form.description.trim().length < 10) {
      e.description = 'Description must be at least 10 characters';
    }
    if (!form.category)           e.category    = 'Please select a category';
    if (!form.location.trim())    e.location    = 'Location is required';
    setErrors(e);
    return Object.keys(e).length === 0;
  }

  function handleChange(
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    // clear error on change
    if (errors[name as keyof typeof form]) {
      setErrors((prev) => ({ ...prev, [name]: undefined }));
    }
  }

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();

    if (!validate()) return;

    setIsSubmitting(true);
    setSubmitError('');

    try {
      const complaint = await api.createComplaint({
        title: form.title.trim(),
        description: form.description.trim(),
        category: form.category as ComplaintCategory,
        location: form.location.trim(),
      });

      setNewId(complaint.id);
      setCreatedComplaint(complaint);
      setSubmitted(true);
    } catch (error) {
      if (error instanceof ApiError) {
        setSubmitError(
          typeof error.detail === 'string'
            ? error.detail
            : 'The server rejected the complaint.'
        );
      } else {
        setSubmitError('Unable to submit the complaint. Please try again.');
      }
    } finally {
      setIsSubmitting(false);
    }
  }

  function handleAnother() {
    setForm({ title: '', description: '', category: '', location: '' });
    setErrors({});
    setSubmitError('');
    setIsSubmitting(false);
    setCreatedComplaint(null);
    setSubmitted(false);
  }

  if (submitted) {
    return (
      <main className="page-wrapper" id="submit-success">
        <div className="container" style={{ maxWidth: 560 }}>
          <div className="toast" style={{ marginBottom: 'var(--sp-6)' }}>
            ✅ &nbsp;Complaint <strong>{newId}</strong> submitted successfully!
          </div>

          {createdComplaint && (
            <div className="card" style={{ marginBottom: 'var(--sp-6)' }}>
              <h2 style={{ marginBottom: 'var(--sp-4)', fontWeight: 700 }}>
                Triage result
              </h2>
              <p><strong>Category:</strong> {createdComplaint.category}</p>
              <p><strong>Priority:</strong> {createdComplaint.priority}</p>
              <p><strong>Summary:</strong> {createdComplaint.ai_summary}</p>
              <p><strong>Provider:</strong> {createdComplaint.triaged_by}</p>
              <p><strong>Confidence:</strong> {createdComplaint.triage_confidence.toFixed(2)}</p>
              <p><strong>Latency:</strong> {createdComplaint.triage_latency_ms} ms</p>
            </div>
          )}

          <div className="card">
            <h2 style={{ marginBottom: 'var(--sp-4)', fontWeight: 700 }}>What's next?</h2>
            <p style={{ color: 'var(--clr-text-muted)', marginBottom: 'var(--sp-5)' }}>
              Your complaint has been logged and assigned ID <strong>{newId}</strong>.
              You can track it on the dashboard.
            </p>
            <div style={{ display: 'flex', gap: 'var(--sp-3)', flexWrap: 'wrap' }}>
              <button
                id="btn-view-dashboard"
                className="btn btn--primary"
                onClick={() => navigate('/dashboard')}
              >
                View Dashboard
              </button>
              <button
                id="btn-submit-another"
                className="btn btn--ghost"
                onClick={handleAnother}
              >
                Submit Another
              </button>
            </div>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="page-wrapper" id="submit-page">
      <div className="container" style={{ maxWidth: 640 }}>
        <div className="page-hero">
          <span className="page-hero__eyebrow">Civic Engagement</span>
          <h1 className="page-hero__title">Submit a Complaint</h1>
          <p className="page-hero__subtitle">
            Report local issues and help keep your community informed.
            All complaints are reviewed by city officials.
          </p>
        </div>

        <form className="card" onSubmit={handleSubmit} noValidate id="complaint-form">
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--sp-5)' }}>
            {/* Title */}
            <div className="form-group">
              <label className="form-label" htmlFor="field-title">Title</label>
              <input
                id="field-title"
                name="title"
                className="form-input"
                type="text"
                placeholder="Brief title of the issue"
                value={form.title}
                onChange={handleChange}
                aria-invalid={!!errors.title}
                maxLength={120}
              />
              {errors.title && (
                <span style={{ color: 'var(--clr-rejected)', fontSize: 'var(--fs-xs)' }}>
                  {errors.title}
                </span>
              )}
            </div>

            {/* Category */}
            <div className="form-group">
              <label className="form-label" htmlFor="field-category">Category</label>
              <select
                id="field-category"
                name="category"
                className="form-select"
                value={form.category}
                onChange={handleChange}
                aria-invalid={!!errors.category}
              >
                <option value="">Select a category…</option>
                {CATEGORIES.map((c) => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
              {errors.category && (
                <span style={{ color: 'var(--clr-rejected)', fontSize: 'var(--fs-xs)' }}>
                  {errors.category}
                </span>
              )}
            </div>

            {/* Location */}
            <div className="form-group">
              <label className="form-label" htmlFor="field-location">Location</label>
              <input
                id="field-location"
                name="location"
                className="form-input"
                type="text"
                placeholder="e.g. Sector 7, Street 12 or Main Street near Mall"
                value={form.location}
                onChange={handleChange}
                aria-invalid={!!errors.location}
              />
              {errors.location && (
                <span style={{ color: 'var(--clr-rejected)', fontSize: 'var(--fs-xs)' }}>
                  {errors.location}
                </span>
              )}
            </div>

            {/* Description */}
            <div className="form-group">
              <label className="form-label" htmlFor="field-description">Description</label>
              <textarea
                id="field-description"
                name="description"
                className="form-textarea"
                placeholder="Describe the issue in detail — what, where, how long, what impact…"
                value={form.description}
                onChange={handleChange}
                aria-invalid={!!errors.description}
                rows={5}
              />
              {errors.description && (
                <span style={{ color: 'var(--clr-rejected)', fontSize: 'var(--fs-xs)' }}>
                  {errors.description}
                </span>
              )}
            </div>

            {submitError && (
              <div
                role="alert"
                style={{ color: 'var(--clr-rejected)', fontSize: 'var(--fs-sm)' }}
              >
                {submitError}
              </div>
            )}

            <button
              id="btn-submit"
              type="submit"
              className="btn btn--primary btn--full"
              disabled={isSubmitting}
            >
              {isSubmitting ? 'Submitting...' : '🚀  Submit Complaint'}
            </button>
          </div>
        </form>
      </div>
    </main>
  );
}
