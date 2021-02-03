const mode = process.env.NODE_ENV || 'development';
const prod = mode === 'production';

module.exports = {
  future: { // for tailwind 2.0 compat
    purgeLayersByDefault: true,
    removeDeprecatedGapUtilities: true,
  },
  plugins: [
    // for tailwind UI users only
    // require('@tailwindcss/ui'),
    // other plugins here
  ],
    theme: {
      extend: {
        boxShadow: {
                link: '0 -4px 0 0 rgba(178, 245, 234, .7) inset',
                linkhover: '0 -6px 0 0 rgba(178, 245, 234, .7) inset',
                wikilink: '0 -4px 0 0 rgba(255, 208, 255, .9) inset',
                wikihover: '0 -12px 0 0 rgba(255, 208, 0, .6) inset',
            },
      }
    },
  purge: {
    content: [
      "./assets/**/*.svelte",
        "./pftl/templates/**/*.html"
    ],
    enabled: prod // disable purge in dev
  },
};