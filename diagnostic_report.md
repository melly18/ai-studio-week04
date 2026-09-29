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

---

calc_total 함수를 살펴보면 csv.DictReader()로 csv파일을 읽는다. 따라서 row별로 읽기 때문에 pandas처럼 "price" column을 한 번에 바꿔버릴 수 없다. 그러므로 반복문 내에서 각 row마다 str로 읽은 price의 콤마를 없애주어야 한다.
```python
price = int(row["price"].replace(",","").strip())
```
Line 19의 코드를 위와 같이 수정해 주었다. strip()의 경우, 혹시나 존재할 수 있는 공백(추가적인 에러의 원인이 될 수 있음)을 없애기 위해 추가하였다.  
그러나 이번에는 또 다른 에러가 아래와 같이 발생했다.

---

**ValueError: invalid literal for int() with base 10: '4200원'**
File "buggy_1.py", line 19, in calc_total
```python
price = int(row["price"].replace(",","").strip())
```
이번에도 19번째 줄에서의 ValueError이다. 에러 메시지를 살펴보면 '4200원'이 문제가 되었음을 추측할 수 있는데, 이를 토대로 breakpoint의 조건식을 <"원" in row["price"]>로 바꾼 후 디버깅을 진행했다. 그 결과, dirty_sales.csv의 328행에서 price의 값이 '4200원'으로 저장되어 있다는 것을 확인할 수 있었다. 콤마의 문제는 해결했다 하더라도, "원"이라는 문자가 덧붙여져 있어 int로 변환할 수 없는 에러가 발생한 것이다.

---

콤마와 "원"을 모두 제거해 주면 숫자만 남기 때문에 price 값을 문제없이 int로 변환할 수 있을 것이다. 따라서 아래와 같이 line 19의 코드를 수정해 주었다.
```python
price = int(row["price"].replace(",","").replace("원","").strip())
```
그리고 또 다른 에러가 발생했다.

---

**ValueError: invalid literal for int() with base 10: ''**
File "buggy_1.py", line 19, in calc_total
```python
price = int(row["price"].replace(",","").replace("원","").strip())
```
이번에도 같은 줄에서의 ValueErorr이다. 에러 메시지를 살펴보면 int 변환의 parameter로 아무 값도 입력되지 않아 문제가 발생했음을 알 수 있다. dirty_sales.csv에 입력되지 않은 price가 있는지 디버거를 통해 확인했다. 별도의 breakpoint 없이 디버그를 실행해도 문제가 발생하면 멈추기 때문에, 399행의 price가 값이 저장되지 않은 상태임을 확인할 수 있었다. 즉, 결측치로 인해 int 변환에서 에러가 발생한 것이다.