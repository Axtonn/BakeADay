export default function Footer() {
  return (
    <footer className="text-center py-4 bg-pink-50 text-pink-800 text-sm mt-12">
      © {new Date().getFullYear()} ABakeADay. Made with <span className="text-pink-500">♥</span> in Sydney.
    </footer>
  );
}
