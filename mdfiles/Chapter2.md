## 2. 저장소 패턴
- 데이터 저장소를 더 간단히 추상화 한 것을 의미한다.
- 모델 계층과 데이터 계층을 분리할 수 있다!

### 데이터 접근에 DIP 적용하기
- DIP : 의존 관계 역전 원칙(Dependency Inversion Priciple), "추상화 된 것에 의존하라"
- 모델을 내부에 있는 것으로 간주하고 의존성이 내부로 들어오도록 만들어야 한다. -> "양파 아키텍처"

### 우리가 일반적으로 사용하는 모델
- 일반적으로는 ORM에 의존한다.
- ORM은 영속성 무지를 제공함 : 어떻게 데이터를 적재, 영속화하는지 알 필요가 없음 -> 즉, 특정 데이터베이스 기술에 도메인이 의존하지 않도록 한다.
```python
class Order(Base):
    id = Column(Integer, primary_key=True)

class OrderLine(Base):
    id = Column(Integer, primary_key=True)
    sku = Column(String(250))
    qty = Integer(Stirng(250))
    order_id = Column(Integer, ForeignKey('order.id'))
    order = relationship(Order)
```
- 의문점 : SQLAlchemy에서 ORM을 작성하는 것은 Column 객체를 알아야하고 이 객체를 사용하여 속성을 정의하게 된다. 이러면 우리가 작성한 모델은 ORM에 의존하고 있는 것이 아닌가?


### 의존성 역전
- 모델이 ORM을 의존하는 것이 아니라, ORM이 모델을 의존하도록 할 것이다.
- SQLAlchemy에서는 이렇게 구현함
```python
from sqlalchemy.orm import mapper

import model # 여기를 주목하세요~!

metadata = MetaData()

order_lines = Table(
    'order_lines', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True)
    Column('sku', Stirng(255)),
    ...

def start_mappers(): # 여기서 mapping 해줌
    lines_mapper = mapper(model.OrderLine, order_lines)
)
```

- ORM은 도메인 모델을 import(의존)한다.
- 도메인 모델에서는 ORM을 사용하지 않는다.

### 저장소 패턴
- 저장소 패턴이란 영속적 저장소를 추상화 한 것이다.
- 모든 데이터가 메모리상에 존재하는 것 처럼 가정하여 데이터 접근과 같은 세부 사항들을 감춘다.
```python
class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, batch: model.Batch):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> model.Batch:
        raise NotImplementedError
```
- 도메인과 서비스 계층에서 데이터에 접근할 때 엄격하게 이 메서드만 사용하게 함
- 이렇게 코드를 짜게되면 단순성이 유지되고, 도메인 모델과 데이터베이스 사이의 결합을 끊을 수 있다.


### 트레이드 오프
- 추상화는 지역적으로 복잡성을 증가시키고 지속적으로 유지보수가 필요하다.
- 저장하는 방법을 더 쉽게 바꿀 수 있고 단위 테스트 시 mock을 사용할 수 있게 된다.
