import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: 'var(--background)',
        foreground: 'var(--foreground)',
        accent: {
          DEFAULT: '#1F3A5F',
          light: '#2E568A',
          dark: '#142740',
        },
        paper: {
          light: '#FFFFFF',
          dark: '#121212',
        },
        ink: {
          light: '#111111',
          dark: '#EAEAEA',
        },
        border: 'var(--border-color)',
        muted: 'var(--muted-color)',
      },
      fontFamily: {
        serif: ['var(--font-serif)', 'Source Serif 4', 'Georgia', 'serif'],
        sans: ['var(--font-sans)', 'Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
      },
      maxWidth: {
        content: '960px',
      },
      transitionDuration: {
        '150': '150ms',
      }
    },
  },
  plugins: [],
}
export default config
