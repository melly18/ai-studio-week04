## 1. buggy_1.py
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

---

if문을 통해 price의 값이 존재하지 않을 경우 해당 row의 연산을 수행하지 않도록 하여 에러가 발생하지 않도록 막았다. 즉, 결측치를 삭제하기로 결정한 것이다. 실제 비즈니스 환경에서는 담당자에게 확인하는 등의 조치를 취할 수 있겠으나, 테스트 데이터기 때문에 삭제를 감행했다. 다만, 만약 결측치가 지나치게 많다면 데이터 분석의 의미가 사라질 수 있기 때문에 missing_v라는 변수를 추가하여 결측치의 개수를 구했다. 이러한 코드 수정 결과 에러가 발생하지 않았고, 다음과 같은 출력 결과를 얻을 수 있었다.
```
총 매출액: 151,198,388,824원
결측치: 2개
```
결측치가 2개에 불과하기 때문에 삭제를 해도 괜찮다는 판단을 내렸으며, 따라서 이렇게 buggy_1.py의 최종 수정을 마무리했다.

## 2. buggy_2.py
**KeyError: '단가'**  
File "buggy_2.py", line 20, in summarize
```python
df["매출액"] = df["단가"] * df["수량"]
```
buggy_2.py는 dirty_sales.csv를 pandas를 이용해 dataframe으로 읽어들이는데, '단가'에 대해서 Key Error가 발생했다는 것은 column명이 잘못되었음을 의미한다. 확인을 위해
```python
print(df.columns.tolist())
```
를 csv 파일 로드 이후에 추가하였고, 그 결과
```
['date', 'product', 'category', 'price', 'quantity', 'stock']
```
와 같은 column들이 dirty_sales.csv를 이루고 있음을 알 수 있었다. 즉, '단가'라는 column이 존재하지 않아 에러가 발생한 것이며, 단가에서 에러가 발생해 넘어갔지만 바로 다음의 '수량' 또한 에러의 원인이 될 수 있음을 확인하였다.

---

'단가'와 '수량'에 맞는 column명으로 바꿔주면서 line 20을 아래와 같이 수정하였다.
```python
df["매출액"] = df["price"] * df["quantity"]
```
실행 결과, Key Error는 수정되었지만 새로운 에러가 발생하였다.

---

summarize를 완료한 이후 카테고리별 합계를 print하면 다음과 같은 결과가 출력된다.
```
category
굿즈      1500015000150001500015000150001500012000120001...
베이커리    3800380038003800380038003800380038003800380038...
원두      1800018000180001800018000180001800018000180001...
음료      4500450045004500450045004500450045004500450045...
Name: 매출액, dtype: str
```
Error가 발생하지는 않았지만, 출력 결과를 살펴보면 문제가 있음을 알 수 있다. 카테고리별 매출 합계이므로 숫자 값이어야 하는데, dtype: str이다. 즉, "price" 또는 "quantity"의 column 데이터가 str이라 제대로 된 값이 나오지 않은 것이다. 이를 확인하기 위해
```python
print(df["price"].info())
print(df["quantity"].info())
```
를 실행하면 다음과 같은 결과가 나온다.
```
<class 'pandas.Series'>
RangeIndex: 500 entries, 0 to 499
Series name: price
Non-Null Count  Dtype
--------------  -----
498 non-null    str  
dtypes: str(1)
memory usage: 4.0 KB
None
<class 'pandas.Series'>
RangeIndex: 500 entries, 0 to 499
Series name: quantity
Non-Null Count  Dtype
--------------  -----
500 non-null    int64
dtypes: int64(1)
memory usage: 4.0 KB
None
```
즉, quantity의 경우 int형이며 nan도 없지만, price의 값에 문제가 있어 에러가 발생한 것을 알 수 있다. buggy_1.py에서와 동일한 csv 파일을 사용하기 때문에 같은 에러("price"에 콤마와 '원' 포함, 결측치 2개 존재)가 존재할 것에 유의하여 코드를 수정한다.

---

summarize 함수를 다음과 같이 수정하였다.
```python
def summarize(df):
    df["price"] = pd.to_numeric(df["price"].astype(str).str.replace(",","").str.replace("원","").str.strip(), errors="coerce")
    df = df.dropna(subset=["price"])
    df["price"] = df["price"].astype("int64")
    df["매출액"] = df["price"] * df["quantity"]
    return df.groupby("category")["매출액"].sum()
```
그 결과
```
category
굿즈      150099546000
베이커리        65254500
원두         180897000
음료         841040024
Name: 매출액, dtype: int64
```
의 카테고리별 매출액 합계가 제대로 나오는 것을 확인할 수 있었다. 이에 buggy_1.py에서 구했던 총 매출액 합계와 비교해 연산이 잘 수행되었는지 확인했다. 그리고 이 때, 오류가 발생한다.

---

이번에도 명시적인 에러는 없다. 하지만 결과를 면밀히 살펴보면 이상한 점을 발견할 수 있다.
```python
print(f"총 매출액: {result.sum():,}원")
```
위 코드를 main에서 실행하면 151,186,737,524원이 나오는데, 이는 buggy_1.py에서 구한 값과 다르다. 이에 매출액의 합계를 구하는 코드를 함수 안에 넣어 결과를 확인해 보았다.
```python
print(f"총 매출액: {df["매출액"].sum():,}원")
```
그 결과는 151,198,388,824원으로 buggy_1.py의 결과값과 동일했다. 그렇다면 무엇이 문제일까?  
df["매출액"]을 구한 다음 코드에서 문제가 있을 거라 생각해 살펴보면, 카테고리별로 groupby를 한 코드임을 확인할 수 있었다. 이에 카테고리의 info를 확인해 봤는데,
```
<class 'pandas.Series'>
Index: 498 entries, 0 to 499
Series name: category
Non-Null Count  Dtype
--------------  -----
488 non-null    str  
dtypes: str(1)
memory usage: 7.8 KB
None
```
즉, 카테고리에 결측치가 존재하여 해당 row를 계산하지 못해 값에 차이가 생긴 것이다.

---

결측치가 존재하는 카테고리는 어떻게 처리하는 게 좋을까? price의 경우, 결측을 함부로 대체하기 어렵기 때문에 삭제하는 방향으로 진행했지만, 카테고리는 기타 분류로 지정하여 데이터를 보존할 수 있을 것이다. 따라서 다음과 같은 코드를 추가해 주었다.
```python
df["category"] = df["category"].fillna("미분류")
```
그 결과,
```
category
굿즈      150099546000
미분류         11651300
베이커리        65254500
원두         180897000
음료         841040024
Name: 매출액, dtype: int64
```
의 출력을 얻을 수 있었고, main의 마지막 줄에 buggy_1.py의 총액과 카테고리별 합계의 합이 일치하는지 assert 코드를 넣은 결과 assertion error 없이 잘 마무리되는 것을 확인할 수 있었다. 이렇게 buggy_2.py의 수정을 마쳤다.