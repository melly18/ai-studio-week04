# -*- coding: utf-8 -*-
"""
buggy_2.py  ―  카테고리별 매출 집계 (pandas 버전)

dirty_sales.csv를 pandas로 읽어 카테고리별 매출 합계를 구하려 한다.
그런데 실행하자마자 죽는다.

[과제] Traceback을 얻어 예외 타입을 확인하고,
       '원인을 데이터에서 직접 확인'한 뒤(힌트: 실제 컬럼명이 무엇인가?)
       코드를 수정하라.
"""
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