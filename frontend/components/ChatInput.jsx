'use client';

import { useState, useRef, useCallback } from 'react';

export default function ChatInput({ onSend, disabled }) {
  const [input, setInput] = useState('');
  const textareaRef = useRef(null);

  const handleSend = useCallback(() => {
    const trimmed = input.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setInput('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.focus();
    }
  }, [input, disabled, onSend]);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleInput = (e) => {
    setInput(e.target.value);
    // Auto-grow textarea
    e.target.style.height = '';
    e.target.style.height = e.target.scrollHeight + 'px';
  };

  return (
    <footer className="absolute bottom-0 left-0 w-full p-6 md:p-8 bg-gradient-to-t from-surface-container-lowest via-surface-container-lowest to-transparent pointer-events-none">
      <div className="max-w-4xl mx-auto w-full pointer-events-auto">
        <div className="relative flex items-end gap-3 glass-panel p-2 rounded-2xl border border-white/10 focus-within:border-primary/50 transition-colors shadow-2xl">
          {/* Attach button (decorative) */}
          <button className="p-3 text-on-surface-variant hover:text-primary transition-colors flex-shrink-0">
            <span className="material-symbols-outlined">attach_file</span>
          </button>

          {/* Textarea */}
          <textarea
            ref={textareaRef}
            className="flex-1 bg-transparent border-none focus:ring-0 text-body-md py-3 text-on-surface placeholder:text-on-surface-variant/50 resize-none max-h-40"
            placeholder="Ask about HDFC fund expense ratios, AUM, or performance..."
            rows="1"
            value={input}
            onChange={handleInput}
            onKeyDown={handleKeyDown}
            disabled={disabled}
            id="chat-input"
          />

          {/* Send button */}
          <div className="flex items-center gap-2 pr-2 pb-1.5">
            <button
              className="w-12 h-12 rounded-full bg-primary text-on-primary flex items-center justify-center shadow-lg hover:scale-105 active:scale-95 transition-all group disabled:opacity-40 disabled:cursor-not-allowed"
              onClick={handleSend}
              disabled={disabled || !input.trim()}
              id="send-btn"
              aria-label="Send message"
            >
              <span className="material-symbols-outlined text-[24px] font-bold group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform">
                send
              </span>
            </button>
          </div>
        </div>

        <p className="text-center text-label-sm text-on-surface-variant mt-4 opacity-50">
          HDFC AI Assistant can make mistakes. Verify important financial data.
        </p>
      </div>
    </footer>
  );
}
