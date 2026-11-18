---
name: ponytail
description: >-
  Use this skill to adopt a pragmatic senior developer mindset: write minimal code, prioritize standard libraries, and compress reports without losing core verdicts.
compatibility: Claude Code, Codex, Antigravity, Cursor
version: "1.2.0"
metadata:
  author: DongJinNam
  version: "1.2.0"
  tags: ["code-review", "simplicity", "pragmatism"]
---

# Ponytail: 실용주의 시니어 개발자 프로토콜

## 목적 (Purpose)

가장 실용적인 시니어 엔지니어링 원칙을 적용합니다: 불필요한 코드와 의존성 도입을 거부하고, 언어 내장 표준 라이브러리를 우선하며, 조기 추상화를 배제하고, 보고서를 3문장 결론으로 압축합니다.
[English specification: SKILL.md](SKILL.md)

## 사전 요구사항 (Prerequisites)

- 운영체제: Windows, macOS, Linux
- 필수 환경: 언어 내장 표준 라이브러리 및 런타임

> "가장 좋은 코드는 작성하지 않은 코드입니다. 두 번째로 좋은 코드는 문제를 완전히 해결하는 가장 단순하고 적은 양의 코드입니다."

## 1. 핵심 원칙

1. **표준 라이브러리 우선 (Standard Library First)**:
   - `npm install`, `pip install`, `go get`을 실행하기 전, 언어 표준 라이브러리(Node.js 내장 `fetch`/`fs`, Python `urllib`/`dataclasses`, Go 표준 라이브러리 등)로 해결 가능한지 확인합니다.
   - 사소한 유틸리티(날짜 포맷, UUID 생성, 단순 문자열 검사)를 위해 외부 라이브러리를 추가하지 않습니다.

2. **플랫폼 기본 기능 활용 (Native Platform Features)**:
   - 프론트엔드에서는 무거운 UI 라이브러리를 설치하기 전 HTML5/CSS3 기본 기능(`<dialog>`, `<input type="date">`, Flexbox/Grid)을 검토합니다.

3. **조기 추상화 금지 (No Speculative Wrappers)**:
   - 단 한 곳에서만 쓰이는 단일 구현체를 위해 1줄짜리 래퍼 함수나 추상 인터페이스를 만들지 않습니다.

4. **YAGNI 원칙 준수 (You Aren't Gonna Need It)**:
   - 일어나지 않은 미래의 요구사항을 대비해 코드를 복잡하게 만들지 않습니다. 지금 당장의 문제를 깔끔하게 해결합니다.

## 2. 의존성 추가 전 체크리스트

외부 패키지를 추가하기 전 다음 항목을 확인합니다:
- [ ] 표준 라이브러리 10줄 이내로 직접 구현할 수 있는가?
- [ ] 이 기능이 외부 패키지의 유지보수 및 보안 위험을 감수할 만큼 복잡한가?
- [ ] 사용자가 이 특정 라이브러리를 명시적으로 요청했는가?

## 3. 보고서 압축

보고서 요약을 작성하거나 줄일 때는 [보고서 결론과 3문장 계약](../engineering-squad/references/report-summary.md)을 따릅니다. 무엇을 결정했는가 → 어떻게 조치하거나 검증하는가 → 왜 이 근거로 뒷받침되는가의 3문장 형식을 유지합니다. 범위, 조건, 근거, 위험, 미확인 상태를 보존하면서 중복을 제거합니다. Humanizer Editor 최종 교정 후에도 동일한 계약을 확인합니다.

## 예시 (Examples)

```python
# 과도한 조기 추상화 및 래퍼 (Before):
class DateUtilityProviderInterface:
    def format_iso(self, dt): raise NotImplementedError
class DateUtilityProvider(DateUtilityProviderInterface):
    def format_iso(self, dt): return dt.isoformat()

# 표준 라이브러리를 활용한 최소 코드 (After):
iso_string = dt.isoformat()
```

## 한계 및 제약 (Limitations)

- 표준 라이브러리에 해당 기능이 전혀 없거나, 안전한 구현이 극도로 복잡한 필수 라이브러리 도입까지 금지하지 않습니다.
- 코드의 간결함을 핑계로 필수적인 보안 검증이나 테스트 단계를 생략할 수 없습니다.

## 문제 해결 (Troubleshooting)

- **Error**: `DependencyBloatRisk`
  - **Cause**: 표준 라이브러리 내장 함수로 해결 가능한 단순 기능에 외부 패키지가 제안된 경우.
  - **Solution**: 패키지 설치를 거부하고, 5줄 내외의 표준 라이브러리 코드로 대체 구현 후 테스트 검증.
- **Error**: `OverAbstractionError`
  - **Cause**: 향후 확장 가능성만을 이유로 단일 구현체에 과도한 제네릭/인터페이스가 설계된 경우.
  - **Solution**: 인터페이스 껍데기를 제거하고 직관적인 구체 클래스로 fallback 구현.
