---
title: iOS MD Button
description: iOS 스타일의 Material Design 버튼 컴포넌트입니다.
category: ios
---

```html
<button class="ios-md-button">
    <span class="button-text">Button</span>
</button>
```

```css
.ios-md-button {
    background: linear-gradient(145deg, #007AFF, #0055FF);
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    color: white;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 122, 255, 0.3);
    position: relative;
    overflow: hidden;
}

.ios-md-button::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(145deg, rgba(255,255,255,0.2), rgba(255,255,255,0));
    opacity: 0;
    transition: opacity 0.3s ease;
}

.ios-md-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 122, 255, 0.4);
}

.ios-md-button:hover::after {
    opacity: 1;
}

.ios-md-button:active {
    transform: translateY(1px);
    box-shadow: 0 2px 10px rgba(0, 122, 255, 0.3);
}

.button-text {
    position: relative;
    z-index: 1;
}
```

```javascript
// 버튼 클릭 이벤트 예시
document.querySelector('.ios-md-button').addEventListener('click', function() {
    console.log('Button clicked!');
});
``` 