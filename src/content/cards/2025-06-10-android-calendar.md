---
id: 9
title: Android 캘린더
description: 커스텀 캘린더
category: android
type: other
image: images/android/Aos-basicCalendar.png
---

```kotlin
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import java.util.*

@Composable
fun FullCalendar() {
    var calendar by remember { mutableStateOf(Calendar.getInstance()) }
    val today = Calendar.getInstance()

    val year = calendar.get(Calendar.YEAR)
    val month = calendar.get(Calendar.MONTH)
    calendar.set(Calendar.DAY_OF_MONTH, 1)

    val firstDayOfWeek = calendar.get(Calendar.DAY_OF_WEEK) - 1
    val daysInMonth = calendar.getActualMaximum(Calendar.DAY_OF_MONTH)
    val totalCells = firstDayOfWeek + daysInMonth

    Column(modifier = Modifier.padding(16.dp)) {

        // 월 이동 컨트롤
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            IconButton(onClick = {
                calendar = (calendar.clone() as Calendar).apply { add(Calendar.MONTH, -1) }
            }) {
                Text("<")
            }

            Text(
                text = "${year}년 ${month + 1}월",
                style = MaterialTheme.typography.titleMedium
            )

            IconButton(onClick = {
                calendar = (calendar.clone() as Calendar).apply { add(Calendar.MONTH, 1) }
            }) {
                Text(">")
            }
        }

        Spacer(modifier = Modifier.height(8.dp))

        // 요일 헤더
        Row(
            horizontalArrangement = Arrangement.SpaceBetween,
            modifier = Modifier.fillMaxWidth()
        ) {
            listOf("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat").forEach { day ->
                Text(
                    text = day,
                    modifier = Modifier.weight(1f),
                    style = MaterialTheme.typography.bodyMedium,
                    maxLines = 1
                )
            }
        }

        Spacer(modifier = Modifier.height(8.dp))

        // 날짜 그리드
        LazyVerticalGrid(
            columns = GridCells.Fixed(7),
            modifier = Modifier.height(300.dp)
        ) {
            items(totalCells) { index ->
                val day = if (index >= firstDayOfWeek) index - firstDayOfWeek + 1 else null
                Box(
                    contentAlignment = Alignment.Center,
                    modifier = Modifier
                        .size(40.dp)
                        .padding(4.dp)
                        .background(
                            color = if (day != null
                                && year == today.get(Calendar.YEAR)
                                && month == today.get(Calendar.MONTH)
                                && day == today.get(Calendar.DAY_OF_MONTH)
                            ) Color.Cyan else Color.Transparent,
                            shape = MaterialTheme.shapes.small
                        )
                ) {
                    if (day != null) {
                        Text(text = "$day")
                    }
                }
            }
        }
    }
}
```

##설명

이 예제는 실전 캘린더 기능을 추가합니다:
1. 'Calendar.getInstance()'로 현재 날짜 가져오기(Cyan으로 표시)  
2. 'IconButton'으로 월 이동 기능 구현  
3. 'Calendar.add(Calendar.MONTH, ±1)'로 월 변경  

##주요 특징
- 월 이동 가능 (이전/다음)  
- 오늘 날짜 강조  
- 상태 저장을 위해 remember 사용  
- java.util.Calendar 사용하여 월별 일수 자동 계산  
