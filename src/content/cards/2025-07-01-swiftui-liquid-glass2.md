---
id: 15
title: Liquid Glass2
description: Glass Design View
category: SwiftUI
type: other
image: /images/SwiftUI/gradient-glass.gif
---

```swift
import SwiftUI

struct LiquidGlass: View {
    
    @State private var showSheet = false
    
    var body: some View {
        ZStack {
            LinearGradient(
                colors: [Color.black, Color.purple],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()
            
            RoundedRectangle(cornerRadius: 20, style: .continuous)
                .fill(.ultraThinMaterial)
                .opacity(0.25) // 여기서 투명도 조절
                .overlay(
                    RoundedRectangle(cornerRadius: 20, style: .continuous)
                        .stroke(Color.white.opacity(0.15), lineWidth: 1)
                )
                .frame(width: 200, height: 200)
            
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
        .navigationBarBackButtonHidden(true) // ← 뒤로가기 버튼 숨기기
        .navigationBarHidden(true)
        .toolbar(.hidden, for: .tabBar)
        // 시트 내용
        .sheet(isPresented: $showSheet) {
            SheetCustomtView()
                .clearModalBackground() 
        }
    }
}

struct SheetCustomtView: View {
    var body: some View {
        VStack(spacing: 20) {
            Text("Hello, this is a transparent sheet!")
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
    LiquidGlass()
}
```

## 설명

이 예제는 SwiftUI에서 **그라디언트 배경**, **유리 느낌의 반투명 박스**, **투명 시트**, **플로팅 버튼**을 함께 사용하는 커스텀 뷰를 보여줍니다.

1. `LiquidGlass` 뷰는 화면 전체에 검정색과 보라색의 `LinearGradient`를 배경으로 사용합니다.
2. 중앙에 `RoundedRectangle`을 배치해 반투명하고 흐림(blur) 처리된 유리 느낌의 박스를 만듭니다.
3. 화면 오른쪽 아래에는 파란색 플로팅 버튼을 배치하여 시트를 띄우는 동작을 구현합니다.
4. 버튼을 누르면 `SheetCustomtView`가 시트(sheet)로 표시되며, 시트의 배경도 반투명과 블러 효과로 커스터마이징됩니다.
5. `.navigationBarHidden(true)` 및 `.toolbar(.hidden, for: .tabBar)`를 사용해 상단 내비게이션 바와 하단 탭바를 숨깁니다.

---

## 주요 특징

- **그라디언트 배경**  
  `LinearGradient`로 화면 배경에 색상 그라디언트를 적용합니다.

- **유리 효과 박스**  
  `ultraThinMaterial`과 `opacity`, `stroke`를 조합해 유리 느낌의 반투명 박스를 중앙에 표시합니다.

- **플로팅 액션 버튼**  
  화면 오른쪽 아래에 원형 파란 버튼을 배치하여 사용자 인터랙션을 제공합니다.

- **투명 및 흐림 효과 시트**  
  `clearModalBackground()` 커스텀 modifier를 적용해 시트의 배경을 투명하게 처리하고 유리 느낌을 연출합니다.

- **상단/하단 바 숨김 처리**  
  `.navigationBarHidden(true)`와 `.toolbar(.hidden, for: .tabBar)`로 내비게이션 바와 탭바를 모두 감춥니다.

- **iOS 버전 호환성**  
  iOS 16.4 이상에서는 `.presentationBackground(.clear)`를 사용하며, 그 이하 버전에서는 `UIViewRepresentable`을 통해 시트 배경을 투명하게 만듭니다.
