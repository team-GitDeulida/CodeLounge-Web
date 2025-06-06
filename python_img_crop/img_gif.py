# from PIL import Image, ImageChops, ImageDraw, ImageSequence

# # 1. 베젤 이미지 불러오기 (RGBA, 원본 크기 그대로 유지)
# bezel = Image.open("bezel.png").convert("RGBA")
# bezel_w, bezel_h = bezel.size

# # 2. 베젤의 알파 채널만 뽑아서, 내부 투명 영역(screen)만 살리는 반전 마스크 생성
# bezel_alpha = bezel.split()[3]  # A 채널
# inverted_bezel_mask = ImageChops.invert(bezel_alpha)

# # 3. 베젤 내부 ‘스크린’ 영역(bounding box) 계산
# transparent_mask = bezel_alpha.point(lambda p: 255 if p == 0 else 0, mode="L")
# screen_box = transparent_mask.getbbox()
# if screen_box is None:
#     raise ValueError("베젤에 투명 영역(스크린)이 없습니다.")
# screen_left, screen_top, screen_right, screen_bottom = screen_box
# screen_w = screen_right - screen_left
# screen_h = screen_bottom - screen_top

# # 4. 포어그라운드 GIF 또는 단일 이미지 열기
# foreground = Image.open("foreground.gif")  # .is_animated=True 이면 GIF

# # 5. 둥근 모서리 반경(px) 설정
# radius = 100

# # 6. 합성된 RGBA 프레임과 각 프레임의 duration을 저장할 리스트
# composited_frames = []
# frame_durations = []

# # 7. 프레임별 처리
# for frame in ImageSequence.Iterator(foreground):
#     # 7-1. 원본 프레임을 RGBA로 변환
#     frame_rgba = frame.convert("RGBA")
#     fg_orig_w, fg_orig_h = frame_rgba.size

#     # 7-2. “screen_w × screen_h”에 맞춰 비율 유지하며 축소(fit)
#     #      scale = min(screen_w/fg_orig_w, screen_h/fg_orig_h, 1.0)
#     scale = min(screen_w / fg_orig_w, screen_h / fg_orig_h, 4.5)
#     new_w = int(fg_orig_w * scale)
#     new_h = int(fg_orig_h * scale)
#     frame_resized = frame_rgba.resize((new_w, new_h), Image.LANCZOS)

#     # 7-3. 리사이즈된 프레임에 둥근 모서리 마스크 씌우기
#     mask = Image.new("L", (new_w, new_h), 0)
#     draw = ImageDraw.Draw(mask)
#     draw.rounded_rectangle(
#         [(0, 0), (new_w, new_h)],
#         radius=radius,
#         fill=255
#     )
#     frame_resized.putalpha(mask)

#     # 7-4. 베젤 크기(bezel_w×bezel_h)와 동일한 투명 캔버스 생성
#     fg_canvas = Image.new("RGBA", (bezel_w, bezel_h), (0, 0, 0, 0))

#     # 7-5. “screen_box 내부에서 가운데 정렬”로 붙이기
#     paste_x = screen_left + (screen_w - new_w) // 2
#     paste_y = screen_top + (screen_h - new_h) // 2
#     fg_canvas.paste(frame_resized, (paste_x, paste_y), frame_resized)

#     # 7-6. 베젤 반전 마스크를 fg_canvas 알파로 교체 → 테두리 영역은 투명(0), 내부만 보이게(255)
#     fg_canvas.putalpha(inverted_bezel_mask)

#     # 7-7. 최종 합성: 빈 캔버스 위에 fg_canvas → 베젤 순서로 덮기
#     composite = Image.new("RGBA", (bezel_w, bezel_h), (0, 0, 0, 0))
#     composite.alpha_composite(fg_canvas)
#     composite.alpha_composite(bezel)

#     # 7-8. 결과 리스트에 저장
#     composited_frames.append(composite)
#     frame_durations.append(frame.info.get("duration", 100))

# # 8. 저장: 프레임이 1개면 PNG, 여러 개면 애니메이션 GIF
# if len(composited_frames) == 1:
#     composited_frames[0].save("output.png")
# else:
#     composited_frames[0].save(
#         "output.gif",
#         save_all=True,
#         append_images=composited_frames[1:],
#         loop=0,
#         duration=frame_durations,
#         disposal=2
#     )



# from PIL import Image, ImageChops, ImageDraw, ImageSequence

# # 1. 베젤 이미지 불러오기 (RGBA, 원본 크기 그대로 유지)
# bezel = Image.open("bezel.png").convert("RGBA")
# bezel_w, bezel_h = bezel.size

# # 2. 베젤의 알파 채널 추출
# bezel_alpha = bezel.split()[3]  # A 채널 (255=불투명, 0=투명)

# # 3. 베젤 내부 ‘스크린’ 영역(bounding box) 계산
# transparent_mask = bezel_alpha.point(lambda p: 255 if p == 0 else 0, mode="L")
# screen_box = transparent_mask.getbbox()
# if screen_box is None:
#     raise ValueError("베젤에 투명 영역(스크린)이 없습니다.")
# screen_left, screen_top, screen_right, screen_bottom = screen_box
# screen_w = screen_right - screen_left
# screen_h = screen_bottom - screen_top

# # 4. 베젤 내부 전체(테두리+스크린)를 나타내는 최종 마스크 생성
# #    bezel_alpha: 테두리 영역 255, 스크린 영역 0
# #    transparent_mask: 스크린 영역 255, 테두리 영역 0
# #    이 둘을 합쳐서 “베젤 내부(255) vs 베젤 외부(0)”가 되도록 함
# full_bezel_mask = ImageChops.lighter(bezel_alpha, transparent_mask)
# # → full_bezel_mask: bezel 바깥=0, bezel 내부(테두리+스크린)=255

# # 5. 포어그라운드 GIF 또는 단일 이미지 열기
# foreground = Image.open("foreground.gif")  # .is_animated=True 이면 GIF

# # 6. 둥근 모서리 반경(px) 설정
# radius = 100

# # 7. 합성된 RGBA 프레임과 각 프레임의 duration 저장용 리스트
# composited_frames = []
# frame_durations = []

# # 8. 프레임별 처리
# for frame in ImageSequence.Iterator(foreground):
#     # 8-1. 원본 프레임을 RGBA로 변환
#     frame_rgba = frame.convert("RGBA")
#     fg_orig_w, fg_orig_h = frame_rgba.size

#     # 8-2. “screen_w × screen_h”에 맞춰 비율 유지하며 축소(fit) — 최대 4.5배까지 확대 허용
#     scale = min(screen_w / fg_orig_w, screen_h / fg_orig_h, 4.5)
#     new_w = int(fg_orig_w * scale)
#     new_h = int(fg_orig_h * scale)
#     frame_resized = frame_rgba.resize((new_w, new_h), Image.LANCZOS)

#     # 8-3. 리사이즈된 프레임에 둥근 모서리 마스크 씌우기
#     mask = Image.new("L", (new_w, new_h), 0)
#     draw = ImageDraw.Draw(mask)
#     draw.rounded_rectangle(
#         [(0, 0), (new_w, new_h)],
#         radius=radius,
#         fill=255
#     )
#     frame_resized.putalpha(mask)

#     # 8-4. 베젤 크기와 동일한 완전 투명 캔버스 생성
#     composite = Image.new("RGBA", (bezel_w, bezel_h), (0, 0, 0, 0))

#     # 8-5. “베젤 내부 스크린 영역”만 흰색 배경으로 채우기
#     #      transparent_mask: 베젤 내부 스크린(255), 나머지(0)
#     white_bg = Image.new("RGBA", (bezel_w, bezel_h), (255, 255, 255, 255))
#     # 투명 마스크를 사용해 흰색을 스크린 영역 ONLY에 입힘
#     composite.alpha_composite(Image.new("RGBA", (bezel_w, bezel_h), (0, 0, 0, 0)))  # 빈 캔버스
#     composite.paste(white_bg, (0, 0), transparent_mask)

#     # 8-6. 둥근 모서리 처리된 frame_resized를 “스크린 영역 중앙”에 붙이기
#     paste_x = screen_left + (screen_w - new_w) // 2
#     paste_y = screen_top + (screen_h - new_h) // 2
#     composite.paste(frame_resized, (paste_x, paste_y), frame_resized)

#     # 8-7. 베젤 이미지를 덮어 테두리(및 투명인 스크린 픽셀)를 그대로 유지
#     composite.alpha_composite(bezel)

#     # 8-8. full_bezel_mask를 최종 알파로 적용
#     #      → 베젤 내부(테두리+스크린)는 alpha=255 유지, 베젤 바깥은 alpha=0(투명)
#     composite.putalpha(full_bezel_mask)

#     # 8-9. 결과 리스트에 저장
#     composited_frames.append(composite)
#     frame_durations.append(frame.info.get("duration", 100))

# # 9. 저장: 프레임 개수에 따라 PNG 또는 애니메이션 GIF
# if len(composited_frames) == 1:
#     # 단일 이미지: PNG로 저장 → 배경 투명 유지
#     composited_frames[0].save("output.png")
# else:
#     # 애니메이션: GIF로 저장 시 투명 인덱스 지정
#     composited_frames[0].save(
#         "output.gif",
#         save_all=True,
#         append_images=composited_frames[1:],
#         loop=0,
#         duration=frame_durations,
#         disposal=2,
#         transparency=0
#     )


# from PIL import Image, ImageChops, ImageDraw, ImageSequence

# # 1. 베젤 이미지 불러오기 (RGBA, 원본 크기 그대로 유지)
# bezel = Image.open("bezel.png").convert("RGBA")
# bezel_w, bezel_h = bezel.size

# # 2. 베젤의 알파 채널만 뽑아서, 내부 투명 영역(screen)만 살리는 반전 마스크 생성
# bezel_alpha = bezel.split()[3]  # A 채널
# inverted_bezel_mask = ImageChops.invert(bezel_alpha)

# # 3. 베젤 내부 ‘스크린’ 영역(bounding box) 계산
# transparent_mask = bezel_alpha.point(lambda p: 255 if p == 0 else 0, mode="L")
# screen_box = transparent_mask.getbbox()
# if screen_box is None:
#     raise ValueError("베젤에 투명 영역(스크린)이 없습니다.")
# screen_left, screen_top, screen_right, screen_bottom = screen_box
# screen_w = screen_right - screen_left
# screen_h = screen_bottom - screen_top

# # 4. 포어그라운드 GIF 또는 단일 이미지 열기
# foreground = Image.open("foreground.gif")  # .is_animated=True 이면 GIF

# # 5. 둥근 모서리 반경(px) 설정
# radius = 100

# # 6. 합성된 RGBA 프레임과 각 프레임의 duration을 저장할 리스트
# composited_frames = []
# frame_durations = []

# # 7. 프레임별 처리
# for frame in ImageSequence.Iterator(foreground):
#     # 7-1. 원본 프레임을 RGBA로 변환
#     frame_rgba = frame.convert("RGBA")
#     fg_orig_w, fg_orig_h = frame_rgba.size

#     # 7-2. “screen_w × screen_h”에 맞춰 비율 유지하며 축소(fit)
#     #      scale = min(screen_w/fg_orig_w, screen_h/fg_orig_h, 1.0)
#     scale = min(screen_w / fg_orig_w, screen_h / fg_orig_h, 4.5)
#     new_w = int(fg_orig_w * scale)
#     new_h = int(fg_orig_h * scale)
#     frame_resized = frame_rgba.resize((new_w, new_h), Image.LANCZOS)

#     # 7-3. 리사이즈된 프레임에 둥근 모서리 마스크 씌우기
#     mask = Image.new("L", (new_w, new_h), 0)
#     draw = ImageDraw.Draw(mask)
#     draw.rounded_rectangle(
#         [(0, 0), (new_w, new_h)],
#         radius=radius,
#         fill=255
#     )
#     frame_resized.putalpha(mask)

#     # 7-4. 베젤 크기(bezel_w×bezel_h)와 동일한 투명 캔버스 생성
#     fg_canvas = Image.new("RGBA", (bezel_w, bezel_h), (0, 0, 0, 0))

#     # 7-5. “screen_box 내부에서 가운데 정렬”로 붙이기
#     paste_x = screen_left + (screen_w - new_w) // 2
#     paste_y = screen_top + (screen_h - new_h) // 2
#     fg_canvas.paste(frame_resized, (paste_x, paste_y), frame_resized)

#     # 7-6. 베젤 반전 마스크를 fg_canvas 알파로 교체 → 테두리 영역은 투명(0), 내부만 보이게(255)
#     fg_canvas.putalpha(inverted_bezel_mask)

#     # 7-7. 최종 합성: 빈 캔버스 위에 fg_canvas → 베젤 순서로 덮기
#     composite = Image.new("RGBA", (bezel_w, bezel_h), (0, 0, 0, 0))
#     composite.alpha_composite(fg_canvas)
#     composite.alpha_composite(bezel)

#     # 7-8. 결과 리스트에 저장
#     composited_frames.append(composite)
#     frame_durations.append(frame.info.get("duration", 100))

# # 8. 저장: 프레임이 1개면 PNG, 여러 개면 애니메이션 GIF
# if len(composited_frames) == 1:
#     composited_frames[0].save("output.png")
# else:
#     composited_frames[0].save(
#         "output.gif",
#         save_all=True,
#         append_images=composited_frames[1:],
#         loop=0,
#         duration=frame_durations,
#         disposal=2
#     )

from PIL import Image, ImageChops, ImageDraw, ImageSequence

# 1. 베젤 이미지 불러오기 (RGBA, 원본 크기 그대로 유지)
bezel = Image.open("bezel.png").convert("RGBA")
bezel_w, bezel_h = bezel.size

# 2. 베젤의 알파 채널만 뽑아서, 내부 투명 영역(screen)만 살리는 반전 마스크 생성
bezel_alpha = bezel.split()[3]  # A 채널
inverted_bezel_mask = ImageChops.invert(bezel_alpha)

# 3. 베젤 내부 ‘스크린’ 영역(bounding box) 계산
transparent_mask = bezel_alpha.point(lambda p: 255 if p == 0 else 0, mode="L")
screen_box = transparent_mask.getbbox()
if screen_box is None:
    raise ValueError("베젤에 투명 영역(스크린)이 없습니다.")
screen_left, screen_top, screen_right, screen_bottom = screen_box
screen_w = screen_right - screen_left
screen_h = screen_bottom - screen_top

# 4. 포어그라운드 GIF 또는 단일 이미지 열기
foreground = Image.open("foreground.gif")  # .is_animated=True 이면 GIF

# 5. 둥근 모서리 반경(px) 설정
radius = 100

# 6. 합성된 RGBA 프레임과 각 프레임의 duration을 저장할 리스트
composited_frames = []
frame_durations = []

# 7. 프레임별 처리
for frame in ImageSequence.Iterator(foreground):
    # 7-1. 원본 프레임을 RGBA로 변환
    frame_rgba = frame.convert("RGBA")
    fg_orig_w, fg_orig_h = frame_rgba.size

    # 7-2. “screen_w × screen_h”에 맞춰 비율 유지하며 축소(fit)
    scale = min(screen_w / fg_orig_w, screen_h / fg_orig_h, 4.5)
    new_w = int(fg_orig_w * scale)
    new_h = int(fg_orig_h * scale)
    frame_resized = frame_rgba.resize((new_w, new_h), Image.LANCZOS)

    # 7-3. 리사이즈된 프레임에 둥근 모서리 마스크 씌우기
    mask = Image.new("L", (new_w, new_h), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle(
        [(0, 0), (new_w, new_h)],
        radius=radius,
        fill=255
    )
    frame_resized.putalpha(mask)

    # 7-4. 베젤 크기(bezel_w×bezel_h)와 동일한 투명 캔버스 생성
    fg_canvas = Image.new("RGBA", (bezel_w, bezel_h), (0, 0, 0, 0))

    # 7-5. “screen_box 내부에서 가운데 정렬”로 붙이기
    paste_x = screen_left + (screen_w - new_w) // 2
    paste_y = screen_top + (screen_h - new_h) // 2
    fg_canvas.paste(frame_resized, (paste_x, paste_y), frame_resized)

    # ————— 여기서부터 수정된 부분 —————

    # 7-6. composite 이미지를 빈 캔버스(TOP)이 아닌, 베젤 기준으로 만든 뒤
    #       fg_canvas(포어그라운드)를 먼저 붙이고, 그 위에 베젤을 얹습니다.
    composite = Image.new("RGBA", (bezel_w, bezel_h), (0, 0, 0, 0))
    # 1) 포어그라운드를 빈 캔버스에 붙일 때는 자체 알파를 마스크로 사용
    composite.paste(frame_resized, (paste_x, paste_y), frame_resized)
    # 2) 그 위에 베젤을 붙으면, 베젤 프레임 부분은 원본 이미지가 보이고
    #    바깥 부분은 bezel.png의 투명도를 유지합니다.
    composite.paste(bezel, (0, 0), bezel)

    # 7-7. 결과 리스트에 저장
    composited_frames.append(composite)
    frame_durations.append(frame.info.get("duration", 100))

# 8. 저장: 프레임이 1개면 PNG, 여러 개면 애니메이션 GIF
if len(composited_frames) == 1:
    composited_frames[0].save("output.png")
else:
    composited_frames[0].save(
        "output.gif",
        save_all=True,
        append_images=composited_frames[1:],
        loop=0,
        duration=frame_durations,
        disposal=2
    )
