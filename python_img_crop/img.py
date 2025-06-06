

# from PIL import Image, ImageChops

# # 1. 베젤 이미지 (투명 영역을 포함한 PNG)
# bezel = Image.open("bezel.png").convert("RGBA")

# # 2. 넣고 싶은 이미지 (예: 시뮬레이터 스크린샷) — 크기 절대 변경하지 않음
# foreground = Image.open("foreground.png").convert("RGBA")

# # 3. 빈 캔버스 생성 (베젤과 동일 크기)
# canvas = Image.new("RGBA", bezel.size, (0, 0, 0, 0))

# # 4. foreground를 캔버스 위에 붙일 임시 이미지(fg_canvas) 생성
# fg_canvas = Image.new("RGBA", bezel.size, (0, 0, 0, 0))

# #    foreground를 ‘가운데 정렬’ 예시:
# bezel_w, bezel_h = bezel.size
# fg_w, fg_h = foreground.size
# offset_x = (bezel_w - fg_w) // 2
# offset_y = (bezel_h - fg_h) // 2

# #    fg_canvas에 원본 크기 그대로 붙이기
# fg_canvas.paste(foreground, (offset_x, offset_y), foreground)
# #    → 이 시점에서 fg_canvas에는 foreground 전체가 원본 해상도로 (offset_x, offset_y) 위치에 복사됨.

# # 5. 베젤의 알파 채널을 추출
# bezel_alpha = bezel.split()[3]  # RGBA 중 A 채널

# # 6. bezel_alpha를 반전(Invert)하여 “투명=255, 불투명=0” 형태의 마스크 생성
# inverted_mask = ImageChops.invert(bezel_alpha)
# #    - bezel_alpha가 0(완전 투명)이면 inverted_mask는 255 → fg_canvas에서 보이게 함.
# #    - bezel_alpha가 255(완전 불투명)이면 inverted_mask는 0 → fg_canvas에서 그 부분 가림.

# # 7. fg_canvas의 알파 채널을 inverted_mask로 교체
# fg_canvas.putalpha(inverted_mask)
# #    → 이렇게 하면 fg_canvas는 “베젤의 투명 영역(스크린 부분)에서만 보이고, 
# #       베젤 불투명 영역(테두리) 밖은 모두 투명 처리” 됨.

# # 8. 빈 캔버스에 마스킹된 fg_canvas 먼저 합성
# canvas.alpha_composite(fg_canvas)

# # 9. 그 위에 원본 베젤을 덮어씌워서 테두리는 그대로 보이도록 함
# canvas.alpha_composite(bezel)

# # 10. 결과 저장
# canvas.save("output.png")


# from PIL import Image, ImageChops, ImageDraw

# # 1. 베젤 이미지 (투명 영역을 포함한 PNG)
# bezel = Image.open("bezel.png").convert("RGBA")

# # 2. 넣고 싶은 이미지 (예: 시뮬레이터 스크린샷) — 크기 절대 변경하지 않음
# foreground = Image.open("foreground.png").convert("RGBA")

# # foreground 원본 크기
# fg_w, fg_h = foreground.size

# # 2-1. 포어그라운드에 둥근 모서리 마스크 적용
# #    (radius 값은 필요에 따라 조정하면 됩니다)
# radius = 100  # 모서리 둥글기 픽셀 단위 (예: 30px)
# #  마스크 이미지를 포어그라운드와 같은 크기의 흑백('L') 모드로 생성
# mask = Image.new("L", (fg_w, fg_h), 0)
# draw = ImageDraw.Draw(mask)
# #  라운드된 사각형을 그려서 내부를 흰색(255)으로 채움
# draw.rounded_rectangle(
#     [(0, 0), (fg_w, fg_h)],
#     radius=radius,
#     fill=255
# )
# #  foreground의 알파 채널을 둥근 모서리 마스크로 교체
# #  (원본 foreground에 알파 채널이 이미 있을 수 있으므로
# #   putalpha(mask)로 덮어쓰면 완전히 마스크가 적용됨)
# foreground.putalpha(mask)

# # 3. 빈 캔버스 생성 (베젤과 동일 크기)
# canvas = Image.new("RGBA", bezel.size, (0, 0, 0, 0))

# # 4. foreground를 캔버스 위에 붙일 임시 이미지(fg_canvas) 생성
# fg_canvas = Image.new("RGBA", bezel.size, (0, 0, 0, 0))

# #    포어그라운드를 ‘가운데 정렬’ 예시:
# bezel_w, bezel_h = bezel.size
# offset_x = (bezel_w - fg_w) // 2
# offset_y = (bezel_h - fg_h) // 2

# #    fg_canvas에 원본 크기(이제 둥근 모서리 적용됨) 그대로 붙이기
# fg_canvas.paste(foreground, (offset_x, offset_y), foreground)

# # 5. 베젤의 알파 채널을 추출
# bezel_alpha = bezel.split()[3]  # RGBA 중 A 채널

# # 6. bezel_alpha를 반전(Invert)하여 “투명=255, 불투명=0” 형태의 마스크 생성
# inverted_mask = ImageChops.invert(bezel_alpha)
# #    - bezel_alpha가 0(완전 투명)이면 inverted_mask는 255 → fg_canvas에서 보이게 함.
# #    - bezel_alpha가 255(완전 불투명)이면 inverted_mask는 0 → fg_canvas에서 그 부분 가림.

# # 7. fg_canvas의 알파 채널을 inverted_mask로 교체
# fg_canvas.putalpha(inverted_mask)
# #    → 이렇게 하면 fg_canvas는 “베젤의 투명 영역(스크린 부분)에서만 보이고,
# #       베젤 불투명 영역(테두리) 밖은 모두 투명 처리” 됨.

# # 8. 빈 캔버스에 마스킹된 fg_canvas 먼저 합성
# canvas.alpha_composite(fg_canvas)

# # 9. 그 위에 원본 베젤을 덮어씌워서 테두리는 그대로 보이도록 함
# canvas.alpha_composite(bezel)

# # 10. 결과 저장
# canvas.save("output.png")

from PIL import Image, ImageChops, ImageDraw

# 1. 베젤 이미지 (투명 영역을 포함한 PNG)
bezel = Image.open("bezel.png").convert("RGBA")
bezel_w, bezel_h = bezel.size

# 2. 넣고 싶은 이미지 (예: 시뮬레이터 스크린샷) — 크기 변경 없이 그대로 둠
foreground = Image.open("foreground.png").convert("RGBA")
fg_w, fg_h = foreground.size

# 2-1. 포어그라운드에 둥근 모서리 마스크 적용 (radius는 필요에 따라 조정)
radius = 100
mask = Image.new("L", (fg_w, fg_h), 0)
draw = ImageDraw.Draw(mask)
draw.rounded_rectangle(
    [(0, 0), (fg_w, fg_h)],
    radius=radius,
    fill=255
)
# putalpha를 사용해 foreground에 둥근 모서리 알파 채널을 덮어씀
foreground.putalpha(mask)

# 3. 빈 캔버스 생성 (베젤과 동일 크기, 완전 투명)
canvas = Image.new("RGBA", (bezel_w, bezel_h), (0, 0, 0, 0))

# 4. fg_canvas: 베젤 크기와 동일한 빈 투명 이미지
fg_canvas = Image.new("RGBA", (bezel_w, bezel_h), (0, 0, 0, 0))

# 4-1. foreground를 중앙 정렬로 붙이기
offset_x = (bezel_w - fg_w) // 2
offset_y = (bezel_h - fg_h) // 2
fg_canvas.paste(foreground, (offset_x, offset_y), foreground)

# 5. 베젤의 알파 채널을 가져와서 반전 마스크 생성
bezel_alpha = bezel.split()[3]                   # 베젤의 A 채널
inverted_mask = ImageChops.invert(bezel_alpha)   # 투명=255, 불투명=0

# 6. fg_canvas를 canvas 위에 붙일 때 inverted_mask를 마스크로 사용
#    → 이렇게 하면 베젤의 “투명 영역(스크린 부분)”에만 fg_canvas가 보여지고,
#       베젤 바깥(알파=255)이면 fg_canvas가 가려집니다.
canvas.paste(fg_canvas, (0, 0), mask=inverted_mask)

# 7. 마지막으로 원본 베젤을 맨 위에 그대로 붙임 (테두리와 내부 경계가 유지됨)
canvas.paste(bezel, (0, 0), bezel)

# 8. 결과 저장
canvas.save("output.png")
