# [거침없는 자바스크립트 85강 6회차]

<aside>
🔥 Shared Array Buffer에 대하여 공부합니다.

</aside>

---

### WebWorker

- 기본적으로 자바스크립트는 단일 스레드 이다. 그렇기 때문에 이미지 처리와 같은 큰 데이터를 처리하게 되면 그동안 브라우저는 블록킹 될 수 있다. 그런 경우를 피하기 위해 우리는 `웹워커` 을 이용하여 js를 이용한 멀티스레드 환경(추가적인 js)을 구축할 수 있다.
- PostMessage / onMessage를 통한 ***포어그라운드↔ 백그라운드 간 통신을 하며, 포어그라운드의 블록킹 없이 백그라운드에서 처리***할 수 있도록 한다.

```jsx
// -- Background Thread 최초의 포스트 메세지에서 발동
// worker.postMessage("Hello"); //프로세스간 메세지 & 스레드 통신간에도 적합
onmessage = ({data})=>{
	...//필요한 데이터만 해체
	postMessage("world")//백그라운드간 통신은 불가, 포그라운드만 통신
}//이벤트 리스너가 존재
// Main Thread
worker.postMessage("Hello")//
onworkerMessage = ({data})=>{...}
```

---

### URL & Blob

`Blob`  : 파일객체와 같은 바이너리 객체

```jsx
URL.createObjectURL(
	new Blob(['...']),{type:'text/javascript'})
)
//blob:http://... 
// 모든 SRC든 다 쓸 수 있다. 인메모리로 부터 URL을 얻어서 사용할 수 있다.
// 매우 유명한 기법
// 단, 브라우저에 따라 호환성이 다르다.
```

---

### workerPromise(반제어, 지연 등 )

```jsx
//WorkerTemplete

const mine = {js:{type:'text/javascript'}}
const WorkerPromise =f=>{
	let resolve,reject;
	const worker = object.assign(new Worker(...blob...${f}(e.data)...),
{onmessage:e=>resolve(e.data),onerror:e=>reject(e.data)}}
	return date => new Promise((res,rej)=>{
		resolve= res;
		reject = rej;
		worker.postMessage(data);
	}
}
const addHello = WorkerPromise(str=>str+"world");
addHello("Hello").then(console.log);
```

---

### Greyscale

```jsx
//큰데이터의 배열처리는 쉽지 않습니다. 특히 이미지의 배열 처리는 백그라운드로 보냅니다.
const greyscale = WorkPromise(imgData=>{
	for(let i =0; i<imgData.length; i+= 4){
		const v = .34*imgData[i] +.5*imgData[i+1]+.16*imgData[i+2]
		imgData[i]=imgData[i+1]=imgData[i+2] = v
	}
})//원본훼손의 경우가 없다.
img.onload =({target})=>{
	const {width,height} = target;
	const ctx = Object.assgin(canvas,{width,height}).getContext("2d")
	ctx.drawImage(target,0,0)
	const imgData = ctx.getImageData(0,0,width,height).data;
	greyscrale(imgData).then(v=>ctx.putImage(new Image(v,with,height),0,0));
//백그라운드에서 그려주기 때문에 타임아웃이나, 포그라운드의 블록킹이 일어나지 않는다.
}
```

<aside>
🔥 다음과 같은 방법을 통해 대부분의 무거운 로직을 백그라운드 스레드로 옮길 수 있다.

</aside>

---

### ArrayBuffer

- 기본적으로 링크드 리스트

```jsx
new ArrayBuffer(12); //12Bytes -> ByteArray, 메모리 확보
const intView = new Int32Array(new ArrayBuffer(12));//원본 데이터를 참조해야됌.32bit 4개
const utiny = new Uint8ClampedArray(new ArrayBuffer(12)));//부호없는 양수 8bit Int
//View를 통해 조작할 수 잇음. 하나의 원본 데이터를 View가 공유할수 있음.
//하나의 데이터 방식임에도 압축하여 사용할 수있음.
```

<aside>
🔥 백그라운드로 보내지는 공유 메모리는 오로지 공유배열버퍼 밖에 없다.

</aside>

```jsx
ctx.drawImage(target,0,0);
const sObj = new SharedArrayBuffer(width*height*4);
const u8c = new Uint8ClampedArray(sObj);
const imgData = ctx.getImageData(0,0,width,height).data;
u8c.set(imgData);//View를 만들어 캔버스로 얻어온 데이터를 빠르게 복사함
greyscale(sObj).then(_=>{//백그라운드로 복사없이 전달될 수 있는 타입은 오로지 쉐어드어레이버퍼 타입밖에 없다.
	const r = new Uint8ClampedArray(u8c.bytelength);//length와 다른 bytelength가 존재
	r.set(u8c);
	ctx.putImageData(new ImageData(r,width,height),0,0)//이미 버퍼타입으로 리턴, 보
});
```

```jsx
const brightness = WorkerPromise(({rate, sObj})=>{
	const v = new Uint8ClampedArray(sObj);
	...
	return sObj;
})// 동시성 문제의 생성.(공유된 메모리이기 때문에)
greyscale(sObj).then(copy)
brightness({rate:-.1,sObj)}.then(copy)
//greyscale이 되는 와중에 brightness가 실행될 수 있음.
```

---

### Schedule Queue

- LInked List 사용

```jsx
const worker = Object.assign(new Worker(URL.createObjectURL(new Blob[...]),{
	{onmessage:e=>(resolve(e.data), next()),onerror:e=>(reject(e.data), next())}
}
const next=_=>{
	if(!start.next) return ;
	//distructor. 연산자 (ex: 배열,객체 해체)
	({data, resolve, reject} = start.next); 
	//객체해체는 괄호로 묶어줘야하고 배열은 별도의 괄호 없이 해체 가능
	start = start.next ;
	worker.postMessage(data);
}
let start, end ; 
...
return data => new Promise((res,rej)=>{
	const v = {data, resolve:res , reject:rej}
	if(end) end = end.next = v;//Linked List
	else{
		start = end = v;
		resolve = res;
		reject = rej;
		worker.prostMessage(data);
	}
})//invoke와 execution 의 분리 -> invoke에서 모든 정보를 알고 있어야 합니다.(커맨드 패턴)
// 상단 v 객체만 알고 있으면(내부 3가지 data) execution 할 수 있음
```

<aside>
📌 ABC계통 언어는 할당식은 우측에서 좌측으로 파싱되는 모순점을 가지고 있다.(수학자가 언어 구축해서)

</aside>

---