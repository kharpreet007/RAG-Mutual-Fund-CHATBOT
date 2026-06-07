'use client';

import { useState, useCallback } from 'react';
import Sidebar from '../components/Sidebar';
import DisclaimerBanner from '../components/DisclaimerBanner';
import ChatWindow from '../components/ChatWindow';
import ChatInput from '../components/ChatInput';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function Home() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showWelcome, setShowWelcome] = useState(true);

  const sendMessage = useCallback(async (query) => {
    if (!query.trim()) return;

    setShowWelcome(false);

    // Get current time for timestamp
    const now = new Date();
    const timestamp = now.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true });

    const userMessage = { role: 'user', text: query, timestamp };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await fetch(`${API_URL}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      });

      const data = await response.json();

      const botMessage = {
        role: 'bot',
        text: data.answer || 'Sorry, something went wrong.',
        status: data.status,
        citation: data.citation || null,
        lastUpdated: data.last_updated || null,
        educationalLink: data.educational_link || null,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error('API error:', error);
      const errorMessage = {
        role: 'bot',
        text: 'Unable to connect to the server. Please make sure the backend is running at localhost:8000.',
        status: 'error',
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const handleExampleClick = useCallback((question) => {
    sendMessage(question);
  }, [sendMessage]);

  const handleNewChat = useCallback(() => {
    setMessages([]);
    setShowWelcome(true);
  }, []);

  const handleFundSelect = useCallback((fundName) => {
    setShowWelcome(false);
    
    // Add bot message with shortcut options
    const botMessage = {
      role: 'bot',
      text: `What would you like to know about **${fundName}**?`,
      options: [
        { label: 'NAV', query: `What is the NAV of ${fundName}?` },
        { label: 'Expense Ratio', query: `What is the expense ratio of ${fundName}?` },
        { label: 'Exit Load', query: `What is the exit load for ${fundName}?` },
        { label: 'Fund Manager', query: `Who is the fund manager of ${fundName}?` }
      ],
      onOptionClick: sendMessage
    };

    setMessages((prev) => [...prev, botMessage]);
  }, [sendMessage]);

  return (
    <>
      {/* Sidebar (Desktop only) */}
      <Sidebar onNewChat={handleNewChat} onFundSelect={handleFundSelect} />

      {/* Main Content Canvas */}
      <main className="flex-1 flex flex-col h-screen lg:ml-72 relative">
        {/* Top App Bar */}
        <header className="flex justify-between items-center w-full px-6 md:px-margin-desktop h-16 sticky top-0 z-50 bg-surface-dim/80 backdrop-blur-xl border-b border-white/10 shadow-sm" id="app-header">
          <div className="flex items-center gap-4">
            {/* Mobile menu button */}
            <button className="lg:hidden text-primary p-2">
              <span className="material-symbols-outlined">menu</span>
            </button>
            <span className="text-headline-md font-bold bg-clip-text text-transparent bg-gradient-to-r from-on-surface to-primary">
              🏦 HDFC Mutual Fund FAQ Assistant
            </span>
          </div>
          <div className="flex items-center gap-4">
            <button className="text-on-surface-variant hover:text-primary transition-colors">
              <span className="material-symbols-outlined">help</span>
            </button>
            <button className="text-on-surface-variant hover:text-primary transition-colors">
              <span className="material-symbols-outlined">account_circle</span>
            </button>
          </div>
        </header>

        {/* Disclaimer Banner */}
        <DisclaimerBanner />

        {/* Chat Container */}
        <ChatWindow
          messages={messages}
          isLoading={isLoading}
          showWelcome={showWelcome}
          onExampleClick={handleExampleClick}
        />

        {/* Fixed Input Area */}
        <ChatInput onSend={sendMessage} disabled={isLoading} />
      </main>
    </>
  );
}
