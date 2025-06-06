// Socket.IO 연결
const socket = io();

// 컴포넌트 데이터를 저장할 배열
let components = [];
let currentCategory = 'all';

// 다크모드 관련 함수들
function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    
    const themeToggle = document.getElementById('themeToggle');
    const icon = themeToggle.querySelector('i');
    
    if (theme === 'dark') {
        icon.classList.remove('fa-moon');
        icon.classList.add('fa-sun');
    } else {
        icon.classList.remove('fa-sun');
        icon.classList.add('fa-moon');
    }
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
}

// 저장된 테마 불러오기
const savedTheme = localStorage.getItem('theme') || 'dark';
setTheme(savedTheme);

// 다크모드 토글 버튼 이벤트 리스너
document.getElementById('themeToggle').addEventListener('click', toggleTheme);

// 검색 기능
function searchComponents(query) {
    if (!query) return components;
    query = query.toLowerCase();
    
    // 현재 선택된 카테고리의 컴포넌트만 필터링
    let filteredComponents = components;
    if (currentCategory !== 'all') {
        filteredComponents = components.filter(component => component.category === currentCategory);
    }
    
    // 검색어로 필터링
    return filteredComponents.filter(component => {
        return (
            component.title.toLowerCase().includes(query) ||
            component.description.toLowerCase().includes(query) ||
            component.category.toLowerCase().includes(query)
        );
    });
}

// 검색어 입력 시 실시간으로 결과 표시
document.getElementById('searchInput').addEventListener('input', (e) => {
    const query = e.target.value.trim();
    const filteredComponents = searchComponents(query);
    renderComponents(currentCategory, filteredComponents);
});

// 검색 버튼 클릭 이벤트 리스너
document.getElementById('searchButton').addEventListener('click', () => {
    const query = document.getElementById('searchInput').value.trim();
    const filteredComponents = searchComponents(query);
    renderComponents(currentCategory, filteredComponents);
});

// 엔터 키 이벤트 리스너
document.getElementById('searchInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const query = e.target.value.trim();
        const filteredComponents = searchComponents(query);
        renderComponents(currentCategory, filteredComponents);
    }
});

// 마크다운 파일 로드 함수
async function loadMarkdownFiles() {
    try {
        const response = await fetch('/api/components');
        const data = await response.json();
        components = data;
        renderComponents();
    } catch (error) {
        console.error('컴포넌트 로드 중 오류 발생:', error);
    }
}

// 컴포넌트 카드 생성 함수
function createComponentCard(component) {
    if (component.type === 'web') {
        return `
            <div class="col-md-3 mb-4">
                <div class="card component-card" data-component-id="${component.id}" data-category="${component.category}">
                    <div class="component-preview">
                        <div class="preview-content">
                            <style>${component.css}</style>
                            <div class="component-buttons">${component.html}</div>
                        </div>
                    </div>
                    <div class="card-body">
                        <h5 class="card-title component-title">${component.title}</h5>
                        <p class="card-text component-description">${component.description}</p>
                    </div>
                </div>
            </div>
        `;
    } else {
        return `
            <div class="col-md-3 mb-4">
                <div class="card component-card" data-component-id="${component.id}" data-category="${component.category}">
                    <div class="component-preview">
                        <img src="${component.image}" alt="${component.title} 미리보기" class="preview-image">
                    </div>
                    <div class="card-body">
                        <h5 class="card-title component-title">${component.title}</h5>
                        <p class="card-text component-description">${component.description}</p>
                    </div>
                </div>
            </div>
        `;
    }
}

// 컴포넌트 목록 렌더링
function renderComponents(category = 'all', filteredComponents = null) {
    const componentList = document.getElementById('component-list');
    currentCategory = category; // 현재 카테고리 저장
    
    let componentsToRender = filteredComponents || components;
    
    if (category !== 'all') {
        componentsToRender = componentsToRender.filter(component => component.category === category);
    }
    
    componentList.innerHTML = componentsToRender.map(createComponentCard).join('');
}

// 카테고리 버튼 이벤트 처리
document.querySelectorAll('[data-category]').forEach(button => {
    button.addEventListener('click', (e) => {
        // 활성화된 버튼 스타일 변경
        document.querySelectorAll('[data-category]').forEach(btn => {
            btn.classList.remove('active');
        });
        e.target.classList.add('active');

        // 선택된 카테고리의 컴포넌트만 표시
        const category = e.target.dataset.category;
        renderComponents(category);
    });
});

// 컴포넌트 클릭 이벤트 처리
document.addEventListener('click', (e) => {
    const card = e.target.closest('.component-card');
    if (card) {
        const componentId = card.dataset.componentId;
        window.location.href = `/component/${componentId}`;
    }
});

// 페이지 로드 시 마크다운 파일 로드
document.addEventListener('DOMContentLoaded', loadMarkdownFiles); 