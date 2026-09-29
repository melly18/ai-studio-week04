# -*- coding: utf-8 -*-
"""
buggy_1.py  ―  판매 데이터 매출 집계 (csv 모듈 버전)

dirty_sales.csv를 한 줄씩 읽어 '매출액 = 단가 x 수량'을 누적한다.
잘 돌아가는 것처럼 보이지만, 어떤 행에서 갑자기 멈춘다.

[과제] 이 스크립트를 실행해 Traceback을 얻고,
       진단 3단계 루틴(무엇이 / 어디서 / 왜)으로 원인을 특정한 뒤
       전처리로 해결하라. (힌트: 예외 타입은 무엇인가?)
"""
import csv

def calc_total(path):
    total = 0
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)  # 사전타입으로 데이터를 읽음.
        missing_v = 0   #FIXED: 결측치 개수를 세기 위한 변수
        for i, row in enumerate(reader):
            if row["price"] == '':      #FIXED: 만약 price의 값이 없다면
                missing_v += 1  #FIXED: 결측치 개수에 1을 더하고
                continue     #FIXED: 해당 row의 연산을 수행하지 않는다.
            price = int(row["price"].replace(",","").replace("원","").strip())   #FIXED: 콤마와 "원" 제거 후 int 변환
            qty = int(row["quantity"])
            total += price * qty
    return total, missing_v  #FIXED: 결측치 개수도 return해 준다.

if __name__ == "__main__":
    total, missing_v = calc_total("dirty_sales.csv") #FIXED: 잘못된 파일 경로 수정 & return 변화에 따른 추가 변수 설정
    print(f"총 매출액: {total:,}원")
    print(f"결측치: {missing_v:,}개")  #FIXED: 결측치의 개수를 사용자에게 알린다.
