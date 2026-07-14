# Hotdeal DB (FMKorea Crawler & API)

본 프로젝트는 에펨코리아(fmkorea) 핫딜 게시판의 최신 정보를 자동으로 크롤링하여, **Key-Value 기반의 JSON API** 로 제공하고 **대시보드 UI**를 통해 시각화하는 자동화 파이프라인 시스템입니다.

---

## 🌟 주요 기능

1. **자동 크롤링 (Github Actions)**
   - 하루에 1번 오전 5시(`0 20 * * *`)마다 `crawler.py` 스크립트가 실행되어 최신 핫딜 목록을 크롤링합니다.
   - 크롤링 대상: 핫딜 글번호(Key), 본문의 외부 링크들, 본문에 첨부된 이미지.
   - 크롤링된 정보는 `hotdeals.db` (SQLite)를 거쳐 `api/data.json` 형태로 지속 업데이트 및 누적됩니다.
2. **JSON API 서빙**
   - Github Pages 기능을 통해 수집된 데이터베이스를 API 형태로 배포합니다.
   - 누구나 정적 URL을 통해 `api/data.json` 데이터에 접근하여 활용할 수 있습니다.
3. **대시보드 UI 지원**
   - 수집된 핫딜 내역을 시각적으로 편리하게 확인할 수 있는 모던한 대시보드(`index.html`)가 내장되어 있습니다.

---

## 🚀 사용법 및 배포 (Github Pages 활성화)

본 시스템이 정상적으로 작동하고 대시보드를 웹에 노출하기 위해서는 **Github Pages** 설정이 필수적입니다. 프로젝트를 레포지토리에 푸시한 후 아래 단계를 따라주세요.

### 1. Github Pages 활성화 방법
1. Github Repository로 이동합니다.
2. **[Settings]** 탭을 클릭합니다.
3. 좌측 메뉴에서 **[Pages]** 를 선택합니다.
4. **Build and deployment** 섹션에서:
   - **Source**: `Deploy from a branch` 를 선택합니다.
   - **Branch**: `main` (또는 활성화된 기본 브랜치)을 선택하고 폴더는 `/ (root)` 를 선택한 뒤 **[Save]** 를 누릅니다.
5. 몇 분 내로 배포가 완료되면, 상단에 `Your site is live at https://[계정명].github.io/[레포지토리명]/` 형태의 링크가 나타납니다.
6. 해당 링크를 클릭하면 **대시보드 UI**에 접근할 수 있습니다. JSON 데이터는 `/api/data.json` 경로에서 확인 가능합니다.

### 2. 수동 수집 명령 (크롤러 수동 실행)
크롤러는 자동으로 하루에 1번 오전 5시에 동작하지만, 실시간으로 당장 업데이트를 원하실 경우 **수동 실행**이 가능합니다.

1. 대시보드 UI에 있는 **수동 수집 명령 (Github Actions)** 버튼을 클릭하거나, 레포지토리의 **[Actions]** 탭으로 직접 이동합니다.
2. 좌측 워크플로우 목록에서 `Hotdeal Crawler` 를 선택합니다.
3. 우측의 **[Run workflow]** 버튼을 클릭하여 스크립트를 즉시 실행합니다.
4. 실행이 완료되면 대시보드를 새로고침하여 최신 데이터를 확인할 수 있습니다.

---

## 📂 파일 구조 및 설명

- `crawler.py`: 핵심 파이썬 크롤링 로직. 데이터베이스(`hotdeals.db`)를 업데이트하고 `data.json`을 생성.
- `index.html`: Github Pages로 서빙되는 프론트엔드 대시보드 UI.
- `requirements.txt`: 파이썬 의존성 패키지 (`requests`, `beautifulsoup4`)
- `.github/workflows/crawler.yml`: 정기적 실행을 담당하는 Github Actions 스크립트.
- `api/data.json`: 최종적으로 배포되는 핫딜 데이터베이스의 결과물. (자동 생성됨)