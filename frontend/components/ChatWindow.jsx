'use client';

import { useRef, useEffect } from 'react';
import MessageBubble from './MessageBubble';
import WelcomeCard from './WelcomeCard';

export default function ChatWindow({ messages, isLoading, showWelcome, onExampleClick }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isLoading]);

  return (
    <section
      className="flex-1 overflow-y-auto custom-scrollbar px-6 md:px-margin-desktop py-stack-lg space-y-stack-lg pb-40"
      id="chat-window"
    >
      {/* Welcome Card */}
      {showWelcome && <WelcomeCard onExampleClick={onExampleClick} />}

      {/* Chat Messages */}
      {messages.map((msg, index) => (
        <MessageBubble key={index} message={msg} />
      ))}

      {/* Loading State */}
      {isLoading && (
        <div className="flex items-center gap-3 message-fade-in">
          <div className="w-8 h-8 rounded-lg bg-surface-variant flex items-center justify-center flex-shrink-0 border border-white/10">
            <span className="material-symbols-outlined text-primary text-[18px]">smart_toy</span>
          </div>
          <div className="bg-surface-variant/30 px-4 py-3 rounded-full flex gap-1.5 items-center border border-white/5">
            <div className="typing-dot"></div>
            <div className="typing-dot"></div>
            <div className="typing-dot"></div>
          </div>
        </div>
      )}

      <div ref={bottomRef} />
    </section>
  );
}
