---
id: 8
title: CustomSegmentControl
description: 커스텀 세그먼트 컨트롤 + 언더라인 이동 UI 구현 예제
category: UIKit
type: other
image: /images/UIKit/segment-control.gif
---

```swift
import UIKit

final class CustomSegmentControlVC: UIViewController {

    private let segmentedControl: UISegmentedControl = {
        let segment = UISegmentedControl(items: ["첫번째", "두번째", "세번째"])
        segment.translatesAutoresizingMaskIntoConstraints = false
        segment.selectedSegmentIndex = 0
        // 스타일 커스텀
        segment.setTitleTextAttributes([
            NSAttributedString.Key.foregroundColor: UIColor.gray
        ], for: .normal)
        segment.setTitleTextAttributes([
            NSAttributedString.Key.foregroundColor: UIColor.invertedSystemBackground,
            .font: UIFont.systemFont(ofSize: 15, weight: .bold)
        ], for: .selected)
        segment.selectedSegmentTintColor = .clear
        let image = UIImage()
        segment.setBackgroundImage(image, for: .normal, barMetrics: .default)
        segment.setBackgroundImage(image, for: .selected, barMetrics: .default)
        segment.setBackgroundImage(image, for: .highlighted, barMetrics: .default)
        segment.setDividerImage(image, forLeftSegmentState: .selected, rightSegmentState: .normal, barMetrics: .default)
        return segment
    }()

    private let underlineView: UIView = {
        let view = UIView()
        view.backgroundColor = .invertedSystemBackground
        view.layer.cornerRadius = 0
        return view
    }()

    private let vc1: UIViewController = {
        let vc = UIViewController()
        vc.view.backgroundColor = .black
        return vc
    }()
    private let vc2: UIViewController = {
        let vc = UIViewController()
        vc.view.backgroundColor = .gray
        return vc
    }()
    private let vc3: UIViewController = {
        let vc = UIViewController()
        vc.view.backgroundColor = .lightGray
        return vc
    }()
    var dataViewControllers: [UIViewController] { [vc1, vc2, vc3] }

    private lazy var pageViewController: UIPageViewController = {
        let vc = UIPageViewController(transitionStyle: .scroll, navigationOrientation: .horizontal)
        vc.setViewControllers([self.dataViewControllers[0]], direction: .forward, animated: true)
        vc.delegate = self
        vc.dataSource = self
        vc.view.translatesAutoresizingMaskIntoConstraints = false
        return vc
    }()

    var currentPage: Int = 0 {
        didSet {
            let direction: UIPageViewController.NavigationDirection = oldValue <= self.currentPage ? .forward : .reverse
            self.pageViewController.setViewControllers(
                [dataViewControllers[self.currentPage]],
                direction: direction,
                animated: true,
                completion: nil
            )
            moveUnderline(animated: true)
        }
    }

    override func viewDidLoad() {
        super.viewDidLoad()
 
        
        self.view.addSubview(self.segmentedControl)
        self.view.addSubview(self.underlineView)
        self.view.addSubview(self.pageViewController.view)

        NSLayoutConstraint.activate([
            segmentedControl.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            segmentedControl.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            segmentedControl.topAnchor.constraint(equalTo: view.topAnchor, constant: 80),
            segmentedControl.heightAnchor.constraint(equalToConstant: 50),

            pageViewController.view.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            pageViewController.view.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            pageViewController.view.bottomAnchor.constraint(equalTo: view.bottomAnchor),
            pageViewController.view.topAnchor.constraint(equalTo: segmentedControl.bottomAnchor),
        ])

        // 언더라인의 높이와 최초 위치 설정 (width, x는 viewDidLayoutSubviews에서)
        underlineView.frame = CGRect(x: 0, y: 0, width: 0, height: 4)

        segmentedControl.addTarget(self, action: #selector(changeValue(control:)), for: .valueChanged)
        segmentedControl.selectedSegmentIndex = 0
        changeValue(control: segmentedControl)
    }

    override func viewDidLayoutSubviews() {
        super.viewDidLayoutSubviews()
        // 최초 렌더링 시 언더라인 위치 정확히 세팅
        moveUnderline(animated: false)
        // 언더라인의 y위치를 세그먼트 하단에 맞추기
        let segFrame = segmentedControl.frame
        underlineView.frame.origin.y = segFrame.maxY - 4
        underlineView.frame.size.height = 4
    }

    @objc private func changeValue(control: UISegmentedControl) {
        self.currentPage = control.selectedSegmentIndex
    }

    /// 언더라인 이동 (frame 연산)
    private func moveUnderline(animated: Bool) {
        let segFrame = segmentedControl.frame
        let segmentCount = CGFloat(segmentedControl.numberOfSegments)
        let segmentWidth = segFrame.width / segmentCount
        let targetX = segFrame.minX + segmentWidth * CGFloat(segmentedControl.selectedSegmentIndex)

        let newFrame = CGRect(x: targetX,
                              y: segFrame.maxY - 4,
                              width: segmentWidth,
                              height: 4)
        if animated {
            UIView.animate(withDuration: 0.2) {
                self.underlineView.frame = newFrame
            }
        } else {
            self.underlineView.frame = newFrame
        }
    }
}

extension CustomSegmentControlVC: UIPageViewControllerDataSource, UIPageViewControllerDelegate {
    func pageViewController(_ pageViewController: UIPageViewController, viewControllerBefore viewController: UIViewController) -> UIViewController? {
        guard let index = self.dataViewControllers.firstIndex(of: viewController), index - 1 >= 0 else { return nil }
        return self.dataViewControllers[index - 1]
    }
    func pageViewController(_ pageViewController: UIPageViewController, viewControllerAfter viewController: UIViewController) -> UIViewController? {
        guard let index = self.dataViewControllers.firstIndex(of: viewController), index + 1 < self.dataViewControllers.count else { return nil }
        return self.dataViewControllers[index + 1]
    }
    func pageViewController(_ pageViewController: UIPageViewController, didFinishAnimating finished: Bool, previousViewControllers: [UIViewController], transitionCompleted completed: Bool) {
        guard let viewController = pageViewController.viewControllers?[0], let index = self.dataViewControllers.firstIndex(of: viewController) else { return }
        self.currentPage = index
        self.segmentedControl.selectedSegmentIndex = index
        self.moveUnderline(animated: true)
    }
}

#Preview {
    CustomSegmentControlVC()
}

extension UIColor {
    static var invertedSystemBackground: UIColor {
        return UIColor { traitCollection in
            switch traitCollection.userInterfaceStyle {
            case .dark:
                // 다크 모드에서는 밝은 배경색
                return .white
            default:
                // 라이트 모드에서는 어두운 배경색
                return .black
            }
        }
    }
}
```

## 설명

이 예제는 UIKit에서 `UISegmentedControl`과 `UIPageViewController`를 결합해,  
세그먼트 선택에 따라 아래 언더라인이 부드럽게 이동하면서  
각 페이지 컨텐츠(`UIViewController`)를 전환하는 커스텀 컴포넌트를 보여줍니다.

1. `UISegmentedControl(items:)`로 세그먼트를 생성하고 텍스트·색상·배경 이미지를 커스터마이즈합니다.  
2. 선택된 인덱스 변화 시 `UIPageViewController.setViewControllers(...)`를 호출해 해당 페이지로 이동합니다.  
3. 세그먼트 아래에 `underlineView`를 두고, `frame` 조정 애니메이션으로 선택 위치에 맞게 이동시킵니다.  
4. 페이지 스와이프 완료 시 델리게이트 콜백에서 세그먼트 인덱스와 언더라인을 동기화합니다.

## 주요 특징

- `UISegmentedControl` 텍스트·폰트·컬러·배경 커스터마이징  
- 선택 변경에 따른 `UIPageViewController` 페이지 전환  
- 언더라인 뷰(`underlineView`)의 애니메이션 이동  
- 페이지 스와이프와 세그먼트 탭 간 양방향 동기화  

