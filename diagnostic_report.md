### 1. buggy_1.py
**FileNotFoundError: [Errno 2] No such file or directory: './Week4/dirty_sales.csv'**  
File "buggy_1.py", line 16, in calc_total
```python
with open(path, "r", encoding="utf-8") as f:
```
Traceback의 호출 경로를 더 자세히 살펴보면, buggy_1.py의 25번째 줄에서
```python
total = calc_total("./Week4/dirty_sales.csv")
```
코드를 통해 에러가 발생한 calc_total 함수를 호출한 것을 볼 수 있다. calc_total이 정의된 모습을 살펴보면 def calc_total(path): 와 같은데, 에러 코드의 path라는 변수가 "./Week4/dirty_sales.csv"라는 값을 가진다는 걸 알 수 있다. Traceback의 에러 메시지를 보면 이 path의 파일이 존재하지 않아 에러가 발생했음을 보여준다. buggy_1.py와 dirty_sales.csv가 한 파일에 존재하므로 calc_total을 호출할 때 "dirty_sales.csv"의 이름만 넘겨준다면 에러가 해결될 것이다.

---

코드 수정 이후, FileNotFoundError는 해결되었지만 이번에는 다음과 같은 새로운 에러가 발생했다.

---

**ValueError: invalid literal for int() with base 10: '5,200'**  
File "buggy_1.py", line 19, in calc_total
```python
price = int(row["price"])
```
에러 메시지를 살펴보면 "price" column의 데이터 중 ','가 포함된 값이 있어 int로 바꾸지 못했을 거라고 추측할 수 있다. Vs code의 디버거를 통해 line 19에 breakpoint를 설정하고 조건식으로 <"," in row["price"]>를 입력하여 디버깅을 실행했다. 그 결과, 'dirty_sales.csv'의 317행에서 price의 값이 '5,200'으로 콤마가 포함되어 있음을 확인할 수 있었다. 콤마가 포함된 숫자 str는 int로 바로 변환할 수 없기 때문에 에러가 발생한 것이다.