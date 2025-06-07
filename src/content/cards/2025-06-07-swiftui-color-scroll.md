---
id: 7
title: ColorScrollView
description: 커스텀 스크롤 뷰
category: SwiftUI
type: other
image: /images/SwiftUI/color-scroll.gif
---

```swift
import SwiftUI

struct HomeView: View {
    var body: some View {
        HomeUIView()
    }
}

private struct HomeUIView: View {
    fileprivate var body: some View {
        DoubleSidedBackgroundScrollView(topColor: .black, bottomColor: .white) {
            VStack {
                
            }
        }
    }
}

#Preview {
    HomeView()
}
```

## 설명

이 예제는 SwiftUI에서 상단과 하단에 각각 다른 배경색을 가지는 커스텀 스크롤 뷰 컴포넌트인 `DoubleSidedBackgroundScrollView`를 사용하는 방법을 보여줍니다:

1. `DoubleSidedBackgroundScrollView(topColor:bottomColor:content:)` 초기화 시 상단(`topColor`)과 하단(`bottomColor`) 배경색을 지정합니다.  
2. 클로저 내부에 원하는 뷰(`VStack` 등)를 넣어 슬라이딩 가능한 콘텐츠를 구성합니다.  
3. 스크롤을 움직이면 지정한 두 가지 색상이 자연스럽게 전환됩니다.  

## 주요 특징

- **양쪽 배경 색상 설정**: 상단과 하단에 서로 다른 배경색 지정  
- **커스텀 콘텐츠 삽입**: 내부 클로저에 원하는 SwiftUI 뷰를 자유롭게 배치 가능  
- **매끄러운 색상 전환**: 스크롤 위치에 따라 두 색상이 자연스럽게 블렌딩  
- **순수 SwiftUI 구현**: `UIViewRepresentable` 없이 오직 SwiftUI만으로 구성  
