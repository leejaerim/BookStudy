# Async Iterator

```jsx
const gene = function*(max, load, block){
	let i = 0, curr= load;
	while(i<max){
		if(curr--){
			block();
			i++;
		}else{
			curr = load;
			console.log(i);
			yield;
		}
	}
};
const gene2 = function*(max, load, block){
	let i = 0;
	while(i<max){
		yield new Promise(res=>{
			let curr = load;
			while(curr-- && i < max){
				block();
				i++;
			}
			console.log(i);
			timeout(res,0);
		});
	}
}

const gene3 = function*(max, block){
	let i = 0;
	while(i++ < max) yield new Promise(res=>{
		block();
		res();
	});
};
const nbfor = (max, load, block)=>{
	const iterator = gene2(max,load,block);
	const next = ({value, done} => done || value.then(v=>next(iterator.next());
	next(iterator.next());	
}

nbFor(10000,_=>console.log("nb");
const f =_=>{
	console.log("f");
	requestAniomationFrame(f);
}
requestAniomationFrame(f);\

```

- Frame Jobs 와 Promise Jobs 가 존재하며, 우리가 선언한 비동기적인 gene3의 경우, promise로 반환되는 `비동기적` 으로 순환하는 작업이 된다.
- 따라서 별도의 `OOME` 없이 모든 nbfor가 작업하고 나서 f 가 실행된다.
- ⇒ 이는 브라우저가 block으로 인식하여 죽이지 않고, 그러나 실제로는 block 되어 브라우저는 다운되지도 않고, 하나의 프레임내에서 block으로 움직인다.
- micro task 로 실행되는 `async iterator`

### Async & await

```jsx
const timeout = (f,ms)=>new Promise(res=>setTimeout(_=>res(f()),ms));
const f1 =_=>"abc";
const f2 =_=>"def";
const start = performance.now() //브라우저의 성능에 따른 정확한 시간 계산

// 프로미스 직렬 => 최대 1500ms
(()=>{
	timeout(f1, 500).then(v=>{
		console.log(v, performance.now() - start);
		return timeout(f2,1000);
	})
	.then(v=>console.log(v, performance.now() - start ));
})();

//async 병렬 => 최대 1000ms
(async () => {
	console.log(await timeout(f1, 500), performance.now() - start);
	console.log(await timeout(f2, 1000), performance.now() - start);
})();

//async 병렬 => 최대 1000ms
(async ()=>{
	const [v1 ,v2] = await Promise.all([timeout(f1, 500), timeout(f2, 1000)]);
	console.log(v1, v2, performance.now() - start);
})();

//async minMax *(가장 빠르게 응답이 온 비동기에 결과 제공) => 최대 500ms
(async ()=>{
	const v = await Promise.race([timeout(f1, 500), timeout(f2, 1000)]);
	console.log(v, performance.now() - start);
})();
 
```

- 단, minMax의 경우 성능이슈가 존재 ⇒ f1이 결과로 반환되어도 f2는 결과와 관계없이 실행됨.
- 반대로 all의 경우엔 모든 프로미스가 실행됨을 보장
- 쉽게 `await` 는 `.then(v=>{}` 을 생략할 수 있는 도구

---

```jsx
const api = async(url, timeout = 5000, info = {})=>{
	try{
		let id = -1;
		const v = await Promise.race([new Promise(res=>id = window.setTimeout(_=>res(), timeout)), 
			fetch(new Request(url, info))]);
		if(v instanceof Response){
			clearTimeout(id);
			return v.status === 404 ? new Error("404") : await v.text();
		}else return new Error("timeout");
	}catch(e){
		return e;
	}
}
(async()=>{
	const v = await api("200.html",1);
	if(v instanceof Error) console.log(`error ${v}`);
	else console.log(`contents : ${v}`);
}();
```

- race를 통해 타임아웃과 fetch를 둘다 경쟁 실행
⇒ 타임아웃 or fetch 둘중 하나 실행
- 무엇보다 컨텍스트를 잘 정리하고 나와야한다. fetch나 ,timeout을 클리어하거나.
⇒ 대용량 트래픽 서버에서는 문제가 될 수 있음.

```jsx
const api2 = async(url, timeout = 5000, info = {})=>{
	let id = -1;
	const v = await Promise.race([new Promise(res=>id = window.setTimeout(_=>res(), timeout)), 
		fetch(new Request(url, info))]);
	if(v instanceof Response){
		clearTimeout(id);
		return v.status === 404 ? throw Error("404") : await v.text();
	}else throw new Error("timeout");
}
(async() => {
	try{
		const {id, nick, thumb} = await api("/member");
		const [{name, email, sex}, friendsId] = await Promise.all([api2(`/detail/${id}`),
			api2(`/friends/${id}`)
		]);
		updateMember(nick, thumb, name, email, sex);
		updateFriends(
			(await Promise.all(friendsId.map(id=> api(`/detail/${id}`)))).map((v,idx)=>({id:friendsId[dix], ...v}))
		);
	}catch(e){console.log(e)}
}
```

- throw로 async 관리 한다. ⇒ async 함수는 return으로 Promise 객체로 wrapping 해서 반환하게 되는데, Promise에서 내제된 throw를 await에서 관리해준다.
**es 표준에 해당하는 정제된 코드**
- 동기와 비동기 자유롭게 혼재된 코드 ⇒ 자바스크립트에서 Promise가 아주 중요한 역할.
-