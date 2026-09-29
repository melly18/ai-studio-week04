## 1. buggy_1.py
AI 미사용

## 2. buggy_2.py
AI 미사용

**수정한 코드를 AI에게 설명을 요구하였다.**
*구조는 3번과 동일하다*

csv 매출 집계에 대해 카테고리별 매출 집계를 도출하는 스크립트이다. KeyError가 발생해 이를 수정하였고, 결측치 제거 등 데이터 정제를 통해 코드를 개선했다.
import pandas as pd

def load(path):
    df = pd.read_csv(path, encoding="utf-8")
    return df

def summarize(df):
    # 단가 x 수량으로 매출액 컬럼을 만든 뒤 카테고리별 합계를 낸다
    df["price"] = pd.to_numeric(df["price"].astype(str).str.replace(",","").str.replace("원","").str.strip(), errors="coerce")  #FIXED: price에서 콤마와 "원"을 제거하고 숫자로 변환
    df = df.dropna(subset=["price"])  #FIXED: df에서 price가 결측치인 row 삭제
    df["price"] = df["price"].astype("int64")  #FIXED: price가 int형이 되도록 변환
    df["매출액"] = df["price"] * df["quantity"]    #FIXED: 잘못된 column명 수정
    df["category"] = df["category"].fillna("미분류")  #FIXED: 결측치 카테고리를 '미분류'로 지정
    return df.groupby("category")["매출액"].sum()

if __name__ == "__main__":
    df = load("dirty_sales.csv")
    result = summarize(df)
    print(result)
    assert result.sum() == 151198388824
이 코드에 대해 자세히 설명하도록.

---

*자세히 설명하라고 요구했더니 지나치게 자세한 답변이 나와 최대한 중요 부분만 요약함.*

이 코드는 csv 형태의 매출 데이터를 불러온 뒤, 데이터 정제 과정을 거쳐 카테고리별 총 매출액을 집계하는 Python 프로그램이다. 특히 원본 데이터에 존재할 수 있는 가격 형식 오류, 결측치, 잘못된 컬럼명 문제(KeyError) 등을 처리하도록 수정된 코드이다.

코드 흐름을 데이터 불러오기 -> 데이터 정제 -> 매출액 계산 -> 카테고리별 집계 -> 결과 검증 순서로 설명하겠다.

1. 전체적인 코드의 목적  
이 코드가 수행하는 작업을 한 문장으로 정리하면 다음과 같다.
    dirty_sales.csv 파일에서 상품의 단가(price)와 수량(quantity)을 이용해 매출액을 계산하고, 상품의 category별로 매출액을 합산한다.

전체적인 데이터 처리 흐름은 다음과 같다.

```
dirty_sales.csv
      ↓
CSV 데이터 불러오기
      ↓
price 데이터 정제
      ↓
price 결측치가 있는 행 제거
      ↓
price를 정수형으로 변환
      ↓
매출액 = price × quantity 계산
      ↓
category 결측치를 "미분류"로 처리
      ↓
category별 매출액 합계
      ↓
결과 출력
      ↓
전체 매출액 검증
```

2. 데이터 불러오기  
load(path) 함수를 통해 pd.read_csv로 csv 파일을 읽어낸다. 그리고 읽어낸 DataFrame을 호출한 곳으로 반환한다. main에서 df = load("dirty_sales.csv") line이 함수를 호출하고, df에 csv 파일 전체 데이터가 들어간다.

3. 데이터 정제  
3, 4, 5번은 모두 summarize(df) 함수에서 일어난다. load()에서 불러온 DataFrame을 parameter로 받아서 다양한 작업을 처리한다.  
먼저 price 데이터를 정제한다. 가격 데이터를 계산할 수 있는 숫자 형태로 변환하는 과정으로, price를 문자열로 변환한 후 콤마와 "원", 공백을 제거하고 숫자로 변환한다. 이 때, errors="coerce"로 인해 오류값은 NaN으로 변환된다.  
이후, 변환된 price에서 결측치 NaN 행을 제거한다. 정제가 완료된 price를 정수형으로 명시적으로 변환한다. 가격이 원 단위이고 소수점이 필요하지 않다는 전제에서 정수형으로 변환한 것이다.  
매출액 계산 다음에 또 다른 데이터 정제가 있다. 바로 category의 결측치를 처리하는 것이다. NaN 행을 그대로 groupby()하면 결측 카테고리를 별도의 그룹으로 명시적으로 관리하기 어렵다. 따라서 '미분류'라는 그룹으로 관리하면서 카테고리 정보가 없는 매출 데이터도 집계에 포함시킨다.

4. 매출액 계산  
각 상품의 매출액을 단가 x 판매 수량으로 계산한다.

5. 카테고리별 집계  
groupby를 통해 category별로 데이터를 그룹화한 후, 매출액의 sum을 통해 각 그룹의 매출액을 합산한다. 즉, 상품 하나하나의 매출액을 계산한 후 같은 카테고리에 속한 상품들의 매출액을 모두 더하는 것이다.

6. 결과 검증  
main에서 summarize 함수 호출을 통해 얻은 최종 집계를 출력한다. 이후 assert를 이용해 프로그램의 결과가 예상한 조건을 만족하는지 검증한다. 여기서는 모든 카테고리의 매출액을 다시 합산하여 그 값이 올바른지 확인한다.

전체 코드를 단계별로 해석하면 결국 다음과 같은 논리이다.

```
# 1. CSV 읽기
df = load("dirty_sales.csv")

# 2. 가격 정제
price에서 콤마와 '원' 제거
        ↓
문자열을 숫자로 변환
        ↓
변환 불가능한 값은 NaN
        ↓
price가 NaN인 행 제거
        ↓
price를 정수형으로 변환

# 3. 매출액 계산
매출액 = 가격 × 수량

# 4. 카테고리 정제
category가 비어 있으면 "미분류"

# 5. 집계
category별로 매출액을 모두 더함

# 6. 결과 검증
모든 카테고리의 합계가
151,198,388,824인지 확인
```

한 가지 주의할 점은 현재 코드에서는 price에 대해서는 결측치와 문자열 형식을 정제하지만, quantity에 대한 데이터 검증은 별도로 하지 않는다. 따라서 데이터 품질을 더 엄격하게 관리하려면 quantity 역시 숫자로 변환하고 결측치나 비정상적인 값을 처리하는 과정이 필요할 수 있다.  
또한 price를 무조건 int64로 변환하는 것은 가격에 소수점이 존재하지 않는다는 전제가 있을 때 적절하다.

**정리**  
이 코드는 단순한 groupby() 집계 코드라기보다는 ETL에 가까운 데이터 처리 과정을 포함하고 있다.

E(Extract)  
-> pd.read_csv()로 CSV에서 데이터를 추출

T(Transform)  
-> price의 ',', '원', 공백 등을 제거  
-> 숫자형으로 변환  
-> 결측 가격 제거  
-> 매출액 계산  
-> 결측 category를 '미분류'로 변환

L(Load/Output)  
-> groupby()로 카테고리별 매출액을 집계하고 결과 출력

그리고 마지막의 assert를 통해 데이터 정제와 집계 이후의 최종 결과가 기대한 전체 매출액과 일치하는지 검증하고 있다.

>스크립트를 입력할 때, 간단한 상황 설명과 발생했던 에러들을 알려주고, 코드에 주석으로 FIXED 처리가 되어있다 보니 AI가 주어진 코드를 매우 훌륭하게 설명해 주었다. 지나치게 자세하게 설명해 주어 요약하다 보니 누락된 부분들이 일부 있는데, 그것들을 포함해서 살펴보면 AI가 코드의 의도와 수정된 이유 등을 모두 잘 파악했음을 알 수 있었다. 그렇게 길거나 복잡한 코드가 아니기 때문에 정확하게 코드를 잘 분석했다.

## 3. buggy_3.py
*무료 Chat GPT와 대화를 진행했다.*
**AI와의 대화에서 프롬프트와 AI의 답변 요지를 가로선으로 구분하고, 채택/기각 판단과 이유, 검증 결과는 들여쓰기로 나타낸다.**

csv 매출 데이터를 읽어 카테고리별 매출 합계를 구하는 파이썬 스크립트다.
def load_and_clean(path):
    df = pd.read_csv(path, encoding="utf-8")
    df["price"] = (df["price"].astype(str).str.replace(",", "").str.replace("원", "").str.strip())
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["revenue"] = df["price"] * df["quantity"]

df = load_and_clean("dirty_sales.csv")
result = df.groupby("category")["revenue"].sum()

전체 스크립트의 일부이다. 마지막 줄에서 아래 첨부한 AttributeError가 발생한다.

Traceback (most recent call last): 
  File "C:\Users\melli\Downloads\ai_studio\Week04\buggy_3.py", line 33, in <module> 
    main() 
    ~~~~^^ 
  File "C:\Users\melli\Downloads\ai_studio\Week04\buggy_3.py", line 29, in main 
    result = df.groupby("category")["revenue"].sum() 
             ^^^^^^^^^^ 
AttributeError: 'NoneType' object has no attribute 'groupby'

print(type(df))로 확인 결과, main의 df가 NoneType임을 알 수 있었다. 그 윗줄을 보면 알 수 있듯, df는 load_and_clean의 함수 호출 결과를 return받는다. 이에 load_and_clean을 살펴보면 return이 없음을 알 수 있다. 즉, return받는 값이 없어 df가 pandas.dataframe을 할당받지 못한 것으로 추정된다.

에러가 발생하는 원인을 설명하고, 내 가설이 맞는지 확인할 수 있는 검증 코드를 알려줘. 수정은 다음 프롬프트로 진행하도록 할게.

---

가설이 맞다. load_and_clean 함수에서 return값이 없어 df에 None이 할당된다. main의 함수 호출 코드 다음 줄에 아래 코드를 삽입하면
```python
print(type(df))
print(df is None)
```
함수의 반환값이 None임을 확인할 수 있다. 만약 함수의 내부에서 DataFrame이 정상적으로 생성되었는지도 함께 확인하고 싶다면 load_and_clean의 마지막에 아래 코드를 추가한다.
```python
print(type(df))
print(isinstance(df, pd.DataFrame))
```
이를 통해 함수 내부에서 DataFrame이 정상적으로 존재하는 것과 함수 호출 결과 반환 값이 None인 것을 함께 확인할 수 있다.

>이미 main에서 df의 type이 None인 것을 문제 진단 과정에서 확인했기 때문에 AI의 답변을 채택하지 않았다. 또, 함수 내부에서 DataFrame의 존재를 확인하는 것은 불필요한 행위라고 판단해 이 또한 채택하지 않았다. AI의 답변으로 인해 코드를 수정하지 않았으므로 검증 결과 기록은 생략한다.

함수 외부에서 df가 NoneType인 것을 확인했어. 이제 코드를 수정해 보자. 함수 내부에서 df의 info는 다음과 같아.
<class 'pandas.DataFrame'>  
RangeIndex: 500 entries, 0 to 499  
Data columns (total 6 columns):  
 \#   Column    Non-Null Count  Dtype  
---  ------    --------------  -----  
 0   date      500 non-null    str    
 1   product   500 non-null    str    
 2   category  490 non-null    str    
 3   price     498 non-null    str    
 4   quantity  500 non-null    int64  
 5   stock     485 non-null    float64
dtypes: float64(1), int64(1), str(4)
memory usage: 23.6 KB
None  
이 정보를 바탕으로 스크립트를 수정해줘.

---

load_and_clean이 df를 return하도록 수정해야 한다. 또한 price에 결측값이 2개 있고, category에도 결측값이 10개 있으므로, 현재 코드를 그대로 사용한다면 revenue가 NaN이 된다. 따라서 다음과 같이 코드를 수정해라.
```python
def load_and_clean(path):
    df = pd.read_csv(path, encoding="utf-8")

    df["price"] = (
        df["price"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("원", "", regex=False)
        .str.strip()
    )

    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["revenue"] = df["price"] * df["quantity"]

    return df


df = load_and_clean("dirty_sales.csv")
result = df.groupby("category")["revenue"].sum()

print(result)
```
왜 return df가 필요한가? 함수 내부의 df와 함수 외부의 df는 같은 이름을 사용하더라도 별개의 변수이기 때문이다. 따라서 return해야만 dataframe을 외부로 전달할 수 있다.  
이번 수정에서는 핵심 버그인 return df를 해결했고, price와 category의 결측값을 어떻게 처리할지는 매출 데이터의 요구사항에 따라 다음 단계에서 결정하면 된다.

>AI가 제공한 수정된 코드를 살펴보면 price를 숫자로 정제하는 과정에서 regex=False가 추가되었고, 핵심 오류를 수정하기 위해 return df가 함수의 마지막 줄에 추가되었다. regex=False가 굳이 필요한 상황이 아닌 듯하여 이 부분은 반영하지 않았고, return이 필요한 것은 맞으므로 return df 부분은 채택하였다.

>>수정한 코드를 실행해 보면, 이제 AttributError는 발생하지 않고 값이 출력됨을 볼 수 있다.
>>```
>>category
>>굿즈      1.500995e+11
>>베이커리    6.525450e+07
>>원두      1.808970e+08
>>음료      8.410400e+08
>>Name: revenue, dtype: float64
>>```
>>제대로 수정된 것 같아 보이지만, buggy_2.py를 수정하면서 알 수 있었듯이 price와 category의 결측치에 대한 조치가 필요하다.

price의 결측치는 drop하고, category의 결측치는 "미분류"로 지정해줘. 또, price를 int형으로 변환하여 revenue가 int값이 되도록 수정해줘.

---

좋다. 처리 순서를 가격 문자열 정리 -> 숫자 변환 -> 가격 결측 행 제거 -> category 결측값 '미분류'로 대체 -> price를 정수형으로 변환 -> revenue 계산 -> df 반환 으로 잡는 게 안전하다.

```python
def load_and_clean(path):
    df = pd.read_csv(path, encoding="utf-8")

    # price에서 쉼표와 '원' 제거
    df["price"] = (
        df["price"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("원", "", regex=False)
        .str.strip()
    )

    # 숫자로 변환할 수 없는 값은 NaN으로 처리
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    # price가 결측치인 행 제거
    df = df.dropna(subset=["price"])

    # category의 결측치는 '미분류'로 지정
    df["category"] = df["category"].fillna("미분류")

    # price를 정수형으로 변환
    df["price"] = df["price"].astype(int)

    # 매출 계산
    df["revenue"] = df["price"] * df["quantity"]

    return df


df = load_and_clean("dirty_sales.csv")
result = df.groupby("category")["revenue"].sum()

print(result)
```
dropna를 통해 결측 행 2개를 제거한다. 이후 price의 int 변환에서 NaN 때문에 발생할 오류를 방지할 수 있다.  
category의 결측치는 행을 삭제하지 않고 '미분류'라는 새로운 카테고리를 부여한다.  
그리고 price를 int로 변환하면 quantity가 int64이므로 revenue 또한 정수형이 된다.  
마지막으로 return df를 통해 함수 외부에서 groupby가 정상적으로 실행된다.

>수정을 요청한 부분만 코드들이 추가되었고, 나머지는 변경 사항이 없이 코드가 안전하게 완성되었다. buggy_2.py에서 비슷한 과정을 수행했기 때문에 gpt가 제공한 코드가 원하는 결과를 도출할 것을 알 수 있다. 실제로 buggy_2.py와 비교하면 astype(int) 부분을 제외하곤(buggy_2.py는  astype("int64") 코드를 사용) 동일한 흐름임을 알 수 있다. 따라서 최종 수정 코드로 ai 생성 코드를 채택했다. 물론 regex=False는 앞서 판단했듯 불필요하다고 여겨 그 부분만 배제했다.

>>수정 결과, 별다른 에러 없이 잘 작동함을 확인할 수 있었다.
>>```
>>category
>>굿즈      150099546000
>>미분류         11651300
>>베이커리        65254500
>>원두         180897000
>>음료         841040024
>>Name: revenue, dtype: int64
>>```
>>제대로 되어 보이지만 실제로는 잘못된 값일 수 있으므로, category별 매출액 합계의 sum을 구해 buggy_1.py의 값과 같은지 assert 코드를 추가했다.
>>실행 결과, AssertionError가 발생하지 않았으므로 제대로 된 데이터 분석이 일어났음을 알 수 있다. 따라서 이상으로 buggy_3.py의 수정을 마무리한다.

## 4. buggy_4.py
AI 미사용

## 5. buggy_5.py
**조건은 3번과 동일하다.**

다음은 csv 매출 데이터를 읽어 앞 행 대비 가격 변화가 큰 행을 찾는 스크립트 속 한 함수이다.
def find_big_jumps(prices, threshold=100000):
    jumps = []
    for i in range(len(prices)):
        diff = prices[i + 1] - prices[i]
        if abs(diff) >= threshold:
            jumps.append((i, prices[i], prices[i + 1], diff))
    return jumps

이 코드의 4번째 줄에서 아래와 같은 에러가 발생했다.

Traceback (most recent call last): 
  File "c:\Users\melli\Downloads\ai_studio\Week04\buggy_5.py", line 36, in <module> 
    jumps = find_big_jumps(prices) 
  File "c:\Users\melli\Downloads\ai_studio\Week04\buggy_5.py", line 29, in find_big_jumps 
    diff = prices[i + 1] - prices[i]  
           ~~~~~~^^^^^^^ 
IndexError: list index out of range

디버거를 통해 i=499일 때 오류가 발생함을 알아냈다. 반복문이 0부터 len(prices)-1까지 돌고, price리스트의 인덱스 또한 0부터 len(prices)-1까지 있는데 i + 1로 존재하지 않는 인덱스에 접근을 시도해 에러가 난 것으로 파악했다.
이 오류의 원인을 설명하고, 내 가설이 맞는지 검증하는 코드를 제안하도록. 수정은 다음 프롬프트에서 진행하도록 하겠다.

---

가설이 정확하다. 오류의 직접적인 원인은 i + 1이 prices의 유효한 인덱스 범위를 벗어나기 때문이다. 가설을 검증하기 위해서는 문제가 되는 코드 앞줄에 아래 코드를 추가하면 된다.
```python
print(f"i={i}, i+1={i+1}, len(prices)={len(prices)}")
```
이 함수를 실행하면 마지막 부분에서 아래와 같은 결과를 얻을 수 있을 것이다.
```
i=497, i+1=498, len(prices)=500
i=498, i+1=499, len(prices)=500
i=499, i+1=500, len(prices)=500
IndexError: list index out of range
```
따라서 현재 코드의 문제는 prices[i] 자체가 아니라 prices[i + 1]에 접근하는 시점에서 발생하며, 특히 마지막 인덱스인 i = len(prices) - 1에서 반드시 문제가 발생하는 구조이다.

>디버거로 확인하고 내린 결론과 AI의 답변이 동일하기 때문에 별도의 확인 없이 바로 코드 수정으로 넘어가도록 하겠다.

이제 수정을 해 보자. 마지막 i를 제외하면 모두 에러 없이 잘 돌아가니, 그 부분만 신경쓰면 될 거야. 가능한 수정은 두 가지 정도 있다고 생각해. 앞 행과의 비교이니 순환해서 맨 처음 것과 비교하기, 또는 어차피 이전 행에서 변화 폭을 측정해 갔기 때문에 마지막 행은 체크하지 않아도 된다는 것. 각 버전의 코드를 작성하고 각각의 장단점을 분석해줘.

---

그렇다. 이 경우의 핵심은 마지막 행에서는 i + 1에 해당하는 다음 행이 존재하지 않는 것을 어떻게 처리할지이다.
1. 마지막에서 처음으로 순환하여 비교
리스트의 마지막 가격과 첫 번째 가격을 비교하도록 하는 방법이다.  
prices[i + 1] 대신 prices[(i + 1) % len(prices)]를 사용하여 다른 행에서는 이전과 동일하고 마지막 행에서는 첫 번째 행을 가리키도록 한다.  

장점으로는 인덱스 오류가 발생하지 않으며, 마지막 행도 비교 대상에 포함된다는 점이 있다. 데이터가 시간 순환형이거나, 마지막과 처음이 논리적으로 연결되는 데이터에 적합하다.  
단점은 원래 데이터의 의미가 바뀔 수 있다는 것이다. 만약 시간 순서로 정렬된 매출 데이터라면 새로운 비교 관계를 임의로 만드는 것이 된다. 그러므로 마지막과 처음이 연결되었는지가 중요하다.

2. 마지막 행은 비교하지 않기
반복문에서 range(len(prices))를 range(len(prices)-1)로 바꾸어 마지막 행을 반복 대상에서 제외하는 방법이다.

장점으로는 수정이 매우 간단하고 원래 코드의 의도와 가장 자연스럽게 연결된다. 또, 마지막 행에 존재하지 않는 다음 행을 억지로 만들어 비교하지 않으며, 순서가 중요한 데이터에서 의미가 바뀌는 문제가 생기지 않는다.  
단점으로는 마지막 행 자체를 기준으로 하는 변화량은 계산하지 않으므로 총 len(prices) - 1 개의 비교만 수행한다.

이 문제에서는 특별히 데이터가 순환한다는 조건이 없다면 2번 방법이 더 자연스럽다.

>dirty_sales.csv 파일의 date를 살펴보면 순서대로 정렬이 되어있지 않음을 확인할 수 있다. 즉, AI의 제안과는 파일의 구조가 다르기 때문에 오히려 1번 방법이 적절하다고 판단된다. 정렬되어 있지 않기 때문에 모든 데이터를 비교해 주는 것이 데이터 분석에 더 도움이 될 수 있기 때문이다. 따라서 1번 방법을 채택하였다. 코드 자체는 별도의 if문 사용 없이 간편하게 수정할 수 있으므로 ai의 제안을 받아들였다.

>>코드를 수정한 후 실행하면 index error가 사라지고 정상 출력이 진행됨을 확인할 수 있다. 결과는 다음과 같다.
>>```
>>급변 지점 2건
>>(249, 21000.0, 9999999.0, 9978999.0)
>>(250, 9999999.0, 3500.0, -9996499.0)
>>```
>>다만 앞서 buggy_4.py의 수정을 통해 알게 된 이상치는 총 2건이었는데(음수값과 지나치게 큰 값), 한 건만 발견할 수 있는 것이 부족하다고 여겨 추가 수정을 진행했다.

데이터가 시간순으로 정렬되어 있지 않아서 1번 방식을 선택했어. 이제 오류는 나지 않지만, 이 데이터 파일에 존재하는 이상치 2개 중 하나만 발견할 수 있기 때문에 이 점을 수정하고 싶어. 지나치게 큰 값도 물론 중요하지만 가격 리스트에서 음수값도 중요하니까. 내가 생각하기론 if문에 음수 조건문을 달아주면 될 것 같긴 한데. 다른 제안이 있다면 코드를 제안하고 내 가설과의 장단점을 분석해줘.

---

그 방향이 맞다. 다만 현재 코드를 보면 이미 변화량의 부호와 관계없이 큰 변화폭을 찾고 있다. 따라서 주의해야 할 점은 "가격 자체가 음수인 것"과 "가격 변화량이 음수인 것"이 서로 다른 조건이라는 것이다. 현재 코드는 변화량이 크다면 음수 변화도 발견할 수 있다. 하지만 큰 변화폭이 아니더라도 현재 가격 자체가 음수라는 이상치를 찾고 싶다면 별도의 조건이 필요하다.

1. 생각한 방식: if에 음수 조건 추가
```python
def find_big_jumps(prices, threshold=100000):
    jumps = []
    for i in range(len(prices)):
        next_i = (i + 1) % len(prices)
        diff = prices[next_i] - prices[i]
        if abs(diff) >= threshold or prices[next_i] < 0:
            jumps.append((i, prices[i], prices[next_i], diff))
    return jumps
```
이렇게 하면 기존 조건은 그대로 유지하면서 다음 행의 가격 자체가 음수인 경우도 찾아낸다.  
다만 한 가지 문제가 있는데, 현재 행이 음수인 경우가 빠질 수 있다.

2. 더 적절한 방법: 두 가격 모두 검사
인접한 두 행을 비교하는 함수라면 두 가격 중 어느 하나라도 음수인지 검사하는 것이 더 안전하다.
```python
def find_big_jumps(prices, threshold=100000):
    jumps = []
    for i in range(len(prices)):
        next_i = (i + 1) % len(prices)
        diff = prices[next_i] - prices[i]
        if abs(diff) >= threshold or prices[i] < 0 or prices[next_i] < 0:
            jumps.append((i, prices[i], prices[next_i], diff))
    return jumps
```
이렇게 하면 큰 가격 변화와 음수 가격이라는 두 종류의 이상치를 모두 탐지할 수 있다.

3. AI가 더 추천하는 방법: 이상치 조건을 분리하기
위 코드는 작동하지만, 앞으로 이상치 종류가 늘어난다면 if문이 점점 복잡해질 수 있다. 그래서 조건을 변수로 분리하는 방법도 좋다.
```python
def find_big_jumps(prices, threshold=100000):
    jumps = []
    for i in range(len(prices)):
        next_i = (i + 1) % len(prices)
        diff = prices[next_i] - prices[i]
        big_jump = abs(diff) >= threshold
        negative_price = prices[i] < 0 or prices[next_i] < 0
        if big_jump or negative_price:
            jumps.append((i, prices[i], prices[next_i], diff))
    return jumps
```
이 방식의 장점은 무엇 때문에 해당 행이 이상치로 판정됐는지 나중에 확인하기 쉽다. 또, 이후에 다양한 조건을 추가하기도 편리하다.

현재 과제의 목적만 놓고 보면 두 번째 방법이 가장 직접적인 수정이고, 코드의 확장성까지 고려한다면 세 번째 방법을 추천한다.

>급변 지점을 확인하는 것이기 때문에 ai가 추천한 1번과 2번 방법 모두 가장 적절하지는 않다. 그렇게 변화폭이 크지 않은 음수값이 있을 때, 음수값 자체가 중요하기 때문에 이를 체크하기 위한 것이라 앞과 뒤가 하나는 음수, 하나는 양수일 때를 판정해야 한다고 생각한다. 이럴 경우 if문이 보기 불편하게 길어질 수 있으므로 3번에서 ai가 제안한 방식을 채택하여 조건을 변수로 분리하고자 한다.

>>수정 결과, 다음과 같은 출력 결과가 나왔다.
>>```
>>급변 지점 4건
>>(198, 15000.0, -4500.0, -19500.0)
>>(199, -4500.0, 4500.0, 9000.0)
>>(249, 21000.0, 9999999.0, 9978999.0)
>>(250, 9999999.0, 3500.0, -9996499.0)
>>```
>>우리가 원하던 대로 2개의 이상치가 모두 찾아졌음을 볼 수 있다. 따라서 buggy_5.py의 수정을 마무리한다.