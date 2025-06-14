---
id: 12
title: Android 애니메이션 버튼
description: animateDpAsState 함수
category: android
type: animation
image: /images/android/Aos-animation.gif
---

```kotlin
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp

@Composable
fun AnimatedBoxButton() {
    var isExpanded by remember { mutableStateOf(false) }

    val boxWidth by animateDpAsState(
        targetValue = if (isExpanded) 300.dp else 100.dp,
        label = "boxWidth"
    )

    Box(
        contentAlignment = Alignment.Center,
        modifier = Modifier
            .padding(16.dp)
            .width(boxWidth)
            .height(60.dp)
            .background(Color(0xFF6200EE), RoundedCornerShape(12.dp))
            .clickable { isExpanded = !isExpanded }
    ) {
    }
}
```

## 설명

이 예제는 박스 크기를 애니메이션으로 변경하는 버튼을 구현합니다:
1. `remember`와 `mutableStateOf`로 상태를 저장  
2. `animateDpAsState`로 너비 값을 부드럽게 애니메이션 처리  
3. `clickable`로 상태 변경 → 다시 눌렀을 때 토글됨  


## 주요 특징
- 클릭 시 길이 변경 애니메이션 적용  
- animateDpAsState 사용  
- Box를 버튼처럼 활용  
