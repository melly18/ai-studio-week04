## 1. buggy_1.py
AI 미사용

## 2. buggy_2.py
AI 미사용

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