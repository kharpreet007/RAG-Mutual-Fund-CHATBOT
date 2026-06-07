'use client';

export default function Sidebar({ onNewChat, onFundSelect }) {
  return (
    <aside className="hidden lg:flex flex-col fixed left-0 top-0 h-screen py-stack-lg bg-surface-container-lowest/95 backdrop-blur-2xl border-r border-white/5 shadow-2xl w-72 z-40">
      {/* Brand */}
      <div className="px-6 mb-8">
        <h1 className="text-headline-md text-primary font-bold">HDFC Assistant</h1>
        <p className="text-on-surface-variant text-label-sm mt-1">Premium AI Access</p>
      </div>

      {/* Navigation & Schemes List */}
      <nav className="flex-1 flex flex-col px-4 min-h-0">
        <button
          onClick={onNewChat}
          className="w-full text-left px-4 py-3 mb-6 rounded-xl bg-primary text-on-primary font-bold flex items-center gap-3 transition-all hover:opacity-90 active:scale-95 flex-shrink-0"
          id="new-chat-btn"
        >
          <span className="material-symbols-outlined">add</span>
          Start New Chat
        </button>

        <div className="pb-2 px-4 text-label-sm text-on-surface-variant uppercase tracking-wider font-bold flex-shrink-0">
          Supported Schemes (19)
        </div>

        {/* Scrollable list of funds */}
        <div className="flex-1 overflow-y-auto custom-scrollbar space-y-1 pr-2">
          {[
            "HDFC Balanced Advantage Fund",
            "HDFC BSE Sensex Index Fund",
            "HDFC Defence Fund",
            "HDFC Equity Fund",
            "HDFC Focused Fund",
            "HDFC Gold ETF Fund of Fund",
            "HDFC Infrastructure Fund",
            "HDFC Large and Mid Cap Fund",
            "HDFC Liquid Fund",
            "HDFC Mid-Cap Fund",
            "HDFC Multi Cap Fund",
            "HDFC Nifty 50 Index Fund",
            "HDFC Nifty Next 50 Index Fund",
            "HDFC Nifty Top 20 Equal Weight Index Fund",
            "HDFC Pharma and Healthcare Fund",
            "HDFC Short Term Opportunities Fund",
            "HDFC Silver ETF FOF",
            "HDFC Small Cap Fund",
            "HDFC Ultra Short Term Fund"
          ].map((fund, i) => (
            <button
              key={i}
              onClick={() => onFundSelect(fund)}
              className="w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-on-surface-variant hover:bg-surface-variant/30 text-label-md transition-all text-left"
              title={fund}
            >
              <span className="material-symbols-outlined text-[18px] opacity-70">account_balance</span>
              <span className="truncate">{fund}</span>
            </button>
          ))}
        </div>
      </nav>
    </aside>
  );
}
