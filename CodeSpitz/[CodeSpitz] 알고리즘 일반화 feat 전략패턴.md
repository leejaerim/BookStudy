# [알고리즘 일반화 feat 전략패턴]

```jsx
const Binder = class extends ViewModelListner{
	#item = new Set;
	#processors = {};
	...
	addProcessor(v,_0=type(v,Processor)){
		this.#processors[v.cat] = v;
	}
	render(viewmode, _=type(viewmodel, ViewModel)){
		const processores = Object.entries(this.#procassors);
		this.#item.forEach(item=>{
			const vm = type(viewmodel[item.viewmodel],ViewModel),
			processors.forEach(([pk,processor]) => {
				Object.entries(vm[pk]).forEach(([k,v])=>{
					processor.process(vm,el,k,v);
				});
			});
		});
	}
};
const Processor = class{
	cat;//category;
	constructor(cat){this.cat =cat; Object.freeze(this);}
	process(vm,el,k,v,_0=type(vm,...){
		this._process(vm,el,k,v);
	}
	_process(vm,el,k,v){throw "Override!"}
}
new (class extends Processor{
	_process(vm,el,k,v){el.style[k] = v;}
})("styles")
new (class extends Processor{
	_process(vm,el,k,v){el.setAttribute(k,v);}
})("attribute").
...

```

### 변하는 스트럭쳐와 변하지않는 부분을 컷오프하여 알고리즘 일반화 시킨다.

- 전략패턴은 그 중간과정이다.
- 

![Untitled](%5B%E1%84%8B%E1%85%A1%E1%86%AF%E1%84%80%E1%85%A9%E1%84%85%E1%85%B5%E1%84%8C%E1%85%B3%E1%86%B7%20%E1%84%8B%E1%85%B5%E1%86%AF%E1%84%87%E1%85%A1%E1%86%AB%E1%84%92%E1%85%AA%20feat%20%E1%84%8C%E1%85%A5%E1%86%AB%E1%84%85%E1%85%A3%E1%86%A8%E1%84%91%E1%85%A2%E1%84%90%E1%85%A5%E1%86%AB%5D%205eb3ab1c964a4676971efc71dac272b2/Untitled.png)

```jsx
binder.addProcessor(new (class extends Processor{
	_process(vm,el,k,v){el.style[k] = v;}
})("styles"));
```

<aside>
📌 Binder는 Processor에 대해 의존성을 가지며, 바인더에 의존성 주입해줌 으로써 , 객체지향기반 프로그래밍이 가능하다.

</aside>