'use client';

export default function MessageBubble({ message }) {
  const { role, text, status, citation, lastUpdated, educationalLink, timestamp } = message;
  const isUser = role === 'user';
  const isRefused = status === 'refused';

  if (isUser) {
    return (
      <div className="flex flex-col items-end message-fade-in">
        <div className="max-w-[80%] md:max-w-lg p-4 rounded-3xl rounded-tr-sm bg-gradient-to-br from-primary-container to-primary text-on-primary shadow-2xl shadow-primary/20 ring-1 ring-white/20 backdrop-blur-md">
          <p className="text-body-md font-medium">{text}</p>
        </div>
        {timestamp && (
          <span className="text-label-sm text-on-surface-variant mt-2 px-1">{timestamp}</span>
        )}
      </div>
    );
  }

  // Bot message (normal or refusal)
  if (isRefused) {
    return (
      <div className="flex flex-col items-start message-fade-in">
        <div className="flex gap-3 max-w-[90%] md:max-w-2xl">
          {/* Refusal icon */}
          <div className="w-8 h-8 rounded-lg bg-red-900/50 flex items-center justify-center flex-shrink-0 border border-red-500/30">
            <span className="material-symbols-outlined text-error text-[18px]">gavel</span>
          </div>
          {/* Refusal bubble */}
          <div className="p-5 rounded-3xl rounded-tl-sm bg-[#2d1b1b]/90 backdrop-blur-xl border border-red-500/40 shadow-2xl shadow-black/60">
            <p className="text-body-md text-red-100">{text}</p>
            {educationalLink && (
              <a
                href={educationalLink}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-3 inline-flex items-center gap-2 text-primary text-label-md font-bold hover:gap-3 transition-all"
              >
                Learn more about mutual funds
                <span className="material-symbols-outlined text-[18px]">arrow_forward</span>
              </a>
            )}
          </div>
        </div>
      </div>
    );
  }

  // Normal bot message
  return (
    <div className="flex flex-col items-start message-fade-in">
      <div className="flex gap-3 max-w-[90%] md:max-w-2xl">
        {/* Bot avatar */}
        <div className="w-8 h-8 rounded-lg bg-surface-variant flex items-center justify-center flex-shrink-0 border border-white/10">
          <span className="material-symbols-outlined text-primary text-[18px]">smart_toy</span>
        </div>
        {/* Bot bubble */}
        <div className="space-y-3">
          <div className="p-5 rounded-3xl rounded-tl-sm glass-panel shadow-2xl shadow-black/60 border border-white/10">
            <p className="text-body-md leading-relaxed">{text}</p>

            {/* Citation + Last Updated footer */}
            {(citation || lastUpdated) && (
              <div className="mt-4 pt-4 border-t border-white/5 flex flex-wrap gap-4 items-center">
                {citation && citation.source_url && (
                  <a
                    className="flex items-center gap-1.5 text-label-sm text-primary hover:underline"
                    href={citation.source_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    id="citation-link"
                  >
                    <span className="material-symbols-outlined text-[14px]">link</span>
                    📎 Source: [{citation.scheme_name || 'groww.in'}]
                  </a>
                )}
                {lastUpdated && (
                  <span className="text-label-sm text-on-surface-variant flex items-center gap-1.5">
                    <span className="material-symbols-outlined text-[14px]">calendar_today</span>
                    📅 Last updated: {lastUpdated}
                  </span>
                )}
              </div>
            )}

            {/* Render interactive options if provided */}
            {message.options && message.options.length > 0 && (
              <div className="mt-4 flex flex-wrap gap-2">
                {message.options.map((opt, idx) => {
                  const label = typeof opt === 'string' ? opt : opt.label;
                  const query = typeof opt === 'string' ? opt : opt.query;
                  return (
                    <button
                      key={idx}
                      onClick={() => message.onOptionClick && message.onOptionClick(query)}
                      className="text-label-md px-4 py-2 rounded-full border border-primary/40 text-primary hover:bg-primary/10 hover:border-primary transition-all active:scale-95 shadow-sm"
                    >
                      {label}
                    </button>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
