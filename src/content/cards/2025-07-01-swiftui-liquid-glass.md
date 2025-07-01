---
id: 7
title: Liquid Glass
description: Glass Design View
category: SwiftUI
type: other
image: /images/SwiftUI/mapkit-glass.gif
---

```swift
import SwiftUI
import MapKit

struct MapkitLiquidGlass: View {
    @State private var showSheet = false
    var body: some View {
        ZStack {
            Map()
            
            VStack {
                Spacer()
                
                HStack {
                    Spacer()
                    
                    Button {
                        showSheet.toggle()
                    } label: {
                        Circle()
                            .fill(.blue)
                            .frame(width: 50, height: 50)
                            .shadow(radius: 4)
                    }
                    .padding(.trailing, 40)
                    .padding(.bottom, 20)
                }
            }
        }
        .sheet(isPresented: $showSheet) {
            SheetCustomView()
                .clearModalBackground()
        }
        .preferredColorScheme(.dark)
    }
}

struct SheetCustomView: View {
    var body: some View {
        VStack(spacing: 20) {
            Text("Hello, this is a Custom sheet!")
                .font(.title)
                .foregroundColor(.white)

            Spacer()
        }
        .padding()
        .presentationDetents([.medium])
        .frame(maxWidth: .infinity)
        .background(
            RoundedRectangle(cornerRadius: 20, style: .continuous)
                .fill(Color.black.opacity(0.2)) // 살짝 어두운 레이어
                .blur(radius: 10)                // 흐림 정도
                .ignoresSafeArea()
        )
        .overlay(
            RoundedRectangle(cornerRadius: 10, style: .continuous)
                .stroke(Color.white.opacity(0.5), lineWidth: 1)
                .shadow(color: Color.black.opacity(0.4), radius: 4, x: 0, y: 2)
                .ignoresSafeArea()
        )
    }
}

/// iOS 16.3 이하에서 sheet 배경을 투명하게 만드는 뷰
struct ClearBackgroundView: UIViewRepresentable {
    func makeUIView(context: Context) -> some UIView {
        let view = UIView()
        DispatchQueue.main.async {
            // 부모뷰(superview) 접근해서 배경 투명하게
            view.superview?.superview?.backgroundColor = .clear
        }
        return view
    }
    
    func updateUIView(_ uiView: UIViewType, context: Context) { }
}

/// sheet에 편하게 쓰기 위한 Modifier
struct ClearBackgroundViewModifier: ViewModifier {
    func body(content: Content) -> some View {
        if #available(iOS 16.4, *) {
            content
                .presentationBackground(.clear)
        } else {
            content
                .background(ClearBackgroundView())
        }
    }
}

/// View Extension
extension View {
    func clearModalBackground() -> some View {
        self.modifier(ClearBackgroundViewModifier())
    }
}

#Preview {
    MapkitLiquidGlass()
}
```

## 설명

이 예제는 SwiftUI에서 **지도(Map)**와 **투명 배경 시트**, **플로팅 버튼**, **다크 모드**를 함께 사용하는 커스텀 뷰를 보여줍니다.

1. `MapkitLiquidGlass` 뷰는 `Map()`을 기본 배경으로 표시하며, 화면 오른쪽 아래에 파란색 플로팅 버튼을 배치합니다.
2. 버튼을 누르면 `SheetCustomView`가 시트(sheet)로 올라오며, 시트의 배경은 반투명하고 블러 처리된 유리 느낌으로 커스터마이징됩니다.
3. `.preferredColorScheme(.dark)`를 사용하여 이 뷰는 항상 다크 모드로 렌더링됩니다.

## 주요 특징

- **다크 모드 강제 적용**  
  `.preferredColorScheme(.dark)`를 사용해 이 뷰 계층만 다크 모드로 표시됩니다.

- **지도 뷰 통합**  
  SwiftUI의 `Map()` 컴포넌트를 사용하여 간단히 지도를 표시합니다.

- **플로팅 액션 버튼**  
  오른쪽 아래에 원형 파란 버튼을 배치해 사용자 인터랙션을 제공합니다.

- **투명 및 흐림 효과 시트**  
  `clearModalBackground()` 커스텀 modifier를 적용해 시트의 배경을 투명하게 처리하고, 유리 느낌을 연출합니다.

- **iOS 버전 호환성**  
  iOS 16.4 이상에서는 `.presentationBackground(.clear)`를 사용하며, 그 이하 버전에서는 `UIViewRepresentable`을 통해 시트 배경을 투명하게 만듭니다.
