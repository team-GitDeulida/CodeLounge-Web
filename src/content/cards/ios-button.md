---
id: 2
title: iOS 버튼
description: iOS 스타일의 버튼 컴포넌트
category: ios
type: other
image: /images/ios-button.png
---

```swift
import UIKit

class CustomButton: UIButton {
    override init(frame: CGRect) {
        super.init(frame: frame)
        setupButton()
    }
    
    required init?(coder: NSCoder) {
        super.init(coder: coder)
        setupButton()
    }
    
    private func setupButton() {
        backgroundColor = .systemBlue
        layer.cornerRadius = 8
        titleLabel?.font = .systemFont(ofSize: 16, weight: .medium)
        setTitleColor(.white, for: .normal)
    }
}
``` 