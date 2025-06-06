---
id: 1
title: html 버튼
description: 기본적인 버튼
category: web
type: web
---

```html
<div class="button-container">
    <button class="btn btn-primary">기본 버튼</button>
    <button class="btn btn-primary hover-effect">호버 효과</button>
</div>
```

```css
.button-container {
    display: flex;
    gap: 10px;
}

.btn {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.btn-primary {
    background-color:rgb(49, 62, 240);
    color: white;
}

.hover-effect:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
``` 