---
id: 11
title: Onboarding - Uikit
description: UIPageViewController 온보딩
category: UIKit
type: other
image: /images/UIKit/onboarding.gif
---

```swift
import UIKit

final class StartViewController: UIViewController {
    
    // MARK: - UI Component

    // MARK: - LifeCycle
    override func viewDidLoad() {
        super.viewDidLoad()
        makeUI()
    }
    
    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
        checnToturialRul()
    }
    
    // MARK: - UI Setting
    private func makeUI() {
        view.backgroundColor = .white
    }
}

// MARK: - 튜토리얼 유뮤에 따라 온보딩 화면 생성
extension StartViewController {
    func checnToturialRul() {
        let userDefault = UserDefaults.standard
        if userDefault.bool(forKey: "Tutorial") == false {
            let onboardingVC = OnboardingViewController(transitionStyle: .scroll, navigationOrientation: .horizontal)
            onboardingVC.modalPresentationStyle = .fullScreen
            present(onboardingVC, animated: false)
        }
    }
}

final class OnboardingViewController: UIPageViewController {
    
    // MARK: - property
    private var pages: [UIViewController] = []
    private lazy var pageControl: UIPageControl = {
        let pc = UIPageControl()
        pc.currentPageIndicatorTintColor = .black
        pc.pageIndicatorTintColor = .lightGray
        return pc
    }()
    

    // MARK: - LifeCycle
    override func viewDidLoad() {
        super.viewDidLoad()
        makeUI()
        constraints()
    }
    
    // MARK: - UI Setting
    private func makeUI() {
        view.backgroundColor = .white
        let page1 = PageContentsViewController(imageName: "1",
                                               title: "하루 한컷",
                                               subTitle: "가족과의 하루를 한 장의 사진으로 \n나눠보세요.")
        let page2 = PageContentsViewController(imageName: "3",
                                               title: "일상 공유",
                                               subTitle: "매일의 이야기를 함께 나눠요.\n")
        let page3 = PageContentsViewController(imageName: "4",
                                               title: "기록을 한눈에",
                                               subTitle: "달력으로 사진을 돌아볼 수 있어요.\n")
        
        let page4 = PageContentsViewController(imageName: "5",
                                               title: "나의 이야기, 나만의 공간에",
                                               subTitle: "내가 남긴 기록을 한 곳에 담아보세요.\n")
        pages.append(contentsOf: [page1, page2, page3, page4])
        
        // dataSource 화면에 보여질 뷰컨트롤러들을 관리
        self.dataSource = self
        self.delegate = self
        
        // UIPageViewController에서 처음 보여질 뷰컨트롤러 설정(첫 page)
        self.setViewControllers([pages[0]], direction: .forward, animated: true)
        
        view.addSubview(pageControl)
        pageControl.translatesAutoresizingMaskIntoConstraints = false
        pageControl.numberOfPages = pages.count
    }
    
    private func constraints() {
        NSLayoutConstraint.activate([
            pageControl.bottomAnchor.constraint(equalTo: view.safeAreaLayoutGuide.bottomAnchor, constant: -10),
            pageControl.centerXAnchor.constraint(equalTo: view.centerXAnchor)
        ])
    }
    
}

extension OnboardingViewController: UIPageViewControllerDataSource {
    // 이전 뷰 컨트롤러 리턴(우측 -> 좌측 슬라이드 제스처)
    func pageViewController(_ pageViewController: UIPageViewController, viewControllerBefore viewController: UIViewController) -> UIViewController? {
        // 현재 vc 인덱스 구하기
        guard let currentIndex = pages.firstIndex(of: viewController) else { return nil }
        
        // 현재 인덱스가 0보다 크다면 다음 줄로 이동
        guard currentIndex > 0 else { return nil }
        return pages[currentIndex - 1]
    }
    
    // 다음 뷰 컨트롤러 화면(좌측 -> 우측 슬라이드 제스처)
    func pageViewController(_ pageViewController: UIPageViewController, viewControllerAfter viewController: UIViewController) -> UIViewController? {
        // 현재 vc 인덱스 구하기
        guard let currentIndex = pages.firstIndex(of: viewController) else { return nil }
        
        // 현재 인덱스가 마지막 인덱스보다 작을 때만 다음줄로 이동
        guard currentIndex < (pages.count - 1) else { return nil }
        return pages[currentIndex + 1]
    }
    
    
}

extension OnboardingViewController: UIPageViewControllerDelegate {
    
    func pageViewController(_ pageViewController: UIPageViewController,
                                didFinishAnimating finished: Bool,
                                previousViewControllers: [UIViewController],
                                transitionCompleted completed: Bool) {
            guard completed,
                  let currentVC = viewControllers?.first,
                  let index = pages.firstIndex(of: currentVC) else { return }
            pageControl.currentPage = index
        }
}


final class PageContentsViewController: UIViewController {
    
    // MARK: - UI Component
    private lazy var stackView: UIStackView = {
        let sv = UIStackView(arrangedSubviews: [imageView, titleLabel, subTitleLabel])
        sv.axis = .vertical
        sv.spacing = 20
        sv.alignment = .center
        return sv
    }()
    private let imageView: UIImageView = {
        let iv = UIImageView()
        iv.contentMode = .scaleAspectFill
        return iv
    }()
    private let titleLabel: UILabel = {
        let label = UILabel()
        label.font = .preferredFont(forTextStyle: .title1)
        return label
    }()
    private let subTitleLabel: UILabel = {
        let label = UILabel()
        label.font = .preferredFont(forTextStyle: .body)
        label.textAlignment = .center
        label.numberOfLines = 0
        return label
    } ()
    
    
    init(imageName: String, title: String, subTitle: String) {
        super.init(nibName: nil, bundle: nil)
        imageView.image = UIImage(named: imageName)
        titleLabel.text = title
        subTitleLabel.text = subTitle
    }
    
    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
    // MARK: - LifeCycle
    override func viewDidLoad() {
        super.viewDidLoad()
        makeUI()
        constraints()
    }

    // MARK: - UI Setting
    private func makeUI() {
        view.backgroundColor = .white
        view.addSubview(stackView)
        stackView.translatesAutoresizingMaskIntoConstraints = false
    }
    
    private func constraints() {
        NSLayoutConstraint.activate([
            
            // stackView - 중앙 정렬 + 좌우 여백
            stackView.centerYAnchor.constraint(equalTo: view.centerYAnchor),
            stackView.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            stackView.widthAnchor.constraint(equalTo: view.widthAnchor, constant: -100),  // inset 50 * 2
            
            // imageView - view 기준으로 60%
            imageView.widthAnchor.constraint(equalTo: view.widthAnchor, multiplier: 0.6),
            imageView.heightAnchor.constraint(equalTo: view.heightAnchor, multiplier: 0.6)
        ])
    }
}

#Preview {
    OnboardingViewController(transitionStyle: .scroll, navigationOrientation: .horizontal)
}
```

## 설명

이 예제는 UIKit 기반 앱에서 **온보딩 화면을 구성하는 방법**을 보여줍니다. 앱이 처음 실행될 때 `UserDefaults`를 통해 사용자가 온보딩을 이미 봤는지 판단하고, 보지 않았다면 `UIPageViewController`를 활용한 온보딩 뷰를 전체 화면으로 표시합니다.

- `StartViewController`: 앱 시작 시 온보딩 필요 여부를 판단하고 온보딩 화면을 띄움  
- `OnboardingViewController`: 여러 페이지로 구성된 온보딩 컨트롤러  
- `PageContentsViewController`: 각 온보딩 페이지의 내용 (이미지, 타이틀, 설명)을 구성  
- `UIPageControl`: 현재 페이지 위치를 표시

## 주요 특징

- ✅ `UserDefaults`를 통한 온보딩 실행 여부 저장
- ✅ `UIPageViewController`를 사용한 스크롤 기반 온보딩 구성
- ✅ `UIPageControl`로 페이지 인디케이터 표시
- ✅ 각 페이지에 이미지와 설명을 삽입할 수 있는 커스터마이징 구조

## 사용 예시

앱 최초 실행 시:

```swift
let userDefault = UserDefaults.standard
if userDefault.bool(forKey: "Tutorial") == false {
    let onboardingVC = OnboardingViewController(transitionStyle: .scroll, navigationOrientation: .horizontal)
    onboardingVC.modalPresentationStyle = .fullScreen
    present(onboardingVC, animated: false)
}