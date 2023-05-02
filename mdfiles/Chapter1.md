## 1. 도메인 모델링
- 예제를 이용한 TDD 익히기
- 도메인 모델의 기본 개념 및 도메인 모델의 핵심 패턴 살펴보기
  - 도메인 : 우리가 해결하려는 문제
  - 모델 : 문제를 해결하기 위한 지도 
  - 도메인 모델 : 비즈니스 모델을 해결하기 위한 방법
- 도메인 모델링의 핵심 패턴 : 엔티티, 값 객체, 도메인 서비스


### (예제)
입고가 곧 될 상품(현재 배송 중)을 실제 재고로 간주하여 판매한다.
따라서 재고가 없는 상품이 줄어드므로 더 많은 상품을 팔 수 있고, 더 적은 재고를 보관해도 된다.  
기존에는 "주문이 들어오면 재고를 n개 줄인다"가 도메인 모델이었지만 이제는 더 복잡해졌다.
- SKU : 제품명
- 주문 : 주문 참조번호로 식별된다
- 주문 라인 : SKU, 수량
- 배치 : 유일한 ID, SKU, 수량

### 추가 사항
테스트 test_can_only_deallocate_allocated_lines이 추가됨.  
즉, 주문이 주문라인에 할당되지 않았을 경우 재고에 아무런 영향이 없어야 함.
- Batch가 자신이 할당된 라인을 알고 있어야 한다.
  - 왜? 주문 라인에 넣을 수 있는 상태인지 확인하고(can_allocate), allocate를 실행하기 위해서.
  - 즉 주문 라인에는 한 제품만 있는게 아님. 여러 제품과 여러 주문이 존재하는데 주문 라인으로 넘기기 전에 deallocate를 하게 된다면 수량 추적에 정확도가 낮아짐. 그래서 수량을 가장 마지막에 계산하도록 함(allocated_quantity).
  - 왜 set을 이용해서 중복처리를 하는가 : 라인이 배치가 되었으면 수량이 줄어들어야 하는데 수량이 똑같으면 안되므로 중복 처리 필요  
  ex) A제품의 재고가 1개고, 1개의 주문이 들어왔음 -> 똑같은 batch가 두번 주문라인으로 오게되면 재고 관리상 문제가 생김


### **값 객체와 엔티티**
#### 1. 값 객체
- 주문에는 여러 라인이 있고 라인은 SKU와 수량으로 이루어져 있다.
- 라인에는 식별할 수 있는 식별자가 없는데 보통 "값 객체" 패턴을 선택하여 식별값을 매긴다.
- 값 객체란 안에 있는 데이터에 따라 식별될 수 있는 도메인 객체를 의미한다.
- 값 객체는 보통 불변객체로 만든다.
- 값 동등성이란 안에 있는 데이터가 같으면 같다는 말이다.
#### 2. 엔티티
- 엔티티 : 사람의 이름을 바꿔도 똑같은 사람. 즉 값 객체와 다르게 오랫동안 유지되는 정체성이 있는 것.
- 정체성 동등성 : 엔티티의 값을 바꿔도 바뀐 엔티티는 동일하게 인식된다.

### **(구현하기)**

#### 1. 값 객체
- 내부값이 변경되면 새 객체가 된다.
- 모든 값 속성을 사용하여 해시를 정의한 후 불변 객체로 만들어주어야 한다.

#### 2. 엔티티
- 내부값이 변경되어도 동일 객체임
- 해시를 None으로 정의한다.


### 도메인 서비스 함수
- 모든 것을 객체로 만들 필요가 없다. 오히려 동사에 해당하는 부분을 표현하려면 함수를 사용하는 편이 좋음.
- 예외를 사용하여 도메인 개념을 표현할 수 있다.