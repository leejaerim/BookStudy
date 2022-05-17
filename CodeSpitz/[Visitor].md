# [Visitor]

### MVVM 모델에서 Scanner에 대해 생각해본다.

스캐너는 엘리먼트를 스캔하여, 바인더에게 엘리먼트를 던져준다.

*(바인더가 스캔해서 엘리먼트를 바인딩 시키는 것은 바인더의 역할과 책임이 아니다.)

문제는 scanner의 scan 메서드에서 

```jsx
const binder = new Binder
const vm = el.getAttribute("data-viewmodel")
```

을  제외한 반복되는 로직은 스캐너의 역할이 아니기때문에 **다른 객체로의 위임이 필요하다.**
*(이렇게 설계 혹은 로직을 보고 역할을 나눌 수 있는 능력이 필요하다.)

이럴 때, 우리는 visitor Pattern을 사용하게 된다.

```jsx
const Scanner = class{
	#visitor; //프라이빗 백그라운드 필드 
	constructor(visitor, _=type(visitor, DomVisitor){
		this.#visitor = visitor;
	}//Domvisitor 타입 제한 (제네릭 T와 비슷한 역할을 수행하게 된다.)
	scan(target, _=type(target,HTMLElement){
		const binder = new Binder, f = el =>{
			const vm = el.getAttribute("data-viewmodel")
			if(vm) binder.add(new BinderItem(el,vm));
		};
		f(target);
		this.#visitor.visit(f,target);
		return binder;
	}
}
```

```jsx
const visitor = class{
	visit(action,target,_0=type(action,"function"){throw "override"}
}
const DomVisitor = class extends Visitor{
	visit(action, target,_0=type(action,"function"),_1=type(target,"HTMLElement"){
		const stack = [];
		let curr = target.firstElement;
		do{action(curr);
			if(curr.firstElementChild) stack.push(curr.firstElementChild);
			if(curr.nextElementSibling) stack.push(curr.nextElementSibling);
		}while(curr = stack.pop());
	}
}
```

---

### 인메모리 , 네이티브 메모리.

우리는 visitor를  추상화하여 추상 클래스를 만들고 그에 대한 확장으로 돔 네이티브(돔에 의존적인)Domvisitor를 만들게 됩니다.

이런 식으로 실제 인메모리 (Visitor)를 네이티브 메모리(Domvisitor)로 확장하여 쓰는 것은 좋습니다.

다만, 현재까지의 코드를 봤을때 자주 일어날 수 있는 문제가 있습니다. 바로 **추상계층 불일치** 입니다.

스캐너 클래스의 constructor는  Domvisitor를 참조제한하고 있습니다. 하지만 실제로는 visitor 부모클래스의 visitor를 오버라이딩해서 쓰고 있습니다. 

즉, visitor 수준에 정의된 visitor 메서드를 사용한다. 실제로는 자식형을 받았지만, 사용되는 메서드는 부모형입니다.

이렇게 스캐너 클래스에서 추상계층의 구현클래스를 참조하고 있습니다.

부모 추상객체에 인메모리만 존재하고, 돔과 관련된 네이티브 메모리는 제거하여 같은 추상 계층 수준에서 계약하게 한다.

우리는 추상계층을 일치 시킬 필요가 있고 그 코드는 다음과 같습니다.

```jsx
const Scanner = class{
	#visitor; //프라이빗 백그라운드 필드 
	constructor(visitor, _=type(visitor, Visitor){
		this.#visitor = visitor;
	}
	visit(f, target){this.#visitor.visit(f,target);}//위임(부모자식간)
	scan(target){ throw "override";}
}
const DomScanner = class extends Scanner{
	constructor(visitor, _=type(visitor, DomVisitor){
		super(visitor)
	}//Domvisitor 타입 제한 (제네릭 T와 비슷한 역할을 수행하게 된다.)
	scan(target, _=type(target,HTMLElement){
		const binder = new Binder, f = el =>{
			const vm = el.getAttribute("data-viewmodel")
			if(vm) binder.add(new BinderItem(el,vm));
		};
		f(target);
		this.#visitor.visit(f,target);
		return binder;
	}
}
```

---

클래스간의 의존성을 잘못설정하면 안됩니다. 그래서 우리는 계층관계를 생각해서 설계해야 된다.