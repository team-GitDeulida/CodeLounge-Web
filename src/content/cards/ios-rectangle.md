---
id: 4
title: Rectangle
description: Rectangle 컴포넌트
category: SwiftUI
type: other
image: /images/ios-rectangle.png
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

이 예제는 iOS에서 네비게이션 바를 구현하는 기본적인 방법을 보여줍니다:

1. `title` 속성을 사용하여 네비게이션 바의 제목을 설정합니다.
2. `prefersLargeTitles`를 true로 설정하여 큰 제목 스타일을 사용합니다.
3. `UIBarButtonItem`을 사용하여 오른쪽에 추가 버튼을 배치합니다.

## 주요 특징

- 네비게이션 바의 기본 설정
- 시스템 아이콘을 사용한 버튼 추가
- 버튼 탭 이벤트 처리 