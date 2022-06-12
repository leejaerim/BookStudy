# [6장] DML 튜닝

### 6.1.1 DML 성능에 미치는 요인

- 인덱스,무결성 제약, 조건절, 서브쿼리, Redo, Undo로깅, Lock, 커밋

### 6.1.2 데이터베이스 Call과 성능

- Parse Call : SQL 파싱과 최적화를 수행하는 단계
- Execute Call : SQL 실행 단계 (SELECT문은 Fetch단계를 거친다.)
- Fetch Call : 결과집합을 전송하는 과정으로 SELECT 문에서만

Call의 발생위치에 따라서도 UserCall과 RecursiveCall로 나눌 수도 있다.

리커전콜의 경우 DBMS 내부에서 호출되는 콜로 UserCall보다 현저히 빠르게 응답한다.

---

6.1.3 Array Processing 활용

- 배치처럼 만번의 Insert콜을 한번으로 호출함으로써 (Array를 통해) 속도를 현저히 빠르게 만들 수도 있다.

---

### 6.1.4 인덱스 및 제약해제를 통한 대량 DML 튜닝

### 6.1.5 수정가능 조인 뷰

- 수정 가능 조인 뷰를 활용하면 참조 테이블과 두번 조인하는 비효율을 없앨 수 있다.
- 키보존 테이블 - 조인된 결과집합을 통해서도 중복 값 없이 유니크하게 식별이 가능한 테이블.

---

### 6.1.6 Merge 문의 활용

- DW에서 가장 흔히 발생하는 신규 트랜잭션 데이터를 반영함으로써 두 시스템간의 동기화작업이다.

```sql
merge into customer t using cutomer_delta s on(t.cust_id = s.cust_id)
when matched then update 
	set t.cust_nm = s.cust_nm, ...
when not matched then insert
	... values ... ;
```

- 소스테이블 기준으로 타겟 테이블과 레프트 아우터 방식으로 조인하여 업데이트하고 실패하면 인서트한다.
→ 이런 이유로 Merge를 UPSERT 라고 부르기도 한다.
- 한가지 중요한 사실은 MERGE문이 DELETE 절로 인한 조인에 성공한 데이터만 삭제할 수 있다는 점이다.
→ 소스테이블의 지워진 데이터를 타겟에서도 지우고 싶겠지만, 머지문이 딜리트절까지 그 역할을 못한다는 것이다. 소스에서 삭제된 데이터를 그냥 조인에 실패할 뿐이기 때문이다.
- 결국 DELETE 절은 조인에 성공한 데이터를 모두 업데이트하고 나서 결과값 DELETE WHERE 해야한다.

---

# Direct Path I/O 활용(***대량 데이터의 처리***)

<aside>
🔥 대량 데이터 처리시 버퍼캐시를 경유하는 I/O매커니즘이 성능을 떨어뜨릴 수 있다. 버퍼캐시 경유 없이이곧바로 데이터블록을 읽고 쓰는 direct path I/O 기능에 대해 알아본다.

</aside>

### 6.2.1 Direct Path I

1. 일반적으로 버퍼캐시를 이용해 데이터의 존재를 읽어보고 상대적으로 속도가 느린 I/O 콜을 줄이게 된다. 하지만 대량 데이터 처리시에는 오히려 버퍼캐시의 역할이 성능을 줄게 된다.(일반적으로 풀스캔 대량 데이터 처리는 블록 재사용가능성이 거의 없다.)
2. 기능이 작동하는 경우 
- 병령쿼리 풀스캔
- 병렬 DML 수행
- 다이렉트 패스 인서트
- Temp 세그먼트 블록 Reading&Insert
- 다이렉트 옵션지정 후 export 시
- nocache 옵션을 지정한 LOB 칼럼을 읽을 때

```sql
select /*+ full(t) parallel(t 4) */ * from big_table t;
select /*+ index_ffs(t big_table_x1) parallel_index(t big_table_x1 4) */ count(*) from big_table t;
```

- 다음과 같은 병렬도 지정시, 성능 4배가 아닌 수십배 빨라지게 되는데 이때 DP I/O 때문이다.

---

### 6.2.2 Direct Path Insert

- 일반적인 Insert 구문은 느린데, 이에 DPI/O 방식을 사용하면 훨씬 빠르게 대량 데이터를 인서트 가능하다.
- Freelist 참조 하지 않으며, HWM 바깥 영역에서 데이터를 순차적으로 입력하며
- 블록을 버퍼캐시에서 탐색하지 않는다.
- 버퍼캐시에 적재하지 않고, 데이터 파일에 직접 기록한다.
- Undo 로깅을 안하며, Redo는 안하게 할 수 있다.

---

### 6.2.3 병렬 DML

- UPDATE, DELETE는 기본적으로 Direct Path Write 방식이 불가능 하다. 따라서 병렬 DML으로 처리할 것인데, 병렬 DML에 항상 DPW 방식을 적용해 처리할 수 있다.

```sql
alter session enable parallel dml;
-- 병렬 DML 활성화
```

- 다음과 같이 CRUD 가능

```sql
insert /*+ parallel(c 4) */ into 고객 c
select /*+ full(o) parallel(o 4) */ * from 외부가입고객 o;

update /*+ full(c) parallel(c 4) */ 고객 c set 고객상태코드 = 'WD'
where 최종거래일시 < '20100101';

delete /*+ full(c) parallel(c 4) */ from 고객 c
where 탈퇴일시 < '20100101';
```

- 결국 병렬 DML도 dpw방식을 사용하므로 데이터를 입력/수정/삭제 시, Exclusive 모드 TM Lock이 걸린다는 사실을 꼭 기억하자. 따라서 ***트랜잭션이 빈번한 주간에 이 옵션을 사용하는 것은 절대 금물이다.***

---