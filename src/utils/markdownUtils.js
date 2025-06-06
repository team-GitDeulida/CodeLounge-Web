const fs = require('fs').promises;
const path = require('path');
const matter = require('gray-matter');
const { marked } = require('marked');

// 마크다운 파일의 메타데이터와 컨텐츠를 파싱하는 함수
async function parseMarkdownFile(filePath) {
    try {
        const fileContent = await fs.readFile(filePath, 'utf-8');
        const { data, content } = matter(fileContent);
        
        // 코드 블록 추출
        const codeBlocks = content.split('```').filter((block, index) => index % 2 === 1);
        
        // 설명 부분 추출 (코드 블록 이후의 텍스트)
        const descriptionText = content.split('```').filter((block, index) => index % 2 === 0)
            .slice(1) // 첫 번째 블록(코드 블록 이전) 제외
            .join('')
            .trim();
        
        // 마크다운을 HTML로 변환
        const descriptionHtml = marked(descriptionText);
        
        // 웹 컴포넌트인 경우 HTML과 CSS 분리
        if (data.type === 'web') {
            const html = codeBlocks[0]?.replace(/^html\n/, '') || '';
            const css = codeBlocks[1]?.replace(/^css\n/, '') || '';
            
            return {
                ...data,
                html,
                css,
                descriptionText,
                descriptionHtml,
                get fullCode() {
                    return `${this.html}\n\n<style>\n${this.css}\n</style>`;
                },
                get previewHtml() {
                    return `<!DOCTYPE html>
<html>
<head>
    <style>${this.css}</style>
    <style>body { margin: 0; padding: 10px; }</style>
</head>
<body>
    ${this.html}
</body>
</html>`;
                }
            };
        }
        
        // 다른 타입의 컴포넌트인 경우
        return {
            ...data,
            code: codeBlocks[0]?.replace(/^[a-z]+\n/, '') || '',
            descriptionText,
            descriptionHtml,
            get fullCode() {
                return this.code;
            }
        };
    } catch (error) {
        console.error(`Error parsing markdown file ${filePath}:`, error);
        throw error;
    }
}

// 카드 목록을 가져오는 함수
async function getCards() {
    const cardsDir = path.join(__dirname, '../content/cards');
    try {
        const files = await fs.readdir(cardsDir);
        const cards = await Promise.all(
            files
                .filter(file => file.endsWith('.md'))
                .map(async file => {
                    const filePath = path.join(cardsDir, file);
                    return await parseMarkdownFile(filePath);
                })
        );
        return cards;
    } catch (error) {
        console.error('Error getting cards:', error);
        throw error;
    }
}

// 특정 카드의 상세 내용을 가져오는 함수
async function getCardDetail(cardId) {
    const cardsDir = path.join(__dirname, '../content/cards');
    try {
        console.log('Searching for card with ID:', cardId);
        const files = await fs.readdir(cardsDir);
        console.log('Found files:', files);

        for (const file of files) {
            if (!file.endsWith('.md')) continue;
            
            const filePath = path.join(cardsDir, file);
            console.log('Checking file:', file);
            
            const content = await fs.readFile(filePath, 'utf-8');
            const { data } = matter(content);
            console.log('File metadata:', data);
            
            if (data.id === parseInt(cardId)) {
                console.log('Found matching file:', file);
                return await parseMarkdownFile(filePath);
            }
        }

        console.log('No matching file found for ID:', cardId);
        return null;
    } catch (error) {
        console.error(`Error getting card detail for ${cardId}:`, error);
        console.error('Error stack:', error.stack);
        throw error;
    }
}

// 새로운 카드 생성 함수
async function createCard(cardId, metadata, content) {
    const cardPath = path.join(__dirname, '../content/cards', `${cardId}.md`);
    const cardContent = matter.stringify(content, metadata);
    await fs.writeFile(cardPath, cardContent);
}

// 새로운 상세 내용 생성 함수
async function createCardDetail(cardId, metadata, content) {
    const detailPath = path.join(__dirname, '../content/details', `${cardId}.md`);
    const detailContent = matter.stringify(content, metadata);
    await fs.writeFile(detailPath, detailContent);
}

module.exports = {
    parseMarkdownFile,
    getCards,
    getCardDetail,
    createCard,
    createCardDetail
}; 