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