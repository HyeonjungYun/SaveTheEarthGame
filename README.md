# SaveTheEarthGame

## 프로젝트 설명

### 프로젝트 기획 의도
- SaveTheEarth는 파이게임을 사용한 슈팅게임입니다.
- '오픈소스 SW개론' 강의의 과제 제출을 위해 만들어진 프로젝트입니다.
- 팀원들과의 협업이 중점인 과제였고, 깃허브를 통한 팀원들과의 협업을 해보고 배우는 것이 과제의 핵심이라고 생각하여 비교적 가볍고 쉬운 파이게임을 이용한 게임을 제작하게 되었습니다.

### 게임 설명
- 간단한 슈팅게임으로 지구를 향해 날아오는 운석을 파괴하는 게임입니다.
- 플레이어는 방향키 좌, 우를 통해 이동할 수 있으며, 스페이스바를 통해 미사일을 발사할 수 있습니다.
- 일정 시간마다 랜덤으로 생성되는 아이템을 먹어 공격력이 강해지거나 스피드가 빨라질 수 있습니다.
- 스테이지 3 마지막에 보스가 나오고 보스를 퇴치하면 게임이 끝납니다.

![upgrade_item](https://github.com/HyeonjungYun/SaveTheEarthGame/assets/58295105/8a28f440-693a-4800-b791-6d91886efbf3)

- 공격력 증가 아이템
    - 해당 아이템을 획득하면 공격력이 증가합니다. (최대 25)
    - 
![speed_item](https://github.com/HyeonjungYun/SaveTheEarthGame/assets/58295105/449c54e8-712a-402d-9257-85aa01d30337)

- 스피드 증가 아이템
    - 해당 아이템을 획득하면 스피드가 증가합니다. (최대 15)
    - 
![pierce_item](https://github.com/HyeonjungYun/SaveTheEarthGame/assets/58295105/e03dc19f-fb50-4649-b6c4-28cc2ca71ed5)

- 히트 증가 아이템
    - 해당 아이템을 획득하면 발사하는 미사일이 운석을 다단히트할 수 있으며 아이템을 먹을 때마다 다단히트 가능한 횟수가 증가합니다. (최대 5)
    - 
![heart](https://github.com/HyeonjungYun/SaveTheEarthGame/assets/58295105/e1849809-9ac6-4c98-ba5d-0d584d5e16d5)
- 라이프 추가 아이템
    - 플레이어의 라이프 카운트와 동일하게 생겼습니다.
    - 해당 아이템을 획득하면 플레이어의 라이프 카운트가 1 증가합니다. (최대 5)
- 아이템들은 각각의 최대치에 도달하면 더 이상 생성되지 않습니다.

 
![rock1](https://github.com/HyeonjungYun/SaveTheEarthGame/assets/58295105/388eee0f-6637-43ab-a1d1-a807a7e26bc1)
![rock3](https://github.com/HyeonjungYun/SaveTheEarthGame/assets/58295105/4bd40fda-a41d-4b2c-bd1c-e24f10ae69e5)
![rock2](https://github.com/HyeonjungYun/SaveTheEarthGame/assets/58295105/1e164528-c919-42cc-a44c-35ea9b35ada3)
- 운석들의 HP는 점수가 쌓일수록 점점 증가합니다.

![boss](https://github.com/HyeonjungYun/SaveTheEarthGame/assets/58295105/1d56bed2-4f1f-4ce2-b9ce-5005608d16aa)
- 게임의 최종 목표는 보스를 퇴치하는 것이며 스테이지 3에서 보스를 퇴치했을 때 게임이 클리어 됩니다.
- 보스 스테이지에서 보스를 잡지 못 하면 게임이 그대로 종료됩니다.

![boss_rock](https://github.com/HyeonjungYun/SaveTheEarthGame/assets/58295105/1ebaa1e2-d26d-45d1-b26c-a92ac2676f60)
- 보스는 위의 사진과 같은 구체를 발사하며 해당 구체는 미사일의 공격을 받지 않습니다.





## Contribute & Collaborate

### 브랜치 전략 
1. 기능 추가, 수정, 버그 픽스 등  issue가 발생한다면 issues에 issue를 추가한다.
    - 혹은 기존에 있는 issue를 보고 작업할 issue를 정한다.
3. 해당 issue의 번호에 맞게 branch를 생성한다.
  - 기능 추가시 feature-#?
  - 버그 픽스 시 fix-#?
  - 코드 구조 변경 시 refactor-#?
  - 그 외 chore-#?
3. 생성된 브랜치에서 작업을 완료 후 push
4. master 브랜치로 Pull Request
5. 팀원들과 해당 Pull Request에 대해 코드 리뷰를 진행
6. 문제가 없을 시 merge


### 커밋 메시지
- Add : 기능 추가
- Fix : 버그 수정
- Refactor : 코드 리팩토링
- Docs ; 주석 수정
- Style : 기능적 변화 없이 코드를 변경했을 때
- chore : 그 외

## 실행 방법(windows)
- 다음과 같은 방법으로 게임을 실행 가능하다.
- 명령 프롬프트를 이용하여 다음 명령어를 차례대로 입력할 수 있다.

### 1. python 및 pip 설치
- 먼저 python과 pip를 설치한다.
    - python 설치 : https://www.python.org/downloads/
    - pip 설치 문서 : https://pip.pypa.io/en/stable/installation/
- 이후 다음과 같은 명령어를 통해 설치되었는지 확인한다.
```
python -V
```
```
pip --version
``` 

### 2. 레포지토리 클론
- 해당 레포지토리를 클론하여 필요한 데이터와 파일을 원하는 디렉토리에 세팅한다.
```
git clone https://github.com/HyeonjungYun/SaveTheEarthGame.git
```

### 3. pygame 설치
- 게임 실행에 필요한 pygame 라이브러리를 다음 명령어를 통해 설치한다.
```
pip install pygame
```

### 4. SaveTheEarth.py 파일 실행
- 이후 SaveTheEarth.py 파일을 다음과 같은 명령어로 실행한다.
```
python SaveTheEarth.py
```
