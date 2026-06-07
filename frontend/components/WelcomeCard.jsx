'use client';

const EXAMPLE_QUESTIONS = [
  'What is the expense ratio of HDFC Mid-Cap Fund?',
  'Compare HDFC Top 100 vs HDFC Flexi Cap exit loads.',
  "Show HDFC Liquid Fund's asset allocation.",
];

export default function WelcomeCard({ onExampleClick }) {
  return (
    <div className="max-w-2xl mx-auto flex flex-col items-center text-center space-y-6 pt-12 pb-12" id="welcome-card">
      {/* Wave Icon */}
      <div className="w-20 h-20 rounded-full bg-primary-container/20 flex items-center justify-center text-4xl shadow-lg border border-primary/20">
        👋
      </div>

      {/* Heading */}
      <div>
        <h2 className="text-headline-lg text-on-surface">Welcome!</h2>
        <p className="text-body-md text-on-surface-variant mt-2 max-w-md">
          I can answer factual questions about 19 HDFC mutual fund schemes. Try one of these to get started:
        </p>
      </div>

      {/* Example Buttons */}
      <div className="w-full max-w-sm space-y-3">
        {EXAMPLE_QUESTIONS.map((question, index) => (
          <button
            key={index}
            className="w-full p-4 rounded-xl glass-panel text-left text-label-md hover:bg-surface-variant/40 transition-all flex justify-between items-center group"
            id={`example-btn-${index}`}
            onClick={() => onExampleClick(question)}
          >
            {question}
            <span className="material-symbols-outlined text-primary opacity-0 group-hover:opacity-100 transition-opacity">
              arrow_forward
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}
