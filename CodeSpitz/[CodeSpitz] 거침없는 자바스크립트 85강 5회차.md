# [거침없는 자바스크립트 85강 5회차]

### DataPass

- 추상화될 수록 덜 변화한다.
- 결국 목적은 `변화율에 따른 코드를 관리`하기 위하여 추상화 하게 된다.

```jsx
 const dataLoader = async function*(...aIters){
	const dataPass = new DataPass;
	for(const item of aIters){
		const v = await item.load(dataPass.data).next();
		yield dataPass.data = v.value;
	}
}
//업데이트 이후 로더를 호출하게 되는데 , 이는 트랜잭션이다.
//업데이트와 동시에 로드할 수 있도록 트랜잭션 동시성 제어 한다.
```

### DataPass Class

```jsx
const DataPass = class{
	get data() {throw}
	set data(v) {throw}
}
const PrevPass = class extends DataPass{
	#data;
	get data(){return this.#data}
	set data(v) {this.#data = v;}
}
const IncPass = class extends DataPass{
	#data = [];
	get data(){return this.#data}
	set data(v) {this.#data.push(v)}
}
```

### 런타임 바인딩

```jsx
//런타임 바인딩
const render =async function(...aIters){
	for await(const json of dataLoader(PresvPass, ...aIters)){...}
}
//우리는 이제 데이터로더에게 pass를 동적으로 바인딩하여 데이터로더 js에서의 변화에 무관하게 된다.
```

- if 하나 없을 때마다 런타임바인딩 전략객체가 오고 case 마다 전략객체 케이스로 대응해줘야 한다.

---

### AsyncItem

```jsx
const AsyncItem = class{
	static #dataPass; static#items;
	static iterable(dataPass,...items){
		AsyncItem.#dataPass = dataPass;
		AsyncItem.#items = items;
		return AsyncItem;
	}
	static async *[Symbol.asyncIterator](){
		const dataPass = new AsyncItem.#dataPass;
		for(const item of AsyncItem.#items){
			const v = await item.load(dataPass.data).next();
			yield dataPass.data = v.value;
		}
	}
	async *load(v){throw}
}
//데이터패스에 대한 지식은 갖게 되지만, 자신의 지식으로 모두 처리가능하게 되어 의존성이 줄어든다.
const render = ...
	AsyncItem.iterable(PrevPass,...aIters)
}
//데이터로드를 삭제하고 Item 에서 처리
```

---

### Render

```jsx
const Renderer = class{
	#dataPass;//프라이빗 필드
	constructor(dataPass){
		this.dataPass = dataPass;
	}
	set dataPass(v){this.#dataPass = v;}
	//데이터 일관성을 위해 Set함수로
	async render(...items){
		const iter = AsyncItem.iterable(this.#dataPass,...items);
		for await(const v of iter)...
	}
}

-> const renderer = new REnderer(PrevPass);
-> rednerer.render(...)
```

---

Url

```jsx
const AsyncItem = class{...}
const Url = class extends AsyncItem{
	#url; #opt; #dataF;
	constructor(u,opt,dataF = JSON.stringify){...}
	async *load(v){
		if(v) this.#opt.body = this.#dataF(v);
		return await(await fetch(this.#url, this.#opt)).json();
	}
}//인스턴스 호출마다 밸류 차이점을 주기 위해 lambda로 구현(인스턴스 차별 전략)
//클래스 오버라이딩 혹은 훅은 클래스별 차이를 준다.(안정성은 좋지만, 변화율에 대한 처리가 힒듬)
```

---

Urls

```jsx
//병행 구현
const Parallel = class extends AsyncItem{
	#items;
	constructor(..items){}
	async *load(data){
		const arr = [...this.#items].map(item=>item.load(data).next());
		//원본데이터 유지를 위해 복사된 배열로 사용.
		//next() 값으로 프로미스 값을 얻어올수 있다.
		return (await Promise.all(arr)).map(v=>v.value);
		//A타입을 B타입으로 바꿔는 map 방식
	}
}
-> const arr = AsyncItem.toPromises(this.#items, data);
```

<aside>
🔥 const arr = [...this.#items].map(item=>item.load(data).next()); 여기서 프로미스객체가 들어오고 여기서 value를 맵객체로 추출하여 리턴한다.

</aside>

```jsx
const AsyncItem = class{
	...
	static toPromise(items,data){
		return [...items].map(item=>item.load(data).next());
	}
//어싱크아이템 레벨의 지식밖에 사용하고 있지 않는 코드를 parallel에 가지고 있는것 자체로 버그다.
}
```

```jsx
const Race = class extends AsyncItem{
	#items;
	constructor(...items){...	}
	async *load(data){
		return (await Promise.race(AsyncItem.toPromises(this.#items, data))).value;
	}
}
```

---

### Timeout

```jsx
const Timeout = class extends AsyncItem{
	static get =(time,msg="timeout") => new Timeout(time,msg);
	#timeout;
	constructor(time,msg){...}
	async *load(v){
		yield await new Promise(this.#timeout);
	}
}
```

<aside>
🔥 함수의 콜링은 invokation 과 Execution으로 나누어있다. 상단의 await의 경우도 마찬가지로 기동시켜놓고 실제로 await를 통해 실행하게 한다.
우리는 이 측면을 가지고 커맨드 패턴을 사용할 수 있다. 실행을 재실행, 취소 등등 분리하여 사용할 수 있다.

</aside>

→ Url Timeout

```jsx
//in Url
//fatch 그저 패치를 할뿐
static get = (u,timeout=0,opt={method:"GET"})=>timeout >0 ?
	new Race(new Url(u,opt),Timeout.get(timeout)): new Url(u,opt);
static post = (u,timeout,opt={})=>{
	opt.method = "POST";
	return Url.get(u,timeout,opt);
}
static urls= (...urls)=>Parallel.get(Url.get,...urls);
async *load(v){

}
const renderer =new Renderer(PrevPass);
renderer.render(
	Url.urls(...)
	Timeout.get(100);
	Url.get("3.json",1000)
)
//우리가 원하는대로 랜더링 할수있다.
```

---