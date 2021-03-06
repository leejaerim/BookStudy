# [MVVM]

<aside>
π λ³Έ νμ΅μ μ½λμ€νΌμΈ  86κ° 2ν MVVMμμ νμ΅ν λ΄μ©μλλ€.

</aside>

- MVVM λͺ¨λΈμ κΈ°μ‘΄μ MVC λμκ° MVP λμμΈν¨ν΄μ μμ λͺ¨λΈμ΄λΌκ³  λ³Ό μ μμ΅λλ€.
- MVPμ κ²½μ° MVCμμ κ°μ§λ λ¨μ μ λ³΄μνμμ§λ§, λ·°μ νλ μ  νμ΄μ κ°μ μμ‘΄μ±μ μ¬λΌμ§μ§ μμμ΅λλ€.
- λ§ν΄νμΈλ¬ λͺ¨λΈ, λ·°, λͺ¨λΈλ·°λ‘ λλ μ μμΌλ©°, λ·°λ λͺ¨λΈλ·°μ μ‘΄μ¬μλν΄ μμ‘΄μ±μ κ°μ§μ§ μμ΅λλ€.

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

- μ°λ¦¬λ viewλ₯Ό κ±΄λλ¦¬μ§ μκ³ , μ€λ‘μ§ viewmodelμ κ°μ μ€μ ν΄μ€μΌλ‘μ¨ , binderκ° ν΄λΉ λ·°λͺ¨λΈμ λλλ§ νκ² λ§λ λ€.
- μ€μΊλκ° htmlμλ¦¬λ¨ΌνΈλ₯Ό μ½κ³ , κ·Έκ³³μ binderκ° viewmodelμ λ°μΈλ©νλ μ,
- 

λͺ¨λΈ - λ·° - λ·°λͺ¨λΈ μ νν

setκ³Ό λ°°μ΄μ μ°¨μ΄λ λ°°μ΄μ κ²½μ° κ°μ μ μ₯νμ§λ§, setμ κ°μ²΄λ₯Ό μ μ₯ν©λλ€.

μ΄ λΆλΆμ λ¨μν κ°μ μ€λ³΅μ λ§λλ€λ κ²μ΄ μλλλ€. λ°°μ΄ μμ κ°μ κΈ°λ³Έμ μΌλ‘ κ°μΌλ‘ μμ©ν©λλ€.

κ°μ²΄μ§ν₯μΈμ΄ μμ€μμλ λ©λͺ¨λ¦¬μ°Έμ‘°λ₯Ό κΈ°μ€μΌλ‘ νλ‘κ·Έλλ° ν©λλ€.  λ°λΌμ μ°λ¦¬λ κ°μ΄ μλ λ©λͺ¨λ¦¬λ‘ μλ³νλ©°, λ°λΌμ SETμ μ¬μ©νμ¬ μ€λΈμ νΈλ₯Ό μ μ₯ν©λλ€.