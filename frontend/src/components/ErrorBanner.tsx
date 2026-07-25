export function ErrorBanner({ message }: { message: string }) {
  return <div className="error-text" role="alert">Error: {message}</div>;
}
