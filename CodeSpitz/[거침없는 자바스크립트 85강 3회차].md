# [거침없는 자바스크립트 85강 3회차]

### CPS = Continuation Passing Style

- Context & Switch
- 일정 작업 후 Passing 함. 블록킹을 짧게 하도록 구현함. 
- 거대한 Switch문으로 관리와 가시성이 나쁨.

```jsx
const gene = function*(a){let b; yield a; b= a; yield b;}
//suspend를 걸어서 b 변수의 상태
```

```jsx
const wrap = block=> new SwitchIterable(block);
const SwitchIterable = class{#block; constructor(block){this.#block = block;}
	[Symbol.iterator](){return new SwichIterator(this.#block);}
}
const SwitchIterator = class{
	static done = {done : true};
	#block;
	#context = new Context;
	constructor(block){this.#block = block;}
	next(){
		const value = this.#block(this.#context);
		return value === Context.stop ? SwitchIterator.done : {value,done:false}
	}
}
const Context = class{ static stop = Symbol(); prev = 0; next = 0; stop(){return Context.stop;}}

const gene2 = a=>{
	let b;
	return wrap(_context=>{
		while(1){
			switch(_context.prev = _context.next){
				case 0:
					_context.next = 2;
					return a;
				case 2:
					b = a;
					_context.next = 5;
					return b;
				case 5:
				case "end" :
					return _context.stop();
			}
		}
	}
}

```

---

### Continuation & Resume

- 

```jsx
const gene4 = a => {
	let b;
	return new SeqIterable{cont =>{cont.resume(a);},cont=>{b=a;cont.resume(b);}}
}
const SeqIterable = class {
	#block;
	constructor(...blocks){this.#block = blocks;}
	[Symbol.iterator](){return new SeqIterator(this.#blocks.slice(0));}
};
const SeqIterator = class{
	static done = {done:true};
	#blocks;
	#cont = new Continuation;
	constructor(blocks){this.#blocks = blocks;}
	next(){
		if(!this.#block.length) return SeqIterator.done;
		const cont = this.#cont;
		cont.stop();
		this.#block.shift()(cont);
		return cont.isStop()? SeqIterator.done : {value:cont.value(), done:false};
	}
}
const Contivuation = class{
	static #stop = Symbol();
	#value;
	resume(v){return this.#value =v;}
	value(){return this.#value;}
	stop(){this.#value = Continuation.#stop;}
	isStop(){return this.#value === Continuation.#stop;}
}
```

<aside>
💡 필요한 역할과 책임을 먼저 만든 후 그 이후에 클래스를 만드는 습관을 들이도록 하자.

</aside>

```jsx
//흐름을 안에서 관리할 수 없음. -> 다양한 전진을 확인해보자
const gene = function*(a){let b; while(1){a++;b=a;yield b;}}
//외부에서 흐름을 제어하는 것은 잘 못된 거다.
//함수로 되어있음에도 불구하고 스택클리어 되어 재귀함수와 같은 스택오버플로우가 일어나지 않는다.
new Continuation (0,cont=>{if(!1) cont.stop(); cont.resume();})
.next(new Continuation(1,cont=>{a++;b=a;cont.resume(b,0);//값을 반환하면서 특정 컨티뉴에이션으로 이동}));
```

```jsx
const Contunation = class{
	#key, #block;
	static #pass = Symbol();
	static #stop = Symbol();
	setSequence(seq){
		this.#seq = seq;
		seq.setCont(this.#key, this);
	}
	setNext(cont){this.#next = cont;}
	getNext(){return this.#next;}
	suspend(){
		this.#value = Continuation.#stop;
		this.#block(this);
	}
	resume(v=Continuation.#pass, next){
		this.#value = v;
		if(next != undefined) this.#next = this.#seq.getCont(next);
	}
	value(){return this.#value;}
	isStop(){return this.#value === Continuation.#stop;}
	isPass(){return this.#value === Continuation.#pass;}
}
```

```jsx
const Sequence = class {
	#table = new Map;
	#cont; #end;
	constructor(cont){
		this.#cont = this.#end = cont;
		cont.setSequence(this);
	}
	next(cont){
		this.#end.setNext(cont);
		this.#end = cont;//링크드리스트 알고리즘
		cont.setSequence(this);
		return this;
	}
	getCont(key){if(!this.#table.has(key)) throw "no key"; return this.#table.get(key);}
	setCont(key,cont){if(this.#table.has(key) throw "exist key"; return this.#table.set(key,cont);}
	[Symbol.iterator](){return new Iterator(this.#cont);}
}
const Iterator = class{
	#target;
	constructor(cont){this.#target = cont;}
	next(){
		const target = this.#target;
		if(target == undefined) return Iterator.done;
		target.suspend();
		if(target.isStop()) return Iterator.done;
		if(target.isPass()){
			this.#target = target.getNext();
		}else{
			const result = {value : target.value(), done:false};
			this.#target = target.getNext();
			return result;
		}
	}
}
```

---

### Continuation Context

- 어휘공간에 따른 재설계(어휘공간을 제약함으로써 변수이름에 대한 혼동을 방지할 수 있게됨)
- 클로저를 통한 어휘공간의 제공은 javascript에서만 가능
    - 렉시컬인바이런먼트(어휘환경 혹은 어휘공간)에서 나아가 렉시컬 컨텍스트를 공유함으로써 이슈를 해결.

```jsx
const gene = a => {
	return new Context().set("a",a).set("b",undefined).next(...).next(
		new Continuation(1,cont =>{
			cont.set("a",cont.get("a") +1);
			cont.set("b",cont.get("a"));
			cont.resume(cont.get("b"),0); 
		}
	)};
}
const Context = class extends Map{
	...
}
```

---

- CPU 폰노이만 구조에서 코드가 블록킹 되고, 그 와중에는 다른 프로세스나 코드가 실행될 수 없는 구조를 이해했다.
- 그렇다면 블록킹구조를 없앨 수 있는가? → 없다. 그래서 블록킹 길이를 줄이는 방법을 택했다.
- 기본적인 for문을 1억번 한다고 가정한다. for문 내부가 단순하면 좋겠지만, 복잡하다면 복잡한 반복문이 1억번 실행되는 동안 우리는 cpu의 점유를 바꿀수 없다.
- 블록킹 길이를 줄이는 방법으로 우리는 Generator와 Iterator의 스펙을 사용하여 확인 해보고자 한다.
- 자바스크립트 엔진은 싱글스레드 라고 하지만, 기본적으로 콜백큐에 삽입하며 생성.소비구조의 파이프 패턴을 사용한다.
- 그래서 우리는 논블록킹 반복문을 만들어 보았고, 이 뿐 아니라 나아가 제네레이터를 구현하였다.(2강)
- 오늘 3강에서는 CPS를 이용한 제네레이터를 만들어 보았다. 다음 4강에서는 비동기 제네레이터를 공부할 예정이다.