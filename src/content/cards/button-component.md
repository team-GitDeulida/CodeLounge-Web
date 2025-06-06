---
id: 1
title: html 버튼
description: 기본적인 버튼 스타일과 애니메이션
category: web
type: web
---

```html
<button class="btn btn-primary">기본 버튼</button>
<button class="btn btn-primary hover-effect">호버 효과</button>
```

```css
.btn {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.btn-primary {
    background-color: #007bff;
    color: white;
}

.hover-effect:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
``` 