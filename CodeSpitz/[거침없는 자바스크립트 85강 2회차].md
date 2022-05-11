# [거침없는 자바스크립트 85강 2회차]

### Concurrency(동시성)

- 엄밀하게 Parallelism*(병행성)과는 다르다. 시분할 시스템 처럼 나누어서 병행성을 제공하는 것처럼 느껴짐
- 병행성은 공유메모리에 대한 문제가 존재한다.
- Javscript Concurrency
    - 엔진워크(랜더링) → 큐체크(↔콜백큐) → run JS → 엔진 워크
    - run JS의 실행시간을 줄임으로써 동시성을 제공.
    - 멀티스레드환경(*네트워크,타이머,메서지,돔이벤트 등)에서 생성/소비패턴을 사용 → 파이프패턴.
    - 멀티스레드환경에서 콜백큐에 어떻게 넣어주는지만 생각해주면 된다.
    - 콜백큐 이하는 병행성을 갖지만, 이상에서 동시성을 제공하는 구성을 갖는다.
- SetTimer 실습

```jsx
const Item = class{ time; block; constructor(block,time){
	this.block = block;
	this.time = time + performance.now();
}}//큐에 들어갈 항목, Item클래스로 감싼다.
const queue = new Set;
const f = time=>{queue.forEach(item=>{if(item.time >time) return
	queue.delete(item);
	item.block();//forEach에서 복사 루프
});
requestAnimationFrame(f);
};
requestAnimationFrame(f);

const timeout = (block,time)=>queue.add(new Item(block,time));
timeout(_=>console.log("hello"),1000);
```

- Non Blocking For

```jsx
const working =_=>{};
for(let i =0; i<10000; i++) working();//blocking
const nbFor = (max,load, block)=>{
	let i = 0;//i는 일관성있게 static 처럼 
	const f = time=>{
		let curr = load;
		while(curr-- &&  i < max){
			block();
			i++;
		}
		if(i<max -1) requestAnimationFrame(f)
	};
	requestAnimationFrame(f); 
};
//클로저패턴을 이용한 non-blocking
nbFor(100,10,working) 
```

---

### Generator

- Iterator를 알아야 하고 이터레이터는 next라는 함수가 있고, 오브젝트를 반환한다는 프로토콜 인터페이스가 정의 되어있다.

```jsx
const infinity = (function*(){
	let i = 0;
	while(true) yield i++;
})()
//yield를 호출하게 되면서 suspend되고, next가 호출될때마다 resume된다.
//function*()은 제네레이터 함수.
```

```jsx
const gene = function*(max,load,block){
	let i =0, curr = load;
	while(i<max){
		if(curr--){block();i++;}
		else{curr=load;yield;}
	}
}//nbrBlock와의 차이로 클로저변수가 아닌 지역변수, 제어의 일부를 위임함으로써 해결
//기본적으로 외부의 제어 개입을 할수 있는 여지를 줌.
const nbFor = (max,load,block)=>{
	const iterator = gene(max,load,block);
	const f =_=>iterator.next().done||timeout(f);
	timeout(f,0);
}
nbFor(100,10,working)//내부로직은 완전히 다르다.
```

### 반제어역전 - Promise

- trigger를 호출할 수 있지만, 언제 콜백올지 보장할 수 없음.
- 원할때, then을 호출. (promise.then의 경우, 콜백과 동일함)
- 애니메이션함수가 프로미스를 받아오고, 원하는 시점에 then을 걸어주면, 원하는 시점에 콜백을 처리할 수 있다.

```jsx
const gene2 function*(...){
	...
	yield new Promise(res=>{
		let curr = load;
		while(curr-- && i<max){block();i++;}
		timeout(res,0);
	}
	...
}
const nbFor = (max,load,block)=>{
	const iterator = gene2(max,load,block);
	const next = ({value, done})=>done|| value.then(v=>next(iterator.next())));
	next(iterator.next());
}//제어권이 gene2에서 promise가 하고 있다. 개별적인 테스크로 분리해서 밀어줌.(책임)
```