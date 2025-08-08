---
id: 15
title: LoginView
description: Onboarding + LoginVIew
category: SwiftUI
type: other
image: /images/SwiftUI/onboardingLoginView.gif
---

```swift
import SwiftUI

// MARK: - Intro Model
struct Intro: Identifiable {
    let id: UUID = UUID()
    var text: String
    var textColor: Color
    var circleColor: Color
    var bgColor: Color
    var circleOffset: CGFloat = 0
    var textOffset: CGFloat = 0
}

// MARK: - Sample Intros
var sampleIntros: [Intro] = [
    .init(text: "잠시 멈춰도 괜찮아요.", textColor: .black, circleColor: .black, bgColor: .white),
    .init(text: "당신의 하루에", textColor: .black, circleColor: .black, bgColor: .white),
    .init(text: "작은 쉼표가 되어줄게요.", textColor: .black, circleColor: .black, bgColor: .white),
    .init(text: "지금, 함께 시작해요.", textColor: .black, circleColor: .black, bgColor: .white)
]

// MARK: - View
struct LoginView: View {
    
    @State private var intros: [Intro] = sampleIntros
    @State private var activeIntro: Intro?
    var body: some View {
        GeometryReader {
            let size = $0.size
            let safeAreaInsets = $0.safeAreaInsets
            
            VStack(spacing: 0) {
                if let activeIntro {
                    Rectangle()
                        .fill(activeIntro.bgColor)
                        .padding(.bottom, -30)
                        /// Circle and Text
                        .overlay {
                            Image("Comma")
                                .resizable()
                                .scaledToFit()
                            
//                            Circle()
//                                .fill(activeIntro.circleColor)
                                .frame(width: 45, height: 45)
                                .background(alignment: .leading, content: {
                                    Capsule()
                                        .fill(activeIntro.bgColor)
                                        .frame(width: size.width)
                                })
                                .background(alignment: .leading) {
                                    Text(activeIntro.text)
                                        .font(.largeTitle)
                                        .foregroundStyle(activeIntro.textColor)
                                        .frame(width: textSize(text: activeIntro.text))
                                        .offset(x: 10)
                                        /// Moving Text based on text Offset
                                        .offset(x: activeIntro.textOffset)
                                }
                                /// Moving Circle in the Opposite Direction
                                .offset(x: -activeIntro.circleOffset)
                            }
                    /// Login Buttons
                    logunButtons()
                        .padding(.bottom, safeAreaInsets.bottom)
                        .padding(.top, 10)
                        .background(.black, in: .rect(topLeadingRadius: 25, topTrailingRadius: 25))
                        .shadow(color: .black.opacity(0.1), radius: 5, x: 0, y: 8)
                }
            }
            .ignoresSafeArea()
        }
        .task {
            if activeIntro == nil {
                activeIntro = sampleIntros.first
                /// Delaying 0.15s and Starting Animation
                let oneSecond = UInt64(1_000_000_000 * 0.5)
                try? await Task.sleep(nanoseconds: oneSecond * UInt64(0.15))
                animate(0)
            }
        }
        .preferredColorScheme(.dark)
    }
    
    /// Login Buttons
    @ViewBuilder
    func logunButtons() -> some View {
        VStack(spacing: 12) {
            Button {
                
            } label: {
                Label("애플로 계속하기", image: "Logo Apple")
                    .foregroundStyle(.black)
                    .fillButton(.white)
            }
            
            Button {
                
            } label: {
                HStack {
                    Image("Logo Google")
                        .resizable()
                        .scaledToFit()
                        .frame(width: 20, height: 20) // 원하는 크기로 조절
                    Text("구글로 계속하기")
                        .foregroundStyle(.white)
                        .fontWeight(.bold)
                }
                .fillButton(.gray5)
            }
            
            Button {
                
            } label: {
                HStack {
                    /*
                    Image("Logo Google")
                        .resizable()
                        .scaledToFit()
                        .frame(width: 20, height: 20) // 원하는 크기로 조절
                     */
                    Text("Login")
                        .foregroundStyle(.white)
                        .fontWeight(.bold)
                }
                .fillButton(.black)
                .shadow(color: .white, radius: 1)
            }

            Spacer()
                .frame(height: 3)
            
            VStack(spacing: 4) {
                Text("본 서비스 로그인 및 이용 시,")
                (
                    Text("이용약관")
                        .underline()
                        .foregroundStyle(.white)
                    +
                    Text(" 및 ")
                        .foregroundStyle(.white)
                    +
                    Text("개인정보처리방침")
                        .underline()
                        .foregroundStyle(.white)
                    +
                    Text("에 동의하신 것으로 간주됩니다.")
                        .foregroundStyle(.white)
                )
            }
            .multilineTextAlignment(.center)
            .font(.footnote)
            .frame(maxWidth: .infinity)
        }
        .padding(15)
    }
    
    func animate(_ index: Int, _ loop: Bool = true) {
        // ✅ index가 유효한 범위일 때 실행
        guard index < intros.count else {
            if loop {
                animate(0, loop)
            }
            return
        }

        // ✅ 현재 Intro 설정
        activeIntro = intros[index]

        withAnimation(.snappy(duration: 1), completionCriteria: .removed) {
            activeIntro?.textOffset = -(textSize(text: intros[index].text) + 20)
            activeIntro?.circleOffset = -(textSize(text: intros[index].text) + 20) / 2
        } completion: {
            withAnimation(.snappy(duration: 0.8), completionCriteria: .logicallyComplete) {
                activeIntro?.textOffset = 0
                activeIntro?.circleOffset = 0
                activeIntro?.circleColor = intros[index].circleColor
                activeIntro?.bgColor = intros[index].bgColor
            } completion: {
                animate(index + 1, loop)
            }
        }
    }

    
    func animate2(_ index: Int, _ loop: Bool = true) {
        if intros.indices.contains(index + 1) {
            /// updating text and text color
            activeIntro?.text = intros[index].text
            activeIntro?.textColor = intros[index].textColor
            
            /// Animating Offsets
            withAnimation(.snappy(duration: 1), completionCriteria: .removed) {
                activeIntro?.textOffset = -(textSize(text: intros[index].text) + 20)
                activeIntro?.circleOffset = -(textSize(text: intros[index].text) + 20) / 2
            } completion: {
                withAnimation(.snappy(duration: 0.8), completionCriteria: .logicallyComplete) {
                    activeIntro?.textOffset = 0
                    activeIntro?.circleOffset = 0
                    activeIntro?.circleColor = intros[index + 1].circleColor
                    activeIntro?.bgColor = intros[index + 1].bgColor
                } completion: {
                    /// Going to Next Slide
                    /// Simply Recursion
                    animate(index + 1, loop)
                }
            }
        } else {
            /// looping
            /// If looping Applied, Then Reset the Index to 0
            if loop {
                animate(0, loop)
            }
        }
    }
    
    /// Fetching Text Size based on Fonts
    func textSize(text: String) -> CGFloat {
        return NSString(string: text).size(withAttributes: [.font: UIFont.preferredFont(forTextStyle: .largeTitle)]).width
    }
}

#Preview {
    LoginView()
}


extension View {
    @ViewBuilder
    func fillButton(_ color: Color) -> some View {
        self
            .fontWeight(.bold)
            .frame(maxWidth: .infinity)
            .padding(.vertical, 15)
            .background(color, in: .rect(cornerRadius: 15))
    }
}
```

## 설명

이 예제는 SwiftUI로 제작된 **온보딩 애니메이션과 로그인 뷰(LoginView)**입니다.  
`Intro` 모델 배열을 순차적으로 애니메이션하며 보여주고, 그 아래에 소셜 로그인 버튼 UI를 함께 구성한 구조입니다.

---

## 주요 특징

### ✅ 1. `Intro` 모델 기반 애니메이션 구성
- 텍스트, 배경색, 원(circle)의 색상 등을 포함한 `Intro` 모델을 정의하여 **순차적으로 변하는 메시지와 배경을 연출**합니다.
- `animate(index:)` 함수는 각 Intro 데이터를 애니메이션을 통해 순차적으로 보여줍니다.
- 텍스트는 왼쪽에서 오른쪽으로 슬라이드되며, 그에 따라 캡슐도 같이 움직입니다.

### ✅ 2. 애니메이션 흐름
- 앱 시작 시 첫 번째 메시지가 표시되고, 이후 **0.15초 지연 후** 애니메이션이 자동으로 순환합니다.
- `.snappy` 애니메이션을 사용하여 부드러운 이동 효과를 구현합니다.
- `textOffset`과 `circleOffset`을 이용하여 텍스트와 원이 움직이는 효과를 만듭니다.

### ✅ 3. 커스텀 로그인 버튼 UI
- Apple, Google, 일반 로그인 버튼을 **개별 스타일**로 구성하였습니다.
- `.fillButton(_:)` modifier를 통해 공통된 버튼 스타일을 재사용합니다.
- 각각의 버튼에는 로고 이미지 또는 텍스트가 포함됩니다.

### ✅ 4. 하단 약관 안내 텍스트
- 하단에는 약관 동의 안내 문구를 **멀티 스타일 텍스트**로 표시하며, `이용약관`과 `개인정보처리방침`은 밑줄 처리되어 강조됩니다.

---

## 애니메이션 구조 요약

| 구성 요소         | 설명 |
|------------------|------|
| `Intro` 모델      | 텍스트, 색상, 위치 오프셋 정보 저장 |
| `animate(_:)`     | 텍스트와 배경 전환 애니메이션 재귀 호출 |
| `textOffset`      | 텍스트의 좌우 이동 애니메이션 제어 |
| `circleOffset`    | 원 모양 UI의 이동 제어 |
| `textSize(_:)`    | 텍스트 크기를 계산해 애니메이션 거리로 사용 |

---

## 활용 예

- 앱 실행 시 사용자에게 브랜드 메시지를 애니메이션으로 전달하고, 이어서 로그인 화면으로 자연스럽게 연결하고 싶은 경우 적합합니다.
- **온보딩 + 로그인 UI를 하나의 화면에서 구성하고 싶은 경우** 활용 가능합니다.

---

## 사용 기술 요약

| 기술 요소        | 설명 |
|------------------|------|
| SwiftUI          | 뷰 계층 및 상태 관리 |
| GeometryReader   | 화면 크기와 SafeArea 계산 |
| Animation        | `.snappy()` 기반 부드러운 상태 전환 |
| View Modifier    | `fillButton(_:)` 커스텀 버튼 스타일링 |
| Text Alignment   | `.offset` 및 `.frame` 조합으로 슬라이딩 구현 |
