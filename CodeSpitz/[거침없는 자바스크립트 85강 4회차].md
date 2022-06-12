# [4강] 85강 거침없이 자바스크립트

### Sequential Async

```jsx
const render = function(...urls){
	Promise.all(urls.map(url=>fetch(url,{method}....
}
const render = function(...urls){
	const loop =_={
		if(urls.length){
			fetch(urls.shift(), {method:"GET"}).then(res=>res.json()).then(json=>{
				console.log(json);
				loop()
			});
		}
	}
	loop();
}
render("1.json","2.json","3.json");
```

### Generator & Executor

- dataLoader 분기했어도 함수로 호출해서 랜더링할 뿐이다.
- 프로미스를 리턴하고 있고, 외부에서 제어(위임) , 데이터로더를 수정할 가능성을 줄여버린다.
- 제어를 처리하는 부분과 제어를 처리하는 부분

```jsx
const dataLoader = function*(f,...urls){//Generator
	for(const url of urls){
		const json = yield fetch(url,{method:"GET"}).then(res=>res.json());
		f(json);
	}
};
const render = function(...urls){
	const iter = dataLoader(console.log,...urls);
	const next = ({value,done})=>{
		if(!done)value.then(v=>next(iter.next(v)));	
	};
	next(iter.next());
};
render("1.json","2.json","3.json");
```

- dataLoader는 제네레이터 맵으로 볼 수 있다.
- 외부 제어가 비동기를 할 줄 알아서 성립한다. 비동기를 캡슐화 해서 넘겨줬고, 외부제어쪽에서 처리
- 프로미스 객체를 주고 then을 외부제어에서 호출될 때 가장 큰 강점을 갖는다.

---

- 데이터로더 함수는 f 함수를 통해서 데이터 처리 및 프로미스 객체 반환 두가지 작업을 하게 되고 우리는 하나의 함수는 하나의 책임을 진다는 원칙에 의해 수정할 필요성을 갖는다.
- 수정된 함수는 다음과 같다.

```jsx
const dataloader = function(...urls){
	for(const url of urls){
		const json = yield fetch(url,{method:"GET"}).then(res=>res.json());
		yield json;
	}
}//비동기 처리도 값처리도 yield를 구분할 필요가 있다.
...
const next = ({value,done})=>{
	if(!done){
		if(value instanceof Promise) value.then(v=>next(iter.next(v)));
		else{
			console.log(value);//데이터처리를 다시 랜더링으로 다시 넘어오게 만들었다.
			next(iter.next());
		}
	}
}//dataloader는 순수히 데이터로드하는 역할, 즉 Promise를 통한 제어권을 넘겨주는 역할만 한다.
```

### Async Iterator

```jsx
const render = async function(...urls){
	for(const url of urls){
		console.log(await(await fetch(url,{method:"GET"})).json())
	}
}
```

- Promise.then을 단축표현한 것이 바로 await 이다.
- 제어, 랜더 전부 들어가 있음.

```jsx
const dataLoader = async function*(...urls){
	for(const url of urls){
		yield await(await fetch(url,{method:"GET"})).json();
	}
}//åsync Generator
const render = async function(...urls){
	for await(const json of dataLoader(...urls)){
		console.log(json)
	}
}//마찬가지로 async이여야지만 async Generator를 사용할 수 있다.
//async iterator(프로미스가 존재)
```

---

### Async yield*

- 서스펜드의 연쇄 다중 뎁스를 지원하는 대표적인 문법이 async yield*

```jsx
const urlLoader = async function*(url){
	yield await(await fetch(url, {method:"GET"})).json();
}
const dataLoader = async function*(...urls){
	for(const url of urls) yield* urlLoader(url);
}
const render = async function(...urls){
	for await(const json of dataLoader(...urls){
		console.log(json)
	}
}
```

- urlLoader를 dataloader에서 제어하고자 한다.
- 서브이터러블을 외부 이터러블로 빼주는 작업.

---

### Async Group

```jsx
const url = async function*(url){
	yield await (await fetch(url,{method:"GET"})).json();
}
const urls = async function*(...urls){
	const r = [];
	//map객체로 url함수를 넘겨 async 함수의 결과값으로 프로미스 객체 u를 갖게 된다.
	for(const u of urls.map(url)).r.push((await u.next()).value);
	yield r;
}
const dataLoader = async function*(...aIters){...}
const render = async function(...aIters){...}
render(urls("1.json","2.json"),url("3.url");
```

- 한계점 : 모든 문법은 프로미스를 수용하게 된다. 또, Iterator객체로 값이 감싸져서 오게 된다.

---

```jsx
const start = function*(url){yield "load start"}
const end = function*(url){yield "load end"}
render(start(),urls(...),url(...),end())
//이젠 랜더 함수에 start,end등의 이터레이터를 반환하는 제네레이터 함수로
// 프로미스 객체이기만 하면, 랜더의 파라미터로 들어갈 수 있다.
```

- 제네레이터(서스펜드구문)이 없다면, 제어의 추상화를 할 수 없다. 데이터로더로 제어의 추상화되어있음.
- 자바 또한 마찬가지로 wait-set함수로 언어수준에서  cps 구현가능

---

### Pass Param

- 앞에 있는 결과를 뒤에 사용하고자 한다면, 1번,2번 데이터를 이용하여 3번 데이터를 로딩하려면, 우리는 Pass Param 해야 한다. 어떻게 일반화 할 수 잇을 것인가?

```jsx
const url = (url,opt={method="POST"})=>new Url(url,opt);
const Url = class{
	#url, #opt;
	constructor(url,opt){
		this.#url = url;
		this.#opt = opt;
	}
	async *load(){
		yield await(await fetch(this.#url. this#opt)).json();
	}
}
```

- 인자와 지역변수만 쓸수 있었던 기존 제네레이터 함수와 다르게, 클래스 메소드인 제네레이터 this를 추가적으로 사용할 수 있다.나중에 변화하는 속성을 this로 잡아줄 수 있다면, 변화에 대응 가능하다.
- this컨텍스트를 통해 다르게 작동하는 어싱크로드 함수를 만들 수 잇다.
- load 함수가 ***인자도 없이 지역변수도 없이 this를 쓸수 있다는 점***이 가장 큰 차이점이다.
- 호출되는 시점에 따라서 this가 다르고 그에 따라 동적으로 바인딩되는 장점이 있다.

---

### Async Iterator Class

```jsx
const AIter = class{
	update(v){}
	async *load(){throw "override";}//런타임 오버라이딩 강제
};
const Url = class extends AIter{
	...
	update(json){if(json) this.#opt.body = JSON.stringify(json);}
	async *load(){
		yield await(await fetch(this.#url, this.#opt)).json();//this lazy binding
	}
}
...
const urls=  (...urls)=>new Urls(...urls.map(u=>url(u));//A타입을 B타입으로 바꿔주는 Map
const Start = class extends AIter{
	async* load(){yield "load end";}
}
const START = new Start();//싱글톤 객체
...
const dataLoader = async function*(...aIters){
	let prev;
	for(const iter of aIters){
		iter.update(prev);//각각의 클래스가 업데이트를 어떻게 오버라이딩했는지에 맡긴다.
		prev = (await iter.load().next()).value;
		yield prev;
	}//루프를 돌면서 A의 결과를 B에 주고 B의 결과를 C의 주는 시퀀셜한 어싱크 이터레이터.
}
```

- 단순하게 하고싶은 작업들만 만들었고, (어휘)를 기술하고, 제어위임을 성공하지 않으면 코드를 전부 유지보수 해야된다. 파라미터에 들어오는 각각의 객체에게 유지보수를 위임한다라는 것.
- 랜더 함수엔 이터레이터와 어싱크 어웨이트 로직외엔 안들어있음(언어수준) 그 나머지는 데이터로더에게 위임. 마찬가지로 커스텀 타입의존성이 없음. 순수한 값만 어떻게 소비할지 정의한다.
- 무엇보다. ***asyncItrator 클래스 객체의 변화에 dataloader함수에게 위임함 으로써  어떤 aIter클래스가 변화한다더라도 랜더함수와 변화가 없다.***
- dataloader가 Pass pram과 prev에 대한 상태값을 관리한다.
- 코드는 사라지지 않고 어떻게 배치하느냐, 즉 설계하느냐에 따라 ***단일책임원칙***을 제공하고자 한다.

---