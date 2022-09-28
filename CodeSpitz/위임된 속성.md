# 위임된 속성

### Delegatpor - 위임

```jsx
const by = (cls) =>{
	Object.entries(cls).filter(([,v])=>typeof v.getValue == 'function' 
		&& typeof v.setValue == 'function').reduce((proto, [key,delegator])=>{
		Object.defineProperty(proto, key, {
			get(){
				return delegator.getValue(this, key);
			}
			set(v){
				delegator.setValue(this,key,v);
			}
		});
		return proto;
	},cls.prototype)
}
const Test = by(class{
	static name = new TestDelegate;
	static company = new TestDelegate;
	map = new Map;
});
class TestDelegate{
	getValue(target,k){
		return target.map.get(k) ?? "no ${k}";
	}
	setValue(target, k, v){
		target.map.set(k,v);
	}
}

const prop = (target, key, delegator) => {
	Object.defineProperty(target, key, {
		get(){
			return delegator.getValue(this,key);
		}
		set(v){
			delegator.setValue(this, key, v);
		}
	}
}
```

- `Object.entries(cls)`   → 객체를 입력받아 k,v의 리스트로 반환

---

### Observer

```jsx
const observe =(_=>{
	class Observer{
		#value;
		#observer;
		constructor(value, observer){
			this.#value = value;
			this.#observer = observer;
		}
		getValue(target,k){return this.#value;}
		setValue(target,k,v){
			this.#observer(target,k,this.#value,this.#value=v);
		}
	}
	return (value, observer)=>new Observer(value,observer);
})();

const Test = by(class{
	static name = observe("",(target, key, old, v)=>{
		if(old === v) return;
		document.querySeletor("#name").value = v;
	});
	static company = observe("",(target, key, old, v)=>{
		if(old ===v ) return;
		document.querySelector("#company").value = v;
	});
}

<input id="name">
<input id="company">
<script>
	const test = new Test;
	document.querySelector("#name").onchange = ({target : {value}}) => test.name = value;}
	document.querySelector("#company").onchange = ({target:{value}})=>test.company = value;)
	test.name = "hika";
</script>
```

- `by()` 를 통해 해당 클래스의 name, company를 위임하여 준다.
- 계속해서 재귀(리커전)되어 값을 변경하지 않도록 `old == v` 값 비교 하여 준다.

---