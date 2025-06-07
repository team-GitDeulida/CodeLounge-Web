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

struct DoubleSidedBackgroundScrollView<Content: View>: View {

    private let ContentBuilder: () -> Content
    private let topColor: Color         // 배경의 상단 색상
    private let bottomColor: Color      // 배경의 하단 색상
    
    @State private var offset: CGFloat = .zero  // 스크롤 오프셋 값 저장(얼마나 위라래로 이동했는지)
    
    init(topColor: Color, bottomColor: Color, contentBuilder: @escaping () -> Content) {
        self.ContentBuilder = contentBuilder // ㅋ,ㄹ로저 형태로 전달된 스크롤 뷰의 실제 내용을 생성
        self.topColor = topColor
        self.bottomColor = bottomColor
    }

    var body: some View {
        ScrollView {
            ZStack {
                ContentBuilder()
                
                // 스크롤뷰 위치 추적
                GeometryReader { proxy in
                    // 스크롤 뷰 상단 부분이 기준 좌표에 대해 얼마나 이동했는가
                    let offset = proxy.frame(in: .named("scroll")).minY
                    // 투명한 색상을 사용하여 레이아웃에 영항을 주지 않음
                    Color.clear.preference(key: ScrollViewOffsetPreferenceKey.self, value: offset)
                }
            }
        }
        .coordinateSpace(name: "scroll")
        
        // PreferenceKey의 값이 변경될 때 offset을 업데이트
        .onPreferenceChange(ScrollViewOffsetPreferenceKey.self) { value in
            offset = value
        }
        .background(
            VStack(spacing: 0) {
                // offset 값에 따라 상단 배경의 높이를 조정
                // max를 사용하여 높이가 음수가 되지 않도록 제한
                topColor
                    .frame(
                        height: max(offset + (UIScreen.main.bounds.height / 2), 0),
                        alignment: .top)
                bottomColor
                    .clipShape(RoundedRectangle(cornerRadius: 30)) // 둥근 모서리 추가
                    .overlay(
                        RoundedRectangle(cornerRadius: 30)
                            .stroke(Color.gray, lineWidth: 2) // 테두리 추가
                    )
                    .padding(.top, -80)
            }
            .ignoresSafeArea()
        )
    }
}

// GeometryReader로 계산한 offset 값을 ScrollView에서 @State로 저장
// reduce 메서드는 현재 값과 새 값을 병합
private struct ScrollViewOffsetPreferenceKey: PreferenceKey {
    static var defaultValue: CGFloat = .zero

    static func reduce(value: inout CGFloat, nextValue: () -> CGFloat) {
        value = nextValue()
    }
}

struct SlideView: View {
    var body: some View {
        DoubleSidedBackgroundScrollView(topColor: .black, bottomColor: .white) {
            VStack {

            }
        }
        .navigationBarBackButtonHidden(true) // ← 뒤로가기 버튼 숨기기
        .toolbar(.hidden, for: .tabBar) 
    }
}

#Preview {
    SlideView()
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
