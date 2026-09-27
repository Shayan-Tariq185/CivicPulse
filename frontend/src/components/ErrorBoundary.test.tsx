import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

import ErrorBoundary from './ErrorBoundary';

function BrokenComponent() {
  throw new Error('render failed');
}

describe('ErrorBoundary', () => {
  it('shows a recovery message when a child throws', () => {
    render(
      <ErrorBoundary>
        <BrokenComponent />
      </ErrorBoundary>
    );
    expect(screen.getByRole('alert')).toHaveTextContent('Something went wrong');
  });
});
