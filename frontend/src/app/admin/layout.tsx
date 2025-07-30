import { Analytics } from '@vercel/analytics/react'

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      
      <main>
        {children}
        <Analytics />
      </main>
    </>
  );
}