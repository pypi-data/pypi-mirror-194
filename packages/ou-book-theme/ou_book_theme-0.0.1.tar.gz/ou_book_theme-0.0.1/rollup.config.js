import scss from 'rollup-plugin-scss';
import { writeFileSync, mkdirSync } from 'fs';

export default {
	input: 'src/ou_book_theme/assets/scripts/index.js',
	output: {
		file: 'src/ou_book_theme/theme/ou_book_theme/static/scripts/ou-book-theme.js',
		format: 'esm',
        assetFileNames: '[name][extname]'
	},
    plugins: [
        scss({
            output(styles) {
                try {
                    mkdirSync('src/ou_book_theme/theme/ou_book_theme/static/styles',{ recursive: true });
                } catch {}
                writeFileSync('src/ou_book_theme/theme/ou_book_theme/static/styles/ou-book-theme.css', styles);
            }
        }),
    ]
};
