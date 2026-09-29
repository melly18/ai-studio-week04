# -*- coding: utf-8 -*-
"""
buggy_3.py  ―  데이터 로드 후 카테고리별 집계

load_and_clean()으로 데이터를 읽어 정제한 뒤,
그 결과를 groupby로 집계하려 한다.
그런데 집계 단계에서 이상한 에러가 난다.

[과제] Traceback의 예외 타입을 확인하고,
       'NoneType ...' 메시지가 가리키는 '이 변수를 만든 직전 단계'를
       역추적하여 원인 함수를 찾아 수정하라.
"""
import pandas as pd

def load_and_clean(path):
    df = pd.read_csv(path, encoding="utf-8")
    # price 컬럼을 숫자로 정제
    df["price"] = (df["price"].astype(str)
                              .str.replace(",", "")
                              .str.replace("원", "")
                              .str.strip())
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df.dropna(subset=["price"])  #FIXED: price의 결측치 row를 제거한다.
    df["category"] = df["category"].fillna("미분류")  #FIXED: category의 결측값을 '미분류'로 새롭게 지정한다.
    df["price"] = df["price"].astype(int)  #FIXED: price를 int 변환한다.
    df["revenue"] = df["price"] * df["quantity"]

    return df  #FIXED: DataFrame을 반환해 준다.

def main():
    df = load_and_clean("dirty_sales.csv")
    result = df.groupby("category")["revenue"].sum()
    print(result)
    assert result.sum() == 151198388824

if __name__ == "__main__":
    main()
