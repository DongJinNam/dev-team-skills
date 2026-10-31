# 보안 역할의 조사·선정 근거

확인일: 2026-10-31. Planner는 기술 적합성과 사고 교훈을 조사하고 Marketing은 채택 지표·주장 범위·출처를 교차 확인한다. 이 문서는 전체 시장 순위가 아닌 조사 후보의 비교다. 재사용 시 지표·원문 변경을 확인한다.

## 공개 스킬 후보와 조합

| 후보 / 원문 | 공개 채택 지표 | 참고할 역량 | 채택 한계 |
| :--- | :--- | :--- | :--- |
| [Sentry security-review](https://github.com/getsentry/skills/blob/main/skills/security-review/SKILL.md) | [skills.sh](https://www.skills.sh/getsentry/skills/security-review) 21.8K installs; 저장소 약 1.1K stars | 공격자 입력·프레임워크 보호·증거 확신도 확인 | 인증 필요 경로 제외 규칙은 채택하지 않는다. 로그인 사용자 간 IDOR도 검사한다. |
| [Trail of Bits differential-review](https://github.com/trailofbits/skills/blob/main/plugins/differential-review/skills/differential-review/SKILL.md) | [skills.sh](https://www.skills.sh/trailofbits/skills/differential-review) 9.3K installs | 변경분과 호출 경로·이력·영향 범위 확인 | 변경 줄 밖의 개인정보 경계까지 확인한다. |
| [Trail of Bits insecure-defaults](https://www.skills.sh/trailofbits/skills/insecure-defaults) | 해당 카탈로그 6.5K installs; [저장소](https://github.com/trailofbits/skills) 약 7.9K stars | 설정 누락 시 fail-open·약한 기본값 검사 | 예시 패턴만으로 취약점을 단정하지 않고 실제 설정·실행 경로를 확인한다. |

설치수는 카탈로그가 표시한 누적 지표이며 고유 사용자 수·효과·안전성 측정값이 아니다. 저장소 stars는 개별 스킬의 인기가 아니다. 카탈로그 감사 배지는 판정이 상충할 수 있어 승인 근거로 사용하지 않는다. Sentry에는 Socket Fail, insecure-defaults에는 Snyk Fail 표시가 관측됐다. 이는 악성 확정도 아니며, 인기만 보고 자동 설치하지 않는 이유다.

[OWASP ASVS 5.0.0](https://asvs.owasp.org/)을 검증 범위의 기준으로 참고한다(발행 2025-05-30). 세 스킬의 검토 관점을 자체 계약인 [security-review.md](./security-review.md)에 조합한다. 외부 파일·스크립트를 복제하거나 자동 설치하지 않으며 실행 의존성도 추가하지 않는다. 향후 코드/본문을 가져오면 revision과 파일별 라이선스·고지 요건을 별도 확인한다. 관측된 저장소 라이선스: [Sentry Apache-2.0](https://github.com/getsentry/skills/blob/main/LICENSE), [Trail of Bits CC-BY-SA-4.0](https://github.com/trailofbits/skills/blob/main/LICENSE).

## 최근 개인정보 사고에서 도출한 검수 범위

| 공식 발표 / 사건 시기 | 확인된 사실 | 이번 역할에 반영한 판단 |
| :--- | :--- | :--- |
| [개인정보위 GS리테일 발표](https://m.korea.kr/briefing/pressReleaseView.do?newsId=156776142), 2026-08-31 / GS SHOP 2024-06-21~2025-02-13, GS25 2024-12-26~2025-01-04 | 크리덴셜 스터핑으로 로그인 후 회원정보가 유출됐다. 이상징후 탐지·차단 및 보호 조직 운영 미흡이 확인됐다. | 로그인 성공과 기능 QA만으로 보호를 입증할 수 없다. 로그인 남용·이상징후 대응과 독립 책임을 검수한다. |
| [개인정보위 보람상조 발표](https://pipc.go.kr/np/cop/bbs/selectBoardArticle.do?bbsId=BS074&mCode=&nttId=12066), 2026-05-14 / 유출 신고 2024-05-28 | SQL 인젝션으로 고객정보가 탈취됐고 접근제어·위수탁 감독·보유기간 경과 정보 파기가 미흡했다. | 입력 검증뿐 아니라 DB 권한, 위탁 흐름, 보관·파기까지 검사한다. |

발표일을 사고 발생일로 혼동하지 않는다. 위 사례가 특정 스킬로 사고를 예방할 수 있었다는 인과를 입증하지는 않는다. **기능 테스트만으로 개인정보 보호를 입증할 수 없으므로 보안 검수를 출시 선행조건으로 둔다**는 것이 이 설계의 판단이다. 보안 PASS는 검수 범위의 증거이며 완전한 무취약점·법적 인증을 의미하지 않는다.
