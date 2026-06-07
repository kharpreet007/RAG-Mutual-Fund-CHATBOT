'use client';

export default function DisclaimerBanner() {
  return (
    <div
      className="w-full bg-amber-500/10 backdrop-blur-md border-b border-amber-500/20 px-6 py-3 flex items-start gap-3 z-40"
      id="disclaimer-banner"
    >
      <span
        className="material-symbols-outlined text-amber-500 flex-shrink-0"
        style={{ fontVariationSettings: "'FILL' 1" }}
      >
        warning
      </span>
      <p className="text-label-md text-amber-200 font-medium leading-tight">
        ⚠️ Facts-only. No investment advice. This assistant provides factual information only. It does not offer recommendations or predictions.
      </p>
    </div>
  );
}
