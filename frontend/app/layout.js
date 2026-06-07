import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'HDFC Mutual Fund FAQ Assistant',
  description: 'A facts-only FAQ assistant for 19 HDFC mutual fund schemes. Get factual information about NAV, expense ratio, exit load, SIP amounts, and more.',
  keywords: 'HDFC, mutual fund, FAQ, NAV, expense ratio, exit load, SIP',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="dark">
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className={`${inter.className} bg-surface-container-lowest h-screen flex overflow-hidden`}>
        {children}
      </body>
    </html>
  );
}
