# [MVVM]

<aside>
📌 본 학습은 코드스피츠 86강 2회 MVVM에서 학습한 내용입니다.

</aside>

- MVVM 모델은 기존의 MVC 나아가 MVP 디자인패턴의 상위 모델이라고 볼 수 있습니다.
- MVP의 경우 MVC에서 가지던 단점을 보완하였지만, 뷰와 프레젠테이션 간의 의존성은 사라지지 않았습니다.
- 마틴파울러 모델, 뷰, 모델뷰로 나눌 수 있으며, 뷰는 모델뷰의 존재에대해 의존성을 가지지 않습니다.

```jsx
const ViewModel = class{
	static #private = Symbol();
	static get(data) {
		return new ViewModel(this.#private, data);
	}
	styles={}; attributes={};properties={};event={};
	constructor(checker,data){
		if(checker != ViewModel.#private) throw "use ViewModel.get()";
		Object.entries(data).forEach(([k,v])=>{
			switch(k){
				case"styles":this.styles=v;break;
				case"attributes":this.attributes=v;break;
				case"properties":this.properties=v;break;
				case"event":this.event=v;break;
				default:this[k]=v;
			}
		});
		Object.seal(this);
	}
}
```

```jsx
const BinderItem = class{
	el; viewmodel;
	constructor(el,viewmodel,_0=type(el,HTMLElement),_1=type(viewmodel,"string")){
		this.el = el;
		this.viewmodel = viewmodel;
		Object.freeze(this);
	}
}
const Binder = class{
	#items = new Set;
	add(v,_=type(v,BinderItem)){this.#items.add(v);}
	render(viewmodel,_=type(viewmodel,ViewModel)){
		this.#items.forEach(item=>{
			const vm = type(viewmodel[item.viewmodel],ViewModel), el = item.el;
			Object.entries(vm.styles).forEach(([k,v])=>el.style[k]=v);
			Object.entries(vm.attributes).forEach(([k,v])=>el.setAttribute(k,v));
			Object.entries(vm.properties).forEach(([k,v])=>el[k]=v);
			Object.entries(vm.event).forEach(([k,v])=>rl["on"+k]=e=>v.call(el,e,viewmodel));
		})
	}
}
```

```jsx
const Scanner = class{
	scan(el,_=type(el,HTMLElement)){
		const binder = new Binder;
		this.checkItem(binder,el);
		const stack = [el.firstElementChild];
		let target;
		while(target = stack.pop()){
			this.checkItem(binder, target);
			if(target.firstElementChild) stack.push(target.firstElementChild);
			if(target.nextElementSibiling) stack.push(target.nextElementSibiling);
		}
		return binder;
	}
	checkItem(binder,el){
		const vm = el.getAttribute("data-viewmodel");
		if(vm) binder.add(new BinderItem(el,vm));
	}
}
```

```jsx
const viewmodel = ViewModel.get({
	wrapper:ViewModel.get({
		styles:{
			width:"50%",
			background:"#ffa",
			cursor : "pointer"
		}
	}),
	title:ViewModel.get({
		properties:{
			innerHTML:"TITLE"
		}
	}),
	contents:ViewModel.get({
		properties:{
			innerHTML:"CONTENTS"
		}
	})
})

const scanner = new Scanner;
const binder = scanner.scan(document.querySelector("#target"));
binder.render(viewmodel);
```

```jsx
const type = (target,type)=>{
    if(typeof type == "string"){
        if(typeof target != type) throw `invalid ${target} : ${type}`;
    }
    else if(!(target instanceof type)) throw `invalid type ${target} : ${type}`;
    return target;
};
```

---

```jsx
const viewmodel = ViewModel.get({
	isStop:false,
	changeContents(){
		this.wrapperstyles.background = 'rgb($(parseInt(Math.random()*150)+100},${...},${...})';
		this.contents.properties.innerHTML = Math.random().toString(16).replace(',','');
	}
	wrapper:ViewModel.get({
		styles:{width:"50%",background:"#ffa",cursor:"pointer"},
		event:{click(e,vm){vm.isStop=true;}}
	}),
	title:ViewModel.get({
		properties:{
			innerHTML:"TITLE"
		}
	}),
	contents:ViewModel.get({
		properties:{
			innerHTML:"CONTENTS"
		}
	})
})
const f =_=>{
		viewmodel.changeContents();
		binder.render(viewmodel);
		if(!viewmodel.isStop) requestAnimationFrame(f);
	}
requestAnimationFrame(f);
```

---

- 우리는 view를 건드리지 않고, 오로지 viewmodel의 값을 설정해줌으로써 , binder가 해당 뷰모델을 랜더링 하게 만든다.
- 스캐너가 html엘리먼트를 읽고, 그곳에 binder가 viewmodel을 바인딩하는 식,
- 

모델 - 뷰 - 뷰모델 의 형태

set과 배열의 차이는 배열의 경우 값을 저장하지만, set은 객체를 저장합니다.

이 부분은 단순히 값의 중복을 막는다는 것이 아닙니다. 배열 안의 값은 기본적으로 값으로 작용합니다.

객체지향언어 수준에서는 메모리참조를 기준으로 프로그래밍 합니다.  따라서 우리는 값이 아닌 메모리로 식별하며, 따라서 SET을 사용하여 오브젝트를 저장합니다.