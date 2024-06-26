import { marked } from 'marked';
import fs from 'fs/promises'; // Используем промисы для асинхронного чтения файлов
import path from 'path';
import { BASE_URL } from '../../../api.js';

/** @type {import('./$types').PageServerLoad} */
export async function load({ params }) {
    const themeId = params.themePage;
    const res = await fetch(`${BASE_URL}/themes/${themeId}`);

    if (res.ok) {
        const theme = await res.json();
        const filePath = path.join(process.cwd(), 'static', 'chapters', theme.content + ".md"); // Формируем правильный путь к файлу

        try {
            const data = await fs.readFile(filePath, 'utf8'); // Асинхронное чтение файла
            const htmlContent = marked(data); // Конвертируем Markdown в HTML
            
            const quizPath = path.join(process.cwd(), `/src/quizzes/Python/ch${themeId}.json`);
            const quizData = JSON.parse(await fs.readFile(quizPath, 'utf8'));

            return {
                htmlContent,
                themeTitle: theme.title,
                themeId,
                quizData
            };
        } catch (err) {
            console.log(`File not found: ${filePath}`, err);
            return {
                htmlContent: 'File not found',
                themeTitle: theme.title,
                themeId,
                quizData: null
            };
        }
    } else {
        console.log('Fetch error');
        return {
            htmlContent: 'Error fetching theme',
            themeTitle: 'Error',
            themeId,
            quizData: null
        };
    }
}
