---
name: humanizer-kr
description: >-
  Use this skill to refine Korean documentation, commit messages, PR descriptions, and code comments into clear, concise, natural Korean, removing robotic AI tone and translation artifacts while preserving 100% technical facts.
---

# Humanizer-KR: 자연스러운 한국어 테크니컬 라이팅

이 스킬은 hjongc의 `humanizer-kr` 원칙을 기반으로, AI 특유의 번역투, 어색한 피동 표현, 과장된 챗봇 문체를 걷어내고 실무 엔지니어가 읽기 편한 간결하고 자연스러운 한국어 문장으로 교정합니다.

---

## 1. 5대 교정 원칙

1. **AI 번역투 제거**:
   - "~에 대한 고려가 필요합니다" → "~을 검토해야 합니다"
   - "~을 수행할 수 있도록 합니다" → "~합니다" / "~하도록 지원합니다"
   - "~에 의해 생성되어집니다" → "~가 생성합니다" (이중 피동 금지)

2. **명확하고 단호한 어조**:
   - 불필요한 미사여구나 상투적인 챗봇 인사말("좋은 질문입니다", "최선을 다해 도와드리겠습니다")을 배제하고 즉시 요점을 전달합니다.

3. **고유명사 및 기술 용어 보존**:
   - 함수명, 클래스명, API 필드명, 수치, 버전, RFC 표준 용어는 100% 원문 그대로 보존합니다.

4. **단문 중심의 명료한 호흡**:
   - 한 문장에 주어와 서술어가 3개 이상 얽힌 복문을 피하고, 읽는 이의 인지 부하를 줄이기 위해 1~2개 절로 나눕니다.

5. **실무 개발 문서 최적화**:
   - 커밋 메시지: "~ 추가", "~ 수정", "~ 리팩토링" 등 명사형 종결 또는 간결한 개조식 적용.
   - PR 본문: 배경, 원인, 조치, 영향도를 일목요연하게 전달.
