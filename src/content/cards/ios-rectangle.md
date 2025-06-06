---
id: 4
title: Rectangle
description: Rectangle 컴포넌트
category: SwiftUI
type: other
image: /images/SwiftUI/ios-rectangle.png
---

```swift
import SwiftUI

struct ContentView: View {
    var body: some View {
        VStack(alignment: .center) {
            Rectangle()
                .frame(width: 200, height: 200)
                .cornerRadius(20)
                .foregroundStyle(.black.opacity(0.8))
        }
    }
}

#Preview {
    ContentView()
}

```

## 설명

이 예제는 SwiftUI에서 Rectangle을 사용하여 사각형을 그리는 기본적인 방법을 보여줍니다:

1. `Rectangle()`을 사용하여 기본 사각형을 생성합니다.
2. `frame` 수정자를 사용하여 사각형의 크기를 지정합니다.
3. `cornerRadius`를 사용하여 모서리를 둥글게 만듭니다.
4. `foregroundStyle`을 사용하여 색상과 투명도를 설정합니다.

## 주요 특징

- 기본 사각형 생성
- 크기 조절
- 모서리 둥글게 만들기
- 색상 및 투명도 설정 