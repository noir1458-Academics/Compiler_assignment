# CSE 52321 컴파일러, 2025년 봄학기 학기 프로젝트

**학기 프로젝트: SLR 파서 구축**

## 1. 프로젝트 개요

이번 학기 프로젝트에서는 모호한 토이 언어(toy language)를 위한 상향식(bottom-up) $SLR(1)$ 파서를 구현합니다. 이 과제는 다음 과정을 통해 파싱 이론과 컴파일러 구현에 대한 이해를 다지는 것을 목표로 합니다:

- 문법 분석 및 모호성 검출
- 모호성 제거를 위한 문법 재정의
- $SLR(1)$ 파싱 테이블 구축
- 파스 트리 생성 및 오류 보고를 포함한 파서 구현

## 2. 프로젝트 요구사항

### 문법 재정의

아래에 모호한 문맥 자유 문법(CFG)이 제공됩니다 (3. 문법 명세 참조). 모호성을 해결하고 그 과정을 문서화하여, 재정의된 문법과 과정을 보고서에 제출하십시오.

### $SLR$ 테이블 구축

모호성이 해결된 문법의 모든 비단말 기호에 대한 FIRST 및 FOLLOW 집합을 계산하여 보고서에 제시하십시오.
$SLR(1)$ 파싱 테이블(ACTION 및 GOTO 테이블)을 구축하십시오.
보고서에는 FOLLOW 집합이 shift/reduce 또는 reduce/reduce 충돌을 해결하는 예시를 최소 하나 이상 포함하십시오.
이 웹사이트를 사용할 수 있습니다: [https://jsmachines.sourceforge.net/machines/slr.html](https://jsmachines.sourceforge.net/machines/slr.html)

### 파서 구현

Python 언어로 파서 함수를 구현하십시오 (4. 코드 지침 참조).
입력 수용 시 파스 트리를 생성하고, 거부 시에는 토큰 인덱스와 원인을 명시하는 상세 오류 보고서를 생성하십시오.

## 3. 문법 명세

다음 문맥 자유 문법(CFG)은 선언, 제어 흐름, 표현식, 함수 호출 등을 포함하는 C 유사 언어를 정의합니다. 이 문법은 의도적으로 모호하게 작성되었습니다.

1.  `Program` $\rightarrow$ `DeclList`
2.  `DeclList` $\rightarrow$ `Decl` `DeclList` | $\epsilon$
3.  `Decl` $\rightarrow$ `VarDecl` | `FuncDecl`
4.  `VarDecl` $\rightarrow$ `type` `id` `;`
5.  `VarDecl` $\rightarrow$ `type` `id` `=` `Expr` `;`
6.  `FuncDecl` $\rightarrow$ `type` `id` `(` `ParamList` `)` `Block`
7.  `ParamList` $\rightarrow$ `Param` `,` `ParamList` | `Param` | $\epsilon$
8.  `Param` $\rightarrow$ `type` `id`
9.  `Block` $\rightarrow$ `{` `StmtList` `}`
10. `StmtList` $\rightarrow$ `Stmt` `StmtList` | $\epsilon$
11. `Stmt` $\rightarrow$ `if` `(` `Expr` `)` `Stmt`
12. `Stmt` $\rightarrow$ `if` `(` `Expr` `)` `Stmt` `else` `Stmt`
13. `Stmt` $\rightarrow$ `while` `(` `Expr` `)` `Stmt`
14. `Stmt` $\rightarrow$ `for` `(` `Expr` `;` `Expr` `;` `Expr` `)` `Stmt`
15. `Stmt` $\rightarrow$ `return` `Expr` `;`
16. `Stmt` $\rightarrow$ `VarDecl`
17. `Stmt` $\rightarrow$ `ExprStmt`
18. `Stmt` $\rightarrow$ `Block`
19. `ExprStmt` $\rightarrow$ `id` `=` `Expr` `;`
20. `Expr` $\rightarrow$ `Expr` `==` `Expr`
21. `Expr` $\rightarrow$ `Expr` `+` `Expr`
22. `Expr` $\rightarrow$ `Expr` `*` `Expr`
23. `Expr` $\rightarrow$ `-` `Expr`
24. `Expr` $\rightarrow$ `id` `(` `ArgList` `)`
25. `Expr` $\rightarrow$ `id`
26. `Expr` $\rightarrow$ `num`
27. `Expr` $\rightarrow$ `(` `Expr` `)`
28. `ArgList` $\rightarrow$ `Expr` `,` `ArgList` | `Expr` | $\epsilon$

대문자로 시작하는 모든 토큰(예: `Program`, `DeclList`, `Expr`)은 비단말 기호입니다. 그 외 모든 토큰(예: `id`, `num`, `or`, `==`, `(`, `;` 등)은 단말 기호입니다. 각 생성 규칙의 기호 사이 공백은 서식용으로 사용되었습니다.

## 4. 코드 지침

파서를 실행하기 위해 제공된 Python 코드 구조를 사용해야 합니다.
다음 두 개의 Python 파일이 제공됩니다:

- `main.py`: 프로그램의 주 진입점 (이 파일은 수정하지 마십시오)
- `parser.py`: `parser()` 함수 및 지원 클래스나 함수를 구현할 파일

주 진입점은 `main.py`입니다. 이 파일은 토큰 입력 파일을 읽고, `parser.py`에 있는 여러분의 `parser()` 함수를 호출한 후 결과를 출력합니다.
중요: Python 표준 라이브러리만 사용해야 합니다. 외부 패키지는 사용하지 마십시오.

## 5. 팀 구성

최대 2명까지 팀을 구성할 수 있습니다. 팀 구성을 원할 경우, 제공된 구글 폼 링크([https://forms.gle/d2tqbjtNzFbzKdWY6](https://forms.gle/d2tqbjtNzFbzKdWY6))를 사용하여 5월 16일 (금) 23:59까지 팀 정보를 제출하십시오. (주의: 2025년 5월 18일 현재, 이 마감일은 이미 지났습니다.)

다음 옵션 중 하나를 선택할 수 있습니다:

- 개인 작업
- 원하는 파트너와 2인 팀 구성
  : 이 경우, 팀원 중 한 명만 구글 폼을 작성하면 됩니다.
- 무작위로 매칭되는 2인 팀 합류
  : 학생 수가 홀수일 경우, 일부 학생은 추첨을 통해 개인 작업을 하게 될 수 있습니다.

5월 16일까지 팀 선호도를 제출하지 않으면 예외 없이 자동으로 개인 작업으로 배정됩니다.
최종 팀 목록 및 팀 ID 배정은 5월 19일 (월)에 공지될 예정입니다.

## 6. 제출 마감일 및 제출물

마감일: 5월 31일 (토) 23:59 (E-class 시스템을 통해 제출)
제출 지연 시, 1일당 점수의 0.1배가 감점됩니다.

**제출물 1.**
`team_<teamID>.zip`이라는 이름의 압축 코드 파일, 내용물:
(아래 제출물 파일명을 변경하지 마십시오)

- `main.py` (제공된 진입점 파일, 수정하지 않음)
- `parser.py` (여러분의 구현 내용)

**제출물 2.**
`team_<teamID>_report.pdf`, 포함해야 할 내용:

- 문법 모호성 해결 과정에 대한 명확한 설명 및 완전한 형태의 재정의된 문법
- 모든 비단말 기호에 대한 FIRST 및 FOLLOW 집합
- $SLR(1)$ 파싱 테이블 (ACTION 및 GOTO)
- FOLLOW 집합이 테이블 내 충돌을 해결하는 최소 하나의 예시
- 여러 코드 실행 결과 예시: 자체 테스트 토큰 스트림과 그에 해당하는 파스 트리 또는 오류 보고서
- 보고서는 영어 또는 한국어로 작성할 수 있습니다.

문법이나 프로젝트 설명에 오류를 발견하면, 이메일(hsmoon@cau.ac.kr)로 교수님께 문의하십시오.

보고서 또는 코드 표절 시 사유를 불문하고 자동으로 F 학점을 받게 됩니다. ChatGPT와 같은 도구를 참고용으로 사용할 수는 있지만, 생성된 내용을 그대로 복사하여 제출하지 마십시오. 이는 제출물 간 높은 유사도를 유발할 수 있으며, 표절 행위로 간주될 것입니다.
