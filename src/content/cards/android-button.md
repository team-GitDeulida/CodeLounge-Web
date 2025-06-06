---
id: 3
title: Button
description: Jetpack Compose 기본버튼
category: android
type: other
image: /images/Aos-basicbutton.png
---

```kotlin
import androidx.compose.material.Button
import androidx.compose.material.Text
import androidx.compose.runtime.Composable

@Composable
fun BasicButton() {
    Button(onClick = { /* TODO: 클릭 처리 */ }) {
        Text("Button")
    }
}
``` 

## 설명

이 예제는 Jetpack Compose에서 기본 버튼을 생성하는 가장 간단한 방법을 보여줍니다:
	
1. `Button` 컴포저블을 사용하여 버튼 생성  
2. `onClick` 람다에 클릭 시 동작 정의  
3. `Text` 를 통해 버튼 내부 텍스트 설정


## 주요 특징

- 기본 버튼 생성  
- 클릭 이벤트 처리 가능  
- 내부 텍스트 지정  