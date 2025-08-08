---
id: 16
title: Button
description: 버튼 컴포넌트
category: Flutter
type: other
image: /images/Flutter/button.gif
---

```flutter
import 'package:flutter/material.dart';

// 앱의 시작점
void main() {
  runApp(const MyApp());
}

// 앱 전체의 뼈대를 구성하는 Stateless Widget
class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false, // 우측 상단의 debug 배너 제거
      home: ResizableBoxScreen(),               // 첫 화면으로 EmptyScreen 위젯 사용
    );
  }
}

// 상태가 있는 위젯 (사각형 크기 변경을 위해 StatefulWidget 사용)
class ResizableBoxScreen extends StatefulWidget {
  const ResizableBoxScreen({super.key});
  
  @override
  State<ResizableBoxScreen> createState() => _ResizableBoxScreenState();
}

// State 클래스: 사각형의 너비 상태를 저장하고, UI 갱신 담당
class _ResizableBoxScreenState extends State<ResizableBoxScreen> {
  double _boxWidth = 100; // 초기 너비
  final double _initialWidth = 100; // 기본 너비 값 (100)
  final double _expandedWidth = 200; // 확장 너비 값 (200)

  // 버튼 클릭 시 실행되는 함수: 너비를 토글
  void _toggleBoxWidth() {
    setState(() {
      // 현재 너비가 초기값이면 확장, 아니면 초기값으로 복귀
      _boxWidth = (_boxWidth == _initialWidth) ? _expandedWidth : _initialWidth;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        // title: const Text('Rectagle'), // 앱 상단 제목
      ),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center, // 세로 중앙 정렬
        children: [
          // 가운데 파란 사각형 (AnimatedContainer로 부드럽게 크기 변경)
          Center(
            child: AnimatedContainer(
              width: _boxWidth,         // 동적으로 바뀌는 너비
              height: 100,             // 고정된 높이
              duration: const Duration(milliseconds: 300), // 애니메이션 지속 시간
              curve: Curves.easeInOut, // 애니메이션 커브 (부드러운 전환)
              decoration: BoxDecoration(
                color: Colors.blue, // 사각형 색상
                borderRadius: BorderRadius.circular(20), // 모서리 둥글게
              ),
            ),
          ),
          const SizedBox(height: 40), // 사각형과 버튼 사이 간격
          
          // 버튼: 누르면 _toggleBoxWidth 실행
          ElevatedButton(
            onPressed: _toggleBoxWidth, // 버튼 누르면 사각형 크기 토글
            child: const Text('사각형 크기 변경'), // 버튼 텍스트
          ),
        ],
      ),
    );
  }
}
```

## 설명

이 예제는 **Flutter 버튼**을 이용하여 **사각형의 가로 크기를 동적으로 변경**하는 인터랙션을 구현한 예제입니다.

버튼을 누를 때마다 사각형의 너비가 100 ↔ 200으로 토글되며, `AnimatedContainer`를 사용해 부드러운 애니메이션으로 크기 변화가 표현됩니다.

---

## 주요 특징

### ✅ 1. `AnimatedContainer`로 부드러운 크기 변화
- `Container` 대신 `AnimatedContainer`를 사용하여 `width` 값이 바뀔 때 애니메이션 효과 적용
- `duration`과 `curve`를 통해 애니메이션 속도와 곡선 제어

### ✅ 2. 버튼을 통한 상태 토글
- `ElevatedButton`을 누르면 `setState()`를 통해 사각형의 너비 상태가 변경됨
- 두 번 누를 때마다 100 → 200 → 100 순으로 반복

### ✅ 3. 심플한 UI 구성
- `Center`로 박스를 가운데 정렬
- `SizedBox`를 사용하여 박스와 버튼 사이 간격 설정

---

## 활용 예

- **애니메이션 학습용 기본 예제**
- 버튼 클릭 시 UI 요소 크기나 모양이 변하도록 구성할 때 활용 가능
- 박스 대신 이미지, 텍스트 등으로 확장 가능

---

## 사용 기술 요약

| 기술 요소            | 설명 |
|---------------------|------|
| `StatefulWidget`     | 상태 변화에 따라 UI를 갱신 |
| `AnimatedContainer`  | 속성 변경 시 부드러운 애니메이션 |
| `setState()`         | 상태 변경 트리거 |
| `ElevatedButton`     | 기본 클릭 버튼 |
| `BoxDecoration`      | 사각형 색상, 둥근 모서리 지정 |
| `borderRadius`       | 모서리를 둥글게 처리 (Radius.circular) |
