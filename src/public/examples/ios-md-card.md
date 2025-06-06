---
title: iOS MD Card
description: iOS 스타일의 Material Design 카드 컴포넌트입니다.
category: ios
---

```html
<div class="ios-md-card">
    <div class="card-image">
        <img src="https://picsum.photos/400/200" alt="Card image">
    </div>
    <div class="card-content">
        <h3 class="card-title">Card Title</h3>
        <p class="card-description">This is a beautiful iOS style card with Material Design elements.</p>
        <button class="card-button">Learn More</button>
    </div>
</div>
```

```css
.ios-md-card {
    background: var(--card-bg);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    max-width: 400px;
    margin: 20px auto;
}

.ios-md-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
}

.card-image {
    width: 100%;
    height: 200px;
    overflow: hidden;
}

.card-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.ios-md-card:hover .card-image img {
    transform: scale(1.05);
}

.card-content {
    padding: 20px;
}

.card-title {
    color: var(--text-color);
    font-size: 1.5rem;
    margin: 0 0 10px 0;
    font-weight: 600;
}

.card-description {
    color: var(--text-secondary);
    font-size: 1rem;
    line-height: 1.5;
    margin-bottom: 20px;
}

.card-button {
    background: linear-gradient(145deg, #007AFF, #0055FF);
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    color: white;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}

.card-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0, 122, 255, 0.3);
}

.card-button:active {
    transform: translateY(1px);
}
```

```javascript
// 카드 버튼 클릭 이벤트 예시
document.querySelector('.card-button').addEventListener('click', function() {
    console.log('Card button clicked!');
});
``` 