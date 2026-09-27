import { Component, type ErrorInfo, type ReactNode } from 'react';

type Props = { children: ReactNode };
type State = { hasError: boolean };

export default class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };

  static getDerivedStateFromError(): State {
    return { hasError: true };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error('Application render error', error, info.componentStack);
  }

  render() {
    if (this.state.hasError) {
      return (
        <main className="page-wrapper" role="alert">
          <div className="container">
            <div className="empty-state">
              <div className="empty-state__title">Something went wrong</div>
              <p>Please refresh the page and try again.</p>
            </div>
          </div>
        </main>
      );
    }

    return this.props.children;
  }
}
