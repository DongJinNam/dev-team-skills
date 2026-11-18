---
name: humanizer-kr
description: >-
  Use this skill to refine Korean documentation, commit messages, and PR descriptions into natural, professional Korean, eliminating robotic translation tone.
compatibility: Claude Code, Codex, Antigravity, Cursor
version: "1.2.0"
metadata:
  author: DongJinNam
  version: "1.2.0"
  tags: ["korean", "humanizer", "documentation"]
---

# Humanizer-KR: 자연스러운 한국어 테크니컬 라이팅

## 목적 (Purpose)

AI 특유의 번역투, 어색한 피동 표현, 과장된 챗봇 문체를 걷어내고 실무 엔지니어가 읽기 편한 간결하고 자연스러운 한국어 문장으로 교정합니다. 기술 사실과 제약 조건은 100% 보존합니다.
[English specification: SKILL.md](SKILL.md)

## 사전 요구사항 (Prerequisites)

- 운영체제: Windows, macOS, Linux
- 필수 환경: 표준 마크다운 편집 환경

## 5대 핵심 교정 원칙

1. **AI 특유의 번역투 및 피동문 걷어내기**:
   - "~할 필요가 있어 보입니다" ➔ 직관적인 행동형 명령문: "검토하십시오" / "수정합니다".
   - 이중 피동("~로 만들어지게 되어집니다")을 능동형 동사로 전면 수정합니다.
2. **명확하고 직결된 톤앤매너**:
   - 불필요한 서두나 챗봇식 과장 인사("좋은 질문입니다!", "기꺼이 도와드리겠습니다")를 전면 배제하고 결론부터 제시합니다.
3. **전문 기술 용어 보존**:
   - 함수명, 클래스명, API 필드명, 버전 번호, 영문 기술 약어는 임의로 한글화하지 않고 그대로 유지합니다.
4. **간결한 단문 위주 구성**:
   - 쉼표로 길게 늘어지는 만연체를 끊어 읽기 피로도를 낮춥니다.
5. **엔지니어링 문서 최적화**:
   - 커밋 메시지: 명확한 명령조("추가:", "수정:", "리팩터링:") 사용.
   - PR 본문: 배경, 원인, 변경점, 영향 범위를 두괄식으로 명시.

## 예시 (Examples)

```markdown
# 교정 전 (어색한 AI 번역투):
"이 설정은 시스템 관리자에 의하여 신중하게 고려되어져야만 합니다."

# 교정 후 (자연스러운 한국어):
"시스템 관리자가 이 설정을 신중하게 검토해야 합니다."
```

## 한계 및 제약 (Limitations)

- 비기술 문학 작품이나 감성적인 글쓰기 교정은 지원하지 않습니다.
- 코드 심볼, 환경 변수명, 설정 키값의 대소문자를 변경하지 않습니다.

## 문제 해결 (Troubleshooting)

- **Error**: `TerminologyAmbiguityError`
  - **Cause**: 특정 도메인 기술 용어의 한국어 번역이 확립되지 않은 경우.
  - **Solution**: 억지 번역을 피하고 영문 원어를 백틱(` `)으로 직접 표기하고 괄호 설명 추가.
- **Error**: `OverCorrectionRisk`
  - **Cause**: 문장을 다듬다가 원래 기술적 제약이나 조건문이 왜곡된 경우.
  - **Solution**: 원문과 사실 관계를 1:1 대조하여 조건/수치를 즉시 복구(fallback).
